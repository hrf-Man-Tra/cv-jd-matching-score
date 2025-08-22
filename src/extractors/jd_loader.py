import os
from ..utils.file_handler import ensure_directory_exists

class JDLoader:
    def load_pdf(self, file_path):
        """Load text file and extract content"""
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                print(f"File not found: {file_path}")
                return None
            
            # Read text file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            return content.strip()
        except Exception as e:
            print(f"Error loading file: {e}")
            return None
    
    def load_txt(self, txt_path):
        """Load text file - alias for load_pdf for backward compatibility"""
        return self.load_pdf(txt_path)
    
    def save_loaded_info(self, jd_info, output_path):
        """Save extracted information to txt file"""
        try:
            # Ensure output directory exists
            ensure_directory_exists(os.path.dirname(output_path))
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(jd_info)
            print(f"JD information saved to: {output_path}")
        except Exception as e:
            print(f"Error saving JD info: {e}")