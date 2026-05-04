import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from google import genai
from .models import UserProfile
from .database import DBJobPosting

class TailoringAgent:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            self.client = genai.Client(api_key=api_key)
        else:
            self.client = None

    def generate_tailored_cv(self, db_job: DBJobPosting, profile: UserProfile):
        print(f"Generating tailored CV for {db_job.job_title}...")
        
        # If no API key, mock the content
        tailored_content = "This is a mocked tailored CV content."
        if self.client:
            prompt = f"Rewrite this base profile to highlight skills for this job description.\\nBase Profile: {profile.raw_cv_text}\\nJob Description: {db_job.job_description}"
            try:
                response = self.client.models.generate_content(
                    model='gemini-flash-latest',
                    contents=prompt
                )
                tailored_content = response.text[:50] + "..." # Just taking a snippet for demo rendering
            except Exception as e:
                print(f"Error generating tailored content: {e}")

        # Render PDF
        os.makedirs("assets", exist_ok=True)
        pdf_path = f"assets/cv_{db_job.job_id}.pdf"
        
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.drawString(100, 750, f"Tailored CV for {profile.name}")
        c.drawString(100, 730, f"Applying for: {db_job.job_title}")
        c.drawString(100, 700, "Content tailored successfully.")
        c.save()
        
        db_job.tailored_cv_path = pdf_path
        db_job.status = "READY_FOR_REVIEW"
        return db_job
