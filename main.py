# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import router as api_router  # assumes you have APIRouter in app/api.py

app = FastAPI(title="PokemonAPI", version="0.1.0")



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
    allow_methods=["*"],
    allow_headers=["*"],
)

# mount your routes under /api
app.include_router(api_router, prefix="/api")

@app.get("/api/ping")
def pint():
    return{"ok": True}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)