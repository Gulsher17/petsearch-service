from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes import search, admin

app = FastAPI(title=settings.APP_NAME, version="1.0.0")

origins = [
    "http://localhost:5174",
    "http://127.0.0.1:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
def health():
    return {"ok": True, "service": settings.APP_NAME}

# ✅ Keep routes after middleware
app.include_router(search.router)
app.include_router(admin.router)
