"""
Script to create sample JD files for testing
"""
import os

def create_sample_jd_text(filename, job_title, content):
    """Create a sample JD text file"""
    filepath = os.path.join("data/input/JD", filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(f"{job_title}\n")
        f.write("=" * len(job_title) + "\n\n")
        
        for item in content:
            # Remove HTML tags for text file
            clean_item = item.replace('<b>', '').replace('</b>', '').replace('•', '-')
            f.write(f"{clean_item}\n")
        f.write("\n")
    
    print(f"Created {filepath}")

def create_sample_jds():
    """Create sample JD files"""
    
    # Ensure JD directory exists
    os.makedirs("data/input/JD", exist_ok=True)
    
    # Sample JD 1 - Software Engineer
    jd1_content = [
        "<b>Job Description: Software Engineer</b>",
        "We are looking for a skilled Software Engineer to join our development team.",
        "<b>Requirements:</b>",
        "• Bachelor's degree in Computer Science or related field",
        "• 3+ years of experience in software development",
        "• Proficiency in Python, Java, or C++",
        "• Experience with web frameworks (Django, Flask, Spring)",
        "• Knowledge of databases (SQL, NoSQL)",
        "• Experience with version control (Git)",
        "• Strong problem-solving skills",
        "<b>Responsibilities:</b>",
        "• Develop and maintain software applications",
        "• Collaborate with cross-functional teams",
        "• Write clean, maintainable code",
        "• Participate in code reviews",
        "• Debug and resolve technical issues"
    ]
    
    # Sample JD 2 - Data Scientist
    jd2_content = [
        "<b>Job Description: Data Scientist</b>",
        "We are seeking a talented Data Scientist to analyze complex data and provide insights.",
        "<b>Requirements:</b>",
        "• Master's degree in Data Science, Statistics, or related field",
        "• 2+ years of experience in data analysis",
        "• Proficiency in Python and R",
        "• Experience with machine learning libraries (scikit-learn, TensorFlow, PyTorch)",
        "• Knowledge of SQL and data visualization tools",
        "• Experience with statistical analysis",
        "• Strong analytical and communication skills",
        "<b>Responsibilities:</b>",
        "• Analyze large datasets to identify trends and patterns",
        "• Develop predictive models and algorithms",
        "• Create data visualizations and reports",
        "• Collaborate with business stakeholders",
        "• Present findings to management"
    ]
    
    # Sample JD 3 - Product Manager
    jd3_content = [
        "<b>Job Description: Product Manager</b>",
        "We are looking for an experienced Product Manager to lead our product development.",
        "<b>Requirements:</b>",
        "• Bachelor's degree in Business, Engineering, or related field",
        "• 5+ years of product management experience",
        "• Experience with Agile/Scrum methodologies",
        "• Strong analytical and problem-solving skills",
        "• Excellent communication and leadership abilities",
        "• Experience with product analytics tools",
        "• Understanding of user experience (UX) principles",
        "<b>Responsibilities:</b>",
        "• Define product strategy and roadmap",
        "• Manage product lifecycle from conception to launch",
        "• Collaborate with engineering, design, and marketing teams",
        "• Conduct market research and competitive analysis",
        "• Gather and prioritize product requirements"
    ]
    
    try:
        create_sample_jd_text("software_engineer.txt", "Software Engineer", jd1_content)
        create_sample_jd_text("data_scientist.txt", "Data Scientist", jd2_content)
        create_sample_jd_text("product_manager.txt", "Product Manager", jd3_content)
        print("All sample JD files created successfully!")
        
    except Exception as e:
        print(f"Error creating files: {e}")

if __name__ == "__main__":
    create_sample_jds()
