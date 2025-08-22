import os
import json
import openai
from dotenv import load_dotenv
from ..utils.file_handler import ensure_directory_exists
from ..utils import prompt

# Load environment variables
load_dotenv()

class MatchingCV:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Template để matching CV với JD
        self.matching_template = prompt.MATCHING_PROMPT

    def calculate_matching_score(self, cv_json, jd_text):
        """Tính toán matching score giữa CV và JD"""
        try:
            # Format prompt với CV JSON và JD text
            prompt = self.matching_template.format(
                CV_JSON_HERE=json.dumps(cv_json, ensure_ascii=False),
                JD_TEXT_HERE=jd_text
            )
            
            # Generate response using OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are an expert recruiter AI. Always respond with valid JSON only. No additional text or formatting."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=3000
            )
            
            # Extract text from response
            result_text = response.choices[0].message.content
            
            # Clean up the response text
            if result_text.startswith('```json'):
                result_text = result_text.replace('```json', '').replace('```', '').strip()
            elif result_text.startswith('```'):
                result_text = result_text.replace('```', '').strip()
            
            # Parse JSON response
            matching_result = json.loads(result_text)
            return matching_result
            
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON: {e}")
            print(f"Raw response: {result_text}")
            return None
        except Exception as e:
            print(f"Error calculating matching score: {e}")
            return None

    def process_matching(self, cv_json_path, jd_text_path):
        """Process matching từ file CV JSON và JD text"""
        try:
            # Load CV JSON
            with open(cv_json_path, "r", encoding="utf-8") as f:
                cv_json = json.load(f)
            
            # Load JD text
            with open(jd_text_path, "r", encoding="utf-8") as f:
                jd_text = f.read()
            
            print("Files loaded successfully")
            print(f"CV keys: {list(cv_json.keys())}")
            print(f"JD text length: {len(jd_text)} characters")
            
            # Calculate matching score
            matching_result = self.calculate_matching_score(cv_json, jd_text)
            
            if matching_result:
                print("Matching score calculated successfully")
                return matching_result
            else:
                print("Failed to calculate matching score")
                return None
                
        except FileNotFoundError as e:
            print(f"File not found: {e}")
            return None
        except Exception as e:
            print(f"Error processing matching: {e}")
            return None

    def save_matching_result(self, matching_result, output_path):
        """Save matching result to JSON file"""
        try:
            # Ensure output directory exists
            ensure_directory_exists(os.path.dirname(output_path))
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(matching_result, f, ensure_ascii=False, indent=2)
            print(f"Matching result saved to: {output_path}")
        except Exception as e:
            print(f"Error saving matching result: {e}")

    def display_matching_summary(self, matching_result):
        """Display a formatted summary of matching results"""
        if not matching_result:
            print("No matching result to display")
            return
        
        print("\n" + "="*60)
        print("            CV-JD MATCHING SUMMARY")
        print("="*60)
        
        scores = matching_result.get("scores", {})
        
        # Define weights for calculation verification
        weights = {
            "exp_years": 0.20,
            "prof_skill_advanced": 0.18,
            "soft_skill": 0.14,
            "education": 0.13,
            "prof_skill_basic": 0.10,
            "achievements": 0.08,
            "relevant_projects": 0.07,
            "certs": 0.05,
            "language": 0.04,
            "activities": 0.01
        }
        
        print(f"📊 FINAL MATCHING SCORE: {matching_result.get('final_matching_score', 0):.1f}/100")
        print("\n🔍 DETAILED BREAKDOWN:")
        print("-" * 60)
        
        for feature, weight in weights.items():
            if feature in scores:
                score_info = scores[feature]
                score = score_info.get("score", 0)
                justification = score_info.get("justification", "No justification provided")
                
                print(f"• {feature.replace('_', ' ').title()}: {score}/100 (Weight: {weight*100}%)")
                print(f"  └─ {justification}")
                print()