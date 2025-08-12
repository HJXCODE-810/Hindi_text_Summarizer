from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from docx import Document
import os
import uuid
from pathlib import Path
from summarizer import summarize_hindi

app = FastAPI(title="Hindi Document Summarizer")

# Configure directories
UPLOAD_FOLDER = "uploads"
SUMMARY_FOLDER = "summaries"
Path(UPLOAD_FOLDER).mkdir(exist_ok=True)
Path(SUMMARY_FOLDER).mkdir(exist_ok=True)

# Setup templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.lower().endswith('.docx'):
        raise HTTPException(status_code=400, detail="Please upload a valid .docx file")
    
    try:
        # Generate unique filename
        file_id = str(uuid.uuid4())
        upload_path = os.path.join(UPLOAD_FOLDER, f"{file_id}.docx")
        summary_filename = f"summary_{file.filename}"
        summary_path = os.path.join(SUMMARY_FOLDER, summary_filename)
        
        # Save uploaded file
        with open(upload_path, "wb") as buffer:
            buffer.write(await file.read())

        # Read DOCX content
        doc = Document(upload_path)
        full_text = '\n'.join([para.text for para in doc.paragraphs if para.text])

        if not full_text.strip():
            raise HTTPException(status_code=400, detail="The uploaded document appears to be empty")

        # Summarize
        summary_text = summarize_hindi(full_text)

        # Write summary to new DOCX
        summary_doc = Document()
        heading = summary_doc.add_heading('', level=1)
        heading_run = heading.add_run('सारांश')
        heading_run.font.name = 'Nirmala UI'
        
        for line in summary_text.split('\n'):
            if line.strip():
                para = summary_doc.add_paragraph('')
                run = para.add_run(line)
                run.font.name = 'Nirmala UI'
        
        summary_doc.save(summary_path)

        return RedirectResponse(url=f"/download/{summary_filename}", status_code=303)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/download/{filename}")
async def download_summary(filename: str):
    path = os.path.join(SUMMARY_FOLDER, filename)
    if os.path.exists(path):
        return FileResponse(path, filename=filename)
    else:
        raise HTTPException(status_code=404, detail="Summary file not found")

@app.exception_handler(404)
async def not_found_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

@app.exception_handler(500)
async def server_error_exception_handler(request: Request, exc: HTTPException):
    return templates.TemplateResponse("500.html", {"request": request}, status_code=500)
