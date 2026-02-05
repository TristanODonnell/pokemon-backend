# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router as api_router  # assumes you have APIRouter in app/api.py

# The core application instance.
# The title and version appear in the auto-generated /docs (Swagger) page.
app = FastAPI(title="PokemonAPI", version="0.1.0")

# Security: Cross-Origin Resource Sharing (CORS)
# This allows our React frontend (Vite) to communicate with this API.
# Without this, the browser's "Same-Origin Policy" would block the requests.

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://pokemon-frontend-aud0.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"], # Allows GET, POST, etc.
    allow_headers=["*"], # Allows custom headers like 'Content-Type'
)

# Route Orchestration:
# We mount the pokemon router under the /api prefix to keep the URL
# structure organized (eg: /api/pokemon/pikachu).
app.include_router(api_router, prefix="/api")

@app.get("/api/ping")
def pint():
    return{"ok": True}


if __name__ == "__main__":
    # For local development: enables auto-reload on file changes.
    import uvicorn
    uvicorn.run("main:app", reload=True)