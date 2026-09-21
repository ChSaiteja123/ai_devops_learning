# Secure Local RAG Assistant

A dependency-free retrieval-augmented generation foundation. It demonstrates document filtering, keyword retrieval, source citations, and a safe fallback without calling an external model.

## Run

```powershell
python rag_assistant.py "How do I deploy safely?"
```

## Production extensions

- replace keyword retrieval with embeddings and a vector store
- enforce tenant permissions before retrieval
- add a model provider adapter with timeouts
- validate output and cite source IDs
- add prompt-injection tests and PII redaction
- store API keys outside source control
