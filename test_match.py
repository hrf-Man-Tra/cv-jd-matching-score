from src.extractors.cv_extractor import CVExtractor
from src.extractors.jd_loader import JDLoader
from src.matching.matching_engine import MatchingCV
from src.utils.file_handler import ensure_directory_exists
import os
import glob

def get_cv_files(cv_folder_path):
    """Get all PDF files in the CV folder"""
    cv_files = glob.glob(os.path.join(cv_folder_path, "*.pdf"))
    return [os.path.basename(cv_file) for cv_file in cv_files]

def get_jd_files(jd_folder_path):
    """Get all TXT files in the JD folder"""
    jd_files = glob.glob(os.path.join(jd_folder_path, "*.txt"))
    return [os.path.basename(jd_file) for jd_file in jd_files]

def get_filename_without_extension(filepath):
    """Get filename without extension"""
    return os.path.splitext(os.path.basename(filepath))[0]
  
def main():
    # Initialize components
    cv_extractor = CVExtractor()
    jd_loader = JDLoader()
    matching_cv = MatchingCV()
    
    # Define folder paths
    cv_folder = "data/input/CV"
    jd_folder = "data/input/JD"
    extracted_info_folder = "data/output/extracted_info"
    matching_results_folder = "data/output/matching_results"
    
    # Ensure output directories exist
    ensure_directory_exists(extracted_info_folder)
    ensure_directory_exists(matching_results_folder)
    
    print("Starting CV-JD Matching Process...")
    print("=" * 60)
    
    # Get all CV and JD files
    cv_files = get_cv_files(cv_folder)
    jd_files = get_jd_files(jd_folder)
    
    if not cv_files:
        print("❌ No CV files found in the CV folder.")
        return
    
    if not jd_files:
        print("❌ No JD files found in the JD folder.")
        return
    
    print(f"Found {len(cv_files)} CV files and {len(jd_files)} JD files")
    print(f"CV files: {cv_files}")
    print(f"JD files: {jd_files}")
    print("=" * 60)
    
    # Dictionary to store extracted information to avoid re-processing
    extracted_cvs = {}
    extracted_jds = {}
    
    # Process all CVs
    print("\n1. Processing all CVs...")
    for cv_file in cv_files:
        cv_path = os.path.join(cv_folder, cv_file)
        cv_name = get_filename_without_extension(cv_file)
        extracted_cv_path = os.path.join(extracted_info_folder, f"extracted_{cv_name}.json")
        
        print(f"   Processing CV: {cv_file}...")
        cv_info = cv_extractor.process_cv(cv_path)
        if cv_info:
            cv_extractor.save_extracted_info(cv_info, extracted_cv_path)
            extracted_cvs[cv_name] = extracted_cv_path
            print(f"   ✅ CV {cv_file} processed successfully")
        else:
            print(f"   ❌ Failed to extract CV {cv_file}")
    
    # Process all JDs
    print("\n2. Processing all Job Descriptions...")
    for jd_file in jd_files:
        jd_path = os.path.join(jd_folder, jd_file)
        jd_name = get_filename_without_extension(jd_file)
        extracted_jd_path = os.path.join(extracted_info_folder, f"extracted_{jd_name}.txt")
        
        print(f"   Processing JD: {jd_file}...")
        jd_info = jd_loader.load_pdf(jd_path)
        if jd_info:
            jd_loader.save_loaded_info(jd_info, extracted_jd_path)
            extracted_jds[jd_name] = extracted_jd_path
            print(f"   ✅ JD {jd_file} processed successfully")
        else:
            print(f"   ❌ Failed to extract JD {jd_file}")
    
    # Perform matching for each CV-JD pair
    print("\n3. Calculating Matching Scores for all CV-JD pairs...")
    total_pairs = len(extracted_cvs) * len(extracted_jds)
    current_pair = 0
    
    matching_results_summary = []
    
    for cv_name, cv_json_path in extracted_cvs.items():
        for jd_name, jd_text_path in extracted_jds.items():
            current_pair += 1
            print(f"   [{current_pair}/{total_pairs}] Matching {cv_name} with {jd_name}...")
            
            # Create result filename: CVname_JDname.json
            result_filename = f"{cv_name}_{jd_name}.json"
            matching_result_path = os.path.join(matching_results_folder, result_filename)
            
            matching_result = matching_cv.process_matching(
                cv_json_path=cv_json_path,
                jd_text_path=jd_text_path
            )
            
            if matching_result:
                # Add CV and JD names to the result for easier identification
                matching_result['cv_name'] = cv_name
                matching_result['jd_name'] = jd_name
                matching_result['cv_file'] = f"{cv_name}.pdf"
                matching_result['jd_file'] = f"{jd_name}.pdf"
                
                matching_cv.save_matching_result(matching_result, matching_result_path)
                print(f"   ✅ Matching completed - Score: {matching_result.get('overall_score', 'N/A')}%")
                
                # Store summary for final display
                matching_results_summary.append({
                    'cv_name': cv_name,
                    'jd_name': jd_name,
                    'score': matching_result.get('overall_score', 'N/A'),
                    'result_file': result_filename
                })
            else:
                print(f"   ❌ Failed to calculate matching score for {cv_name} and {jd_name}")
    
    # Display final summary
    print("\n" + "=" * 80)
    print("MATCHING RESULTS SUMMARY")
    print("=" * 80)
    if matching_results_summary:
        print(f"{'CV Name':<15} {'JD Name':<20} {'Score':<10} {'Result File'}")
        print("-" * 80)
        for result in matching_results_summary:
            print(f"{result['cv_name']:<15} {result['jd_name']:<20} {result['score']:<10} {result['result_file']}")
        
        print(f"\n✅ Successfully processed {len(matching_results_summary)} CV-JD pairs")
        print(f"📁 Results saved in: {matching_results_folder}")
    else:
        print("❌ No successful matches were completed")

if __name__ == "__main__":
    main()