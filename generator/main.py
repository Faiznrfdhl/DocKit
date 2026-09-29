from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from .engine import DocKitEngine
from pydantic import BaseModel
import os

app = FastAPI(title="DocKit Generator API")

# Inisialisasi engine dengan folder templates
engine = DocKitEngine(templates_dir=os.path.join(os.getcwd(), "generator/templates"))

class GenerateRequest(BaseModel):
    framework: str = "fastapi"
    project_name: str = "my-awesome-project"
    db_enabled: bool = True
    redis_enabled: bool = False

@app.post("/generate")
def generate_project(req: GenerateRequest):
    context = req.model_dump()
    zip_file = engine.generate(framework=req.framework, options=context)
    
    filename = f"{req.project_name}.zip"
    
    return StreamingResponse(
        zip_file,
        media_type="application/x-zip-compressed",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )