import os
import subprocess
from typing import List

from fastapi import FastAPI, HTTPException, Header, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from qdrant_client import QdrantClient
from sentence_transformers import SentenceTransformer

COLLECTION_NAME = "help_resources"

app = FastAPI()

# CORS middleware to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="help_tulsa_api/templates")

client = QdrantClient(
    host=os.getenv("QDRANT_HOST", "qdrant"),
    port=int(os.getenv("QDRANT_PORT", "6333"))
)
model = SentenceTransformer("all-MiniLM-L6-v2")
admin_token = os.getenv("ADMIN_TOKEN", "changeme")


class AskRequest(BaseModel):
    query: str
    top_k: int = 5


@app.post("/ask")
def ask(req: AskRequest):
    vector = model.encode(req.query).tolist()
    hits = client.search(collection_name=COLLECTION_NAME, query_vector=vector, limit=req.top_k)

    return {
        "query": req.query,
        "results": [
            {
                "score": round(h.score, 4),
                "resource": h.payload
            } for h in hits
        ]
    }


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/ask-ui", response_class=HTMLResponse)
def ask_ui(request: Request, query: str = Form(...)):
    vector = model.encode(query).tolist()
    hits = client.search(collection_name=COLLECTION_NAME, query_vector=vector, limit=5)

    results = [
        {"score": round(h.score, 4), "resource": h.payload}
        for h in hits
    ]

    return templates.TemplateResponse("index.html", {
        "request": request,
        "results": results,
        "query": query
    })


@app.post("/admin/refresh")
def refresh(x_token: str = Header(..., alias="X-Token")):
    if x_token != admin_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    print("Running crawler and vector services")
    subprocess.run(["docker", "compose", "run", "--rm", "crawler"], check=False)
    subprocess.run(["docker", "compose", "run", "--rm", "vector"], check=False)
    return {"status": "jobs launched"}
