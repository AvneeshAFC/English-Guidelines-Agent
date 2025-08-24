from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
import uvicorn
from Config import constants as const
from Utility.utils import parse_pdf, parse_docx
from LLM.agent import assessor_agent
import os

app = FastAPI(title="AI Document Assessor API")

# Create a directory for uploads if it doesn't exist
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/assess/")
async def assess_document_endpoint(
    file: UploadFile = File(...),
    guidelines: str = Form(...)
):
    """
    API endpoint to assess a document.
    Accepts a file (PDF or Word) and guidelines.
    """
    try:
        file_content = await file.read()
        filename = file.filename
        
        if filename.endswith(".pdf"):
            doc_text = parse_pdf(file_content)
        elif filename.endswith(".docx"):
            doc_text = parse_docx(file_content)
        else:
            raise HTTPException(status_code=const.STATUS_CODE["BAD_REQUEST"], detail="Unsupported file format. Please upload a PDF or DOCX file.")

        if not doc_text:
            raise HTTPException(status_code=const.STATUS_CODE["BAD_REQUEST"], detail="Could not extract text from the document.")

        result = assessor_agent.run_assessment(doc_text, guidelines)

        if result.get("error"):
            raise HTTPException(status_code=const.STATUS_CODE["INTERNAL_SERVER_ERROR"], detail=result["error"])

        return JSONResponse(content={"report": result["assessment_report"]})

    except Exception as e:
        return JSONResponse(status_code=const.STATUS_CODE["INTERNAL_SERVER_ERROR"], content={"message": f"An error occurred: {str(e)}"})

@app.post("/modify/")
async def modify_document_endpoint(
    file: UploadFile = File(...),
    guidelines: str = Form(...),
    request: str = Form("Please fix all issues found.")
):
    """
    API endpoint to modify a document.
    Accepts a file, guidelines, and a modification request.
    """
    try:
        file_content = await file.read()
        filename = file.filename
        
        if filename.endswith(".pdf"):
            doc_text = parse_pdf(file_content)
        elif filename.endswith(".docx"):
            doc_text = parse_docx(file_content)
        else:
            raise HTTPException(status_code=const.STATUS_CODE["BAD_REQUEST"], detail="Unsupported file format.")

        if not doc_text:
            raise HTTPException(status_code=const.STATUS_CODE["BAD_REQUEST"], detail="Could not extract text from the document.")

        result = assessor_agent.run_modification(doc_text, guidelines, request)

        if result.get("error"):
            raise HTTPException(status_code=const.STATUS_CODE["INTERNAL_SERVER_ERROR"], detail=result["error"])
        
        modified_text = result["modified_document"]
        
        # Return as plain text, can be extended to return a new docx/pdf
        return PlainTextResponse(content=modified_text)

    except Exception as e:
        return JSONResponse(status_code=const.STATUS_CODE["INTERNAL_SERVER_ERROR"], content={"message": f"An error occurred: {str(e)}"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
