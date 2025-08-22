import os

class Config:
    """Configuration settings for the CV-JD Matching Score application."""
    
    # Load environment variables
    API_KEY = os.getenv("API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    
    # File paths
    INPUT_CVS_PATH = os.path.join("data", "input", "cvs")
    INPUT_JD_PATH = os.path.join("data", "input", "job_descriptions")
    OUTPUT_EXTRACTED_INFO_PATH = os.path.join("data", "output", "extracted_info")
    OUTPUT_MATCHING_RESULTS_PATH = os.path.join("data", "output", "matching_results")