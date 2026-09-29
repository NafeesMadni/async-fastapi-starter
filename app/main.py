from __future__ import annotations

from fastapi import FastAPI

app = FastAPI(title="Async FastAPI starter app")


@app.get("/health")
async def health():
    """Return a message indicating that the application is responding."""
    return {"message": "I'm healthy!"}
