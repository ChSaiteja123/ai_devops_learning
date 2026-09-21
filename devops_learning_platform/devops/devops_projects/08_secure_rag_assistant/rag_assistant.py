import json
import sys
from pathlib import Path


DOCUMENTS = json.loads(Path("documents.json").read_text(encoding="utf-8"))


def retrieve(question, tenant="public", limit=3):
    query_terms = {term.lower() for term in question.split() if len(term) > 2}
    candidates = []
    for document in DOCUMENTS:
        if document["tenant"] != tenant:
            continue
        searchable = f"{document['title']} {document['content']}".lower()
        score = sum(term in searchable for term in query_terms)
        if score:
            candidates.append((score, document))
    return [document for _, document in sorted(candidates, reverse=True, key=lambda item: item[0])[:limit]]


def answer(question):
    sources = retrieve(question)
    if not sources:
        return {
            "answer": "I do not have enough approved context to answer that question.",
            "sources": [],
        }

    context = " ".join(document["content"] for document in sources)
    citations = [document["id"] for document in sources]
    return {"answer": context, "sources": citations}


def main():
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        raise SystemExit("Usage: python rag_assistant.py <question>")
    result = answer(question)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
