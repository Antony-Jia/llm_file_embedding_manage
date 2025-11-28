from fastapi import FastAPI

from app.api.v1 import auth, org, documents, chat, llm, search, embeddings

app = FastAPI(title="File Embedding Platform", version="0.1.0")

# include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(org.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(llm.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")
app.include_router(embeddings.router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok"}
