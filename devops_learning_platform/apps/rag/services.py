"""
RAG (Retrieval Augmented Generation) Service.

WHAT IS RAG?
------------
RAG enhances LLM responses by retrieving relevant documents from a
knowledge base BEFORE generating an answer.

WITHOUT RAG:
  User: "What does our runbook say about high CPU alerts?"
  LLM: "I don't have access to your runbooks."

WITH RAG:
  1. User question → Embed into vector
  2. Search vector DB for similar document chunks
  3. Include those chunks in the LLM prompt
  4. LLM answers based on YOUR documents

ARCHITECTURE:
-------------
Document Upload → Text Extraction → Chunking → Embedding → Vector DB
                                                                ↓
User Query → Embed Query → Similarity Search → Retrieve Chunks
                                                      ↓
                                              LLM + Chunks → Answer

VECTOR DATABASE:
----------------
We use ChromaDB (open-source, runs locally).
Each document chunk is stored as a high-dimensional vector.
Similarity search finds the most relevant chunks for a query.
"""
import logging
import time
from pathlib import Path
from django.conf import settings
from .models import Document, RAGQuery

logger = logging.getLogger(__name__)


class RAGService:
    def __init__(self):
        self.openai_key = getattr(settings, 'OPENAI_API_KEY', '')
        self.chroma_dir = getattr(settings, 'CHROMA_PERSIST_DIRECTORY', './chroma_db')
        self.chunk_size = getattr(settings, 'RAG_CHUNK_SIZE', 1000)
        self.chunk_overlap = getattr(settings, 'RAG_CHUNK_OVERLAP', 200)
        self._collection = None

    def _get_collection(self):
        """Lazy-load Chroma collection."""
        if self._collection is None:
            try:
                import chromadb
                client = chromadb.PersistentClient(path=self.chroma_dir)
                self._collection = client.get_or_create_collection(
                    name='devops_knowledge',
                    metadata={'hnsw:space': 'cosine'},
                )
            except ImportError:
                logger.warning('chromadb not installed. Vector search unavailable.')
        return self._collection

    def index_document(self, document: Document) -> bool:
        """
        Process a document: extract text, chunk, embed, store in vector DB.
        Returns True on success.
        """
        document.status = 'processing'
        document.save(update_fields=['status'])

        try:
            # 1. Extract text
            text = self._extract_text(document)
            if not text:
                raise ValueError('Could not extract text from document.')

            document.content = text
            document.save(update_fields=['content'])

            # 2. Chunk text
            chunks = self._chunk_text(text)

            # 3. Store in vector DB
            collection = self._get_collection()
            if collection:
                ids = [f'doc_{document.id}_chunk_{i}' for i in range(len(chunks))]
                metadatas = [{
                    'document_id': document.id,
                    'title': document.title,
                    'category': document.category,
                    'chunk_index': i,
                } for i in range(len(chunks))]

                # Upsert in batches of 100
                for i in range(0, len(chunks), 100):
                    collection.upsert(
                        documents=chunks[i:i+100],
                        ids=ids[i:i+100],
                        metadatas=metadatas[i:i+100],
                    )

            document.chunk_count = len(chunks)
            document.status = 'indexed'
            from django.utils import timezone
            document.indexed_at = timezone.now()
            document.save(update_fields=['chunk_count', 'status', 'indexed_at'])
            return True

        except Exception as exc:
            logger.error('Failed to index document %s: %s', document.id, exc)
            document.status = 'failed'
            document.error_message = str(exc)
            document.save(update_fields=['status', 'error_message'])
            return False

    def query(self, query_text: str, user=None, n_results: int = 5) -> dict:
        """
        Query the knowledge base and generate an answer using RAG.
        Returns: {answer, sources, confidence, response_time_ms}
        """
        start_time = time.time()

        # 1. Retrieve relevant chunks
        chunks, sources = self._retrieve(query_text, n_results)

        # 2. Generate answer
        if chunks:
            answer = self._generate_answer(query_text, chunks)
            confidence = 0.85
        else:
            answer = self._fallback_answer(query_text)
            confidence = 0.3
            sources = []

        response_time_ms = int((time.time() - start_time) * 1000)

        # 3. Log the query
        RAGQuery.objects.create(
            user=user,
            query=query_text,
            answer=answer,
            source_documents=sources,
            confidence_score=confidence,
            response_time_ms=response_time_ms,
        )

        return {
            'answer': answer,
            'sources': sources,
            'confidence': confidence,
            'response_time_ms': response_time_ms,
        }

    def _retrieve(self, query_text: str, n_results: int) -> tuple:
        collection = self._get_collection()
        if not collection:
            return [], []
        try:
            results = collection.query(query_texts=[query_text], n_results=n_results)
            docs = results.get('documents', [[]])[0]
            metas = results.get('metadatas', [[]])[0]
            sources = [{'title': m.get('title', ''), 'category': m.get('category', '')} for m in metas]
            return docs, sources
        except Exception as exc:
            logger.warning('Vector search error: %s', exc)
            return [], []

    def _generate_answer(self, query: str, chunks: list) -> str:
        context = '\n\n---\n\n'.join(chunks[:5])
        prompt = (
            f"Based on the following documentation, answer this question:\n\n"
            f"Question: {query}\n\n"
            f"Documentation:\n{context}\n\n"
            f"Provide a clear, structured answer. If the docs don't fully answer the question, "
            f"say so and provide general guidance."
        )
        try:
            import openai
            client = openai.OpenAI(api_key=self.openai_key)
            response = client.chat.completions.create(
                model='gpt-4o',
                messages=[
                    {'role': 'system', 'content': 'You are a DevOps expert. Answer questions based on the provided documentation.'},
                    {'role': 'user', 'content': prompt},
                ],
                max_tokens=1200,
                temperature=0.3,
            )
            return response.choices[0].message.content
        except Exception as exc:
            logger.warning('OpenAI error in RAG: %s', exc)
            return f"Based on the indexed documentation:\n\n" + '\n\n'.join(chunks[:2])

    def _fallback_answer(self, query: str) -> str:
        return (
            f"No documents are currently indexed in the knowledge base.\n\n"
            f"To use RAG:\n"
            f"1. Upload documents via POST /api/v1/rag/documents/\n"
            f"2. Wait for indexing to complete\n"
            f"3. Query via POST /api/v1/rag/query/\n\n"
            f"Supported formats: PDF, TXT, Markdown, DOCX"
        )

    def _extract_text(self, document: Document) -> str:
        if document.content:
            return document.content
        if document.file:
            file_path = document.file.path
            suffix = Path(file_path).suffix.lower()
            if suffix in ('.txt', '.md'):
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    return f.read()
            if suffix == '.pdf':
                try:
                    import pypdf
                    with open(file_path, 'rb') as f:
                        reader = pypdf.PdfReader(f)
                        return '\n'.join(page.extract_text() or '' for page in reader.pages)
                except ImportError:
                    pass
        return ''

    def _chunk_text(self, text: str) -> list:
        """Split text into overlapping chunks."""
        chunks = []
        size = self.chunk_size
        overlap = self.chunk_overlap
        start = 0
        while start < len(text):
            end = start + size
            chunks.append(text[start:end])
            start += size - overlap
        return [c.strip() for c in chunks if c.strip()]
