import os
import json
import openai
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from ..utils.file_handler import ensure_directory_exists
from ..utils import prompt

# Load environment variables
load_dotenv()

class CVExtractor:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Template để extract thông tin CV
        self.extraction_template = prompt.EXTRACTOR_PROMPT

    def load_pdf(self, pdf_path):
        """Load PDF và extract text"""
        try:
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            
            # Combine all pages
            full_text = ""
            for doc in documents:
                full_text += doc.page_content + "\n"
            
            return full_text
        except Exception as e:
            print(f"Error loading PDF: {e}")
            return None

    def extract_cv_info(self, cv_text):
        """Extract thông tin quan trọng từ CV text"""
        try:
            # Format prompt với CV text
            prompt = self.extraction_template.format(cv_text=cv_text)
            
            # Generate response using OpenAI
            response = self.client.chat.completions.create(
                model= os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                messages=[
                    {"role": "system", "content": "You are an expert HR data structuring bot. Always respond with valid JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=2000
            )
            
            # Extract text from response
            result_text = response.choices[0].message.content
            
            # Clean up the response text (remove any markdown formatting)
            if result_text.startswith('```json'):
                result_text = result_text.replace('```json', '').replace('```', '').strip()
            elif result_text.startswith('```'):
                result_text = result_text.replace('```', '').strip()
            
            # Parse JSON response
            cv_info = json.loads(result_text)
            return cv_info
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print(f"Raw response: {result_text}")
            return None
        except Exception as e:
            print(f"Error extracting CV info: {e}")
            return None

    def process_cv(self, pdf_path):
        """Process CV từ PDF file"""
        print(f"Processing CV: {pdf_path}")
        
        # Load PDF
        cv_text = self.load_pdf(pdf_path)
        if not cv_text:
            return None
        
        print("PDF loaded successfully")
        print(f"Text length: {len(cv_text)} characters")
        
        # Extract information
        cv_info = self.extract_cv_info(cv_text)
        if not cv_info:
            return None
        
        print("CV information extracted successfully")
        return cv_info

    def save_extracted_info(self, cv_info, output_path):
        """Save extracted information to JSON file"""
        try:
            # Ensure output directory exists
            ensure_directory_exists(os.path.dirname(output_path))
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(cv_info, f, ensure_ascii=False, indent=2)
            print(f"CV information saved to: {output_path}")
        except Exception as e:
            print(f"Error saving CV info: {e}")