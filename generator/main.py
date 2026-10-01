import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from .engine import DocKitEngine
from fastapi.middleware.cors import CORSMiddleware

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")

app = FastAPI(
    title="DocKit Generator API",
    description=(
        "**DocKit — Docker Development Kit.**\n\n"
        "Generate production-ready project boilerplates in seconds."
    ),
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = DocKitEngine(templates_dir=TEMPLATES_DIR)


class GenerateRequest(BaseModel):
    framework: str = Field("fastapi", examples=["fastapi"])
    project_name: str = Field("my-awesome-project", examples=["my-awesome-project"])
    db_enabled: bool = True
    redis_enabled: bool = False


@app.get("/", tags=["Meta"])
def root():
    return {
        "name": "DocKit",
        "tagline": "Generate production-ready project boilerplates in seconds.",
        "version": app.version,
        "docs": "/docs",
        "available_frameworks": engine.list_frameworks(),
        "endpoints": {
            "GET /frameworks": "Daftar framework yang didukung",
            "POST /generate": "Generate project & download ZIP",
        },
    }


@app.get("/frameworks", tags=["Meta"])
def list_frameworks():
    return {"frameworks": engine.list_frameworks()}


@app.post("/generate", tags=["Generator"])
def generate_project(req: GenerateRequest):
    if not engine.framework_exists(req.framework):
        raise HTTPException(
            status_code=404,
            detail=f"Framework '{req.framework}' belum tersedia. "
                   f"Pilihan saat ini: {engine.list_frameworks()}",
        )

    zip_buffer = engine.generate(req.framework, req.model_dump())
    filename = f"{req.project_name}.zip"

    return StreamingResponse(
        zip_buffer,
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )