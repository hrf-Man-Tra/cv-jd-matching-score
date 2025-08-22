from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import tempfile
import json
from typing import Dict, Any
from src.extractors.cv_extractor import CVExtractor
from src.extractors.jd_loader import JDLoader
from src.matching.matching_engine import MatchingCV

app = FastAPI(
    title="CV-JD Matching API",
    description="API for matching CV with Job Descriptions",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize components
cv_extractor = CVExtractor()
jd_loader = JDLoader()
matching_cv = MatchingCV()

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "CV-JD Matching API is running!"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "cv-jd-matching-api"}

@app.post("/extract-cv")
async def extract_cv(cv_file: UploadFile = File(...)):
    """
    Extract structured information from CV PDF file
    """
    # Validate file type
    if not cv_file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported for CV")
    
    try:
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
            content = await cv_file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Process CV
        cv_info = cv_extractor.process_cv(temp_file_path)
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        if cv_info:
            return JSONResponse(content={
                "status": "success",
                "filename": cv_file.filename,
                "extracted_info": cv_info
            })
        else:
            raise HTTPException(status_code=500, detail="Failed to extract CV information")
            
    except Exception as e:
        # Clean up temporary file if it exists
        if 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Error processing CV: {str(e)}")

@app.post("/load-jd")
async def load_jd(jd_file: UploadFile = File(...)):
    """
    Load Job Description from text file
    """
    # Validate file type
    if not jd_file.filename.lower().endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only TXT files are supported for JD")
    
    try:
        # Read file content
        content = await jd_file.read()
        jd_text = content.decode('utf-8')
        
        if jd_text.strip():
            return JSONResponse(content={
                "status": "success",
                "filename": jd_file.filename,
                "jd_text": jd_text.strip()
            })
        else:
            raise HTTPException(status_code=400, detail="JD file is empty")
            
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Unable to decode file. Please ensure it's a valid UTF-8 text file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading JD: {str(e)}")

@app.post("/match-cv-jd")
async def match_cv_jd(
    cv_file: UploadFile = File(...),
    jd_file: UploadFile = File(...)
):
    """
    Upload CV (PDF) and JD (TXT) files to get matching score
    """
    # Validate file types
    if not cv_file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="CV file must be PDF format")
    
    if not jd_file.filename.lower().endswith('.txt'):
        raise HTTPException(status_code=400, detail="JD file must be TXT format")
    
    temp_cv_path = None
    temp_jd_path = None
    
    try:
        # Process CV file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_cv:
            cv_content = await cv_file.read()
            temp_cv.write(cv_content)
            temp_cv_path = temp_cv.name
        
        # Process JD file
        jd_content = await jd_file.read()
        jd_text = jd_content.decode('utf-8')
        
        # Extract CV information
        cv_info = cv_extractor.process_cv(temp_cv_path)
        if not cv_info:
            raise HTTPException(status_code=500, detail="Failed to extract CV information")
        
        # Calculate matching score
        matching_result = matching_cv.calculate_matching_score(cv_info, jd_text)
        if not matching_result:
            raise HTTPException(status_code=500, detail="Failed to calculate matching score")
        
        # Add file information to result
        matching_result['cv_filename'] = cv_file.filename
        matching_result['jd_filename'] = jd_file.filename
        
        return JSONResponse(content={
            "status": "success",
            "cv_filename": cv_file.filename,
            "jd_filename": jd_file.filename,
            "extracted_cv_info": cv_info,
            "jd_text": jd_text[:500] + "..." if len(jd_text) > 500 else jd_text,  # Truncate for response
            "matching_result": matching_result
        })
        
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="Unable to decode JD file. Please ensure it's a valid UTF-8 text file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing files: {str(e)}")
    finally:
        # Clean up temporary files
        if temp_cv_path and os.path.exists(temp_cv_path):
            try:
                os.unlink(temp_cv_path)
            except:
                pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)