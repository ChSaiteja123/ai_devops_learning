from celery import shared_task
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def index_document_task(self, document_id: int):
    """Background task: index a document into the vector store."""
    try:
        from .models import Document
        from .services import RAGService
        doc = Document.objects.get(id=document_id)
        service = RAGService()
        success = service.index_document(doc)
        if not success:
            raise Exception(f'Indexing failed for document {document_id}')
        logger.info('Document %s indexed successfully', document_id)
    except Exception as exc:
        logger.error('index_document_task error: %s', exc)
        raise self.retry(exc=exc, countdown=60)
