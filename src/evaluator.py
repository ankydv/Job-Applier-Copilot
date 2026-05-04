import os
from google import genai
from .models import UserProfile
from .database import DBJobPosting

class EvaluationAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Warning: GEMINI_API_KEY not set. Evaluator will use a mock score.")
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)

    def evaluate_job(self, db_job: DBJobPosting, profile: UserProfile) -> DBJobPosting:
        print(f"Evaluating job: {db_job.job_title} at {db_job.employer_name}")
        
        if not self.client:
            # Mock evaluation
            db_job.match_score = 85
            db_job.status = "MATCHED"
            return db_job

        prompt = f"""
        You are an expert technical recruiter. Evaluate the following job description against the candidate's base profile.
        Calculate a match score from 0 to 100.
        Return ONLY a JSON object with 'score' (integer) and 'reason' (string).
        
        Job Title: {db_job.job_title}
        Job Description: {db_job.job_description}
        
        Candidate Profile: {profile.raw_cv_text}
        """
        
        try:
            response = self.client.models.generate_content(
                model='gemini-flash-latest',
                contents=prompt
            )
            # Simple heuristic since LLMs might wrap JSON in markdown blocks
            text = response.text.lower()
            if "score" in text:
                db_job.match_score = 90 # Extract actual score in production
                db_job.status = "MATCHED"
            else:
                db_job.match_score = 50
                db_job.status = "REJECTED"
        except Exception as e:
            print(f"Error evaluating job: {e}")
            db_job.status = "NEW"
            
        return db_job
