 
# HelpTulsa.ai — Semantic Microservice Stack

HelpTulsa.ai is a minimal, container-native system for searching reentry and mental-health resources using semantic search.

Built with:

- 🧠 **FastAPI** backend with Sentence-Transformers
- 📦 **Qdrant** vector database
- 🕸️ **React + Tailwind** frontend
- 🐳 Docker Compose microservices

---

## 🧩 Services

| Service           | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| `crawler_service` | Converts `inputs/resources.xlsx` into `data/resources.jsonl`.               |
| `vector_service`  | Embeds records using `all-MiniLM-L6-v2` and upserts into Qdrant.            |
| `api_service`     | Exposes `/ask` for semantic search and `/admin/refresh` for re-indexing.   |
| `frontend`        | React + Tailwind UI for natural language queries.                           |

---

## 🚀 Usage

### 1. Clone & Setup

`bash
git clone https://github.com/YOUR_USERNAME/helptulsa.git
cd helptulsa
cp .env.example .env`

### 2. Add Excel Input File

Place your resource spreadsheet at:

inputs/resources.xlsx

### 3. Run Everything

docker compose up --build

This will launch:

    🔌 API: http://localhost:8000

    💬 UI: http://localhost:5173

    📊 Qdrant UI: http://localhost:6333/dashboard

## 🔍 API: Semantic Search
POST /ask

Submit a natural language query and return top-k matches.

Request:

`{
  "query": "Where can I get trauma counseling?",
  "top_k": 5
}`

Response:

`{
  "query": "Where can I get trauma counseling?",
  "results": [
    {
      "score": 0.91,
      "resource": {
        "Name": "Inside Out Reentry Services",
        "Services/Notes": "Trauma counseling, child reunification",
        "City": "Tulsa",
        ...
      }
    }
  ]
}`

## 💻 Frontend (React + Tailwind)

Open your browser to:

`http://localhost:5173`

Type a question like:

Where can I find housing for single mothers?

You’ll see live, styled, scored semantic search results.
## 🔄 Admin Refresh

Trigger re-ingestion of data:
POST /admin/refresh

Headers:

X-Token: changeme

This runs:

    crawler_service: Re-parses resources.xlsx

    vector_service: Re-embeds + upserts into Qdrant

🧠 Dev Notes

    Sentence embeddings powered by sentence-transformers

    React UI uses fetch() to hit /ask

    Qdrant stores vectors and payloads in help_resources collection

    CORS configured for cross-origin access

🔧 Coming Soon

    ✅ Feedback buttons (helpful / not helpful)

    📈 Admin dashboard for diffs and edit history

    ☁️ Deployments via Railway, Render, or Vercel

📄 License

MIT © HelpTulsa.ai, 2025
