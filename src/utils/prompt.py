# src/utils/prompt.py

# Prompts for Extractor
EXTRACTOR_PROMPT = """
### OVERALL CONTEXT
You are an expert HR data structuring bot. Your task is to analyze a comprehensive block of text containing multiple sections from a single resume and extract a full, structured JSON object with all required metrics.

### EVALUATION PRINCIPLES
- **Experience:** Specifying years of experience for each specific roles, jobs and areas. Don't need to specify the total years of experience.
- **Language:** All information about non-native language levels
- **Education:** All information about educational background, including degrees obtained and institutions attended.
- **Certs:** All certifications about courses like coursera, licenses, or professional qualifications.
- **Achievements:** All achievements, awards, or recognitions received.
- **Relevant Projects:** All projects that are relevant to the job position, including roles and contributions.
- **Activities:** All extracurricular activities or community involvement.

### TASK
Analyze the multi-part input text block below. Respond ONLY with a single, valid JSON object containing all the specified keys. If a section is empty or not applicable, return a default value of 0.

The required JSON output structure is:
{{
"exp": <text>,
"language": <text>,
"education": <text>,
"prof_skill_advanced": <text>,
"prof_skill_basic": <text>,
"soft_skill": <text>,
"certs": <text>,
"achievements": <text>,
"relevant_projects": <text>,
"activities": <text>
}}

### YOUR TASK
Input Text Block:
---BEGIN RESUME DATA---
{cv_text}
---END RESUME DATA---

Your JSON Output:
"""

# Prompts for Matching
MATCHING_PROMPT = """
You are an AI Recruiter Assistant.

Your task is to analyze how well a candidate CV matches a job description (JD) based on 10 key features.

Below is the candidate CV (in JSON format) and the JD (free text format). Your goal is to:
- Score each feature individually on a scale of 0–100
- Justify each score briefly (1–2 sentences)
- Calculate the final weighted matching score (0–100) based on the following weights:

Scoring weights:
- exp_years: 20%
- prof_skill_advanced: 18%
- soft_skill: 14%
- education: 13%
- prof_skill_basic: 10%
- achievements: 8%
- relevant_projects: 7%
- certs: 5%
- language: 4%
- activities: 1%

Scoring Guidelines:
- exp_years: Compare candidate's years of experience with JD requirements
- prof_skill_advanced: Match advanced technical skills mentioned in JD
- soft_skill: Evaluate communication, leadership, teamwork skills
- education: Compare degree level and field relevance
- prof_skill_basic: Match basic/fundamental skills required
- achievements: Assess awards, recognitions, notable accomplishments
- relevant_projects: Evaluate project experience relevance
- certs: Match certifications with job requirements
- language: Assess language proficiency requirements. If JD doesn't mention languages, give a default score of 100.
- activities: Consider extracurricular activities relevance

---
### 📄 CV (JSON format):
{CV_JSON_HERE}

---
### 📝 Job Description (JD):
{JD_TEXT_HERE}

---
### 🎯 Output ONLY valid JSON in this exact format:
{{
"scores": {{
    "exp_years": {{
    "score": 0,
    "justification": "Brief explanation here"
    }},
    "prof_skill_advanced": {{
    "score": 0,
    "justification": "Brief explanation here"
    }},
    "soft_skill": {{
    "score": 0,
    "justification": "Brief explanation here"
    }},
    "education": {{
    "score": 0,
    "justification": "Brief explanation here"
    }},
    "prof_skill_basic": {{
    "score": 0,
    "justification": "Brief explanation here"
    }},
    "achievements": {{
    "score": 0,
    "justification": "Brief explanation here"
    }},
    "relevant_projects": {{
    "score": 0,
    "justification": "Brief explanation here"
    }},
    "certs": {{
    "score": 0,
    "justification": "Brief explanation here"
    }},
    "language": {{
    "score": 0,
    "justification": "Brief explanation here"
    }},
    "activities": {{
    "score": 0,
    "justification": "Brief explanation here"
    }}
}},
"final_matching_score": 0.0
}}
"""

# Có thể bổ sung thêm các prompt khác nếu cần thiết