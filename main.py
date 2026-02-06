from fastapi import FastAPI, UploadFile
import shutil
import os

# Import all functions directly
from extractor import read_document, extract_fields_from_text
from router import route_claim

app = FastAPI()

@app.post("/process-claim/")
async def process_claim(file: UploadFile):
    file_path = f"temp_{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        text = read_document(file_path)
        extracted = extract_fields_from_text(text)
        missing, route, reason = route_claim(extracted)
        
        return {
            "extractedFields": extracted,
            "missingFields": missing,
            "recommendedRoute": route,
            "reasoning": reason
        }
    finally:
        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)