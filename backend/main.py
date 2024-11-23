from fastapi import FastAPI, File, UploadFile, HTTPException, Depends
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import os
import secrets

app = FastAPI()

# Add Basic Auth
security = HTTPBasic()
USERNAME = "himanshu"
PASSWORD = "password"

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials.username

# Convert DOCX to PDF function
def convert_docx_to_pdf(docx_file):
    """Convert a DOCX file to a PDF."""
    doc = Document(docx_file)
    pdf_buffer = BytesIO()

    # Page and margin settings
    page_width, page_height = letter
    margin = 72  # 1 inch

    pdf = canvas.Canvas(pdf_buffer, pagesize=(page_width, page_height))
    x_start = margin
    y_start = page_height - margin
    current_y = y_start

    pdf.setFont("Times-Roman", 12)
    max_width = page_width - (2 * margin)

    for para in doc.paragraphs:
        text = para.text.strip()
        if text:
            lines = text.split("\n")
            for line in lines:
                pdf.drawString(x_start, current_y, line[:90])  # Basic text wrapping
                current_y -= 15
                if current_y < margin:
                    pdf.showPage()
                    current_y = page_height - margin
                    pdf.setFont("Times-Roman", 12)
    pdf.save()
    pdf_buffer.seek(0)
    return pdf_buffer

# Convert endpoint with authentication
@app.post("/convert")
async def convert_to_pdf(file: UploadFile = File(...), username: str = Depends(authenticate)):
    if not file.filename.endswith(".docx"):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a .docx file.")
    
    try:
        # Convert DOCX to PDF
        pdf_buffer = convert_docx_to_pdf(file.file)

        # Save the PDF to a temporary location
        output_filename = f"{os.path.splitext(file.filename)[0]}_converted.pdf"
        with open(output_filename, "wb") as f:
            f.write(pdf_buffer.read())
        
        # Return the PDF as a response
        return FileResponse(output_filename, filename=output_filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
