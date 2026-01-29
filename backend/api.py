"""
FastAPI backend server for My Personal Agent
"""
import sys
import os
from pathlib import Path

# Add parent directory to path to import modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from typing import Optional
import tempfile
import shutil
import json

from src.my_personal_agent.modules.vehicle_diagnostics import VehicleDiagnostics
from src.my_personal_agent.modules.resume_analyzer import ResumeAnalyzer
from src.my_personal_agent.modules.resume_builder import ResumeBuilder

app = FastAPI(title="My Personal Agent API")

# CORS middleware
# Allow both local development and production Vercel URLs
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    # Add your Vercel frontend URL here after deployment
    # Example: "https://your-app.vercel.app"
]
# Also allow any Vercel preview deployments
import os
vercel_url = os.getenv("VERCEL_URL")
if vercel_url:
    allowed_origins.append(f"https://{vercel_url}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize modules
vehicle_diagnostics = VehicleDiagnostics()
resume_analyzer = ResumeAnalyzer()
resume_builder = ResumeBuilder()


@app.get("/")
async def root():
    return {"message": "My Personal Agent API", "status": "running"}


@app.get("/api/health")
async def health():
    return {"status": "healthy"}


@app.post("/api/vehicle")
async def diagnose_vehicle(
    image: UploadFile = File(...),
    description: Optional[str] = Form(None)
):
    """Diagnose vehicle from uploaded image"""
    tmp_path = None
    try:
        # Validate file type
        if not image.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        # Get file extension
        file_ext = Path(image.filename).suffix.lower()
        if file_ext not in ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp']:
            raise HTTPException(status_code=400, detail=f"Unsupported image format: {file_ext}. Supported: PNG, JPG, JPEG, GIF, BMP, WEBP")
        
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
            shutil.copyfileobj(image.file, tmp_file)
            tmp_path = tmp_file.name
        
        # Validate file exists and has content
        if not os.path.exists(tmp_path) or os.path.getsize(tmp_path) == 0:
            raise HTTPException(status_code=400, detail="Uploaded file is empty or invalid")
        
        try:
            result = vehicle_diagnostics.diagnose(
                image_path=tmp_path,
                user_description=description,
                include_contacts=True,
            )
            return result
        except Exception as diag_error:
            # Log the actual error for debugging
            import traceback
            error_details = traceback.format_exc()
            print(f"Vehicle diagnostics error: {str(diag_error)}")
            print(f"Traceback: {error_details}")
            raise HTTPException(status_code=500, detail=f"Diagnostics failed: {str(diag_error)}")
        finally:
            # Clean up temp file
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.unlink(tmp_path)
                except Exception:
                    pass
    except HTTPException:
        # Re-raise HTTP exceptions
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
        raise
    except Exception as e:
        # Log unexpected errors
        import traceback
        error_details = traceback.format_exc()
        print(f"Unexpected error in vehicle diagnostics: {str(e)}")
        print(f"Traceback: {error_details}")
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
        raise HTTPException(status_code=500, detail=f"Failed to analyze image: {str(e)}")


@app.post("/api/resume/analyze")
async def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    """Analyze resume against job description"""
    try:
        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(resume.filename).suffix) as tmp_file:
            shutil.copyfileobj(resume.file, tmp_file)
            tmp_path = tmp_file.name
        
        try:
            result = resume_analyzer.analyze(
                resume_path=tmp_path,
                job_description_text=job_description,
            )
            return result
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/resume/build")
async def build_resume(data: dict):
    """Build resume from provided data"""
    try:
        experiences = data.get("experiences", [])
        skills = data.get("skills", [])
        education = data.get("education", [])
        portfolio = data.get("portfolio", [])
        target_job = data.get("target_job")
        output_format = data.get("output_format", "pdf")
        
        result = resume_builder.build_resume(
            experiences=experiences,
            skills=skills,
            education=education,
            portfolio_items=portfolio,
            target_job=target_job,
            output_format=output_format,
        )
        
        # Convert file path to relative URL path
        file_path = result["file_path"]
        # Extract filename from path
        filename = Path(file_path).name
        
        return {
            "file_path": result["file_path"],
            "download_url": f"/api/resume/download/{filename}",
            "format": result["format"],
            "resume_data": result["resume_data"],
        }
    except Exception as e:
        # Log full error details for debugging
        import traceback
        error_details = traceback.format_exc()
        print(f"Resume build error: {str(e)}")
        print(f"Traceback: {error_details}")
        raise HTTPException(status_code=500, detail=f"Failed to build resume: {str(e)}")


@app.get("/api/resume/download/{filename}")
async def download_resume(filename: str):
    """Download a generated resume file"""
    try:
        from src.my_personal_agent.config import settings
        
        # Construct the file path
        file_path = Path(settings.output_dir) / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        
        # Determine media type
        media_type_map = {
            ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ".doc": "application/msword",
            ".pdf": "application/pdf",
            ".txt": "text/plain",
        }
        
        media_type = media_type_map.get(file_path.suffix.lower(), "application/octet-stream")
        
        return FileResponse(
            path=str(file_path),
            filename=filename,
            media_type=media_type,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
