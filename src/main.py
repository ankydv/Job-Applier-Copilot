import os
from dotenv import load_dotenv
from .models import UserProfile
from .analyzer import ProfileAnalyzer
from .sourcer import JSearchSourcer
from .database import SessionLocal, DBJobPosting
from .evaluator import EvaluationAgent
from .tailorer import TailoringAgent
from .notifier import NotificationAgent

def main():
    # 0. Setup Configuration
    load_dotenv()
    api_key = os.getenv("RAPIDAPI_KEY", "example-api-key")
    db = SessionLocal()
    
    # 1. Initialize user profile
    my_profile = UserProfile(
        name="Alex Smith",
        raw_cv_text="Experienced Software Engineer with 5 years in Python, FastAPI, and APIs..."
    )
    
    # 2. Step 1: Analyze Profile
    analyzer = ProfileAnalyzer()
    search_params = analyzer.extract_search_parameters(my_profile)
    
    # 3. Step 2: Source Jobs
    sourcer = JSearchSourcer(api_key=api_key)
    jobs = sourcer.fetch_jobs(search_params)
    
    print(f"\\nFound {len(jobs)} jobs for {my_profile.name}")
    
    # Save to database if not exists
    for job in jobs:
        existing = db.query(DBJobPosting).filter(DBJobPosting.job_id == job.job_id).first()
        if not existing:
            new_db_job = DBJobPosting(
                job_id=job.job_id,
                employer_name=job.employer_name,
                job_title=job.job_title,
                job_city=job.job_city,
                job_is_remote=job.job_is_remote,
                job_apply_link=job.job_apply_link,
                job_description=job.job_description,
                status="NEW"
            )
            db.add(new_db_job)
    db.commit()

    # 4. Pipeline Execution
    evaluator = EvaluationAgent()
    tailorer = TailoringAgent()
    notifier = NotificationAgent()
    
    # Process all NEW jobs
    new_jobs = db.query(DBJobPosting).filter(DBJobPosting.status == "NEW").all()
    for db_job in new_jobs:
        evaluated_job = evaluator.evaluate_job(db_job, my_profile)
        db.commit()
        
    # Process all MATCHED jobs
    matched_jobs = db.query(DBJobPosting).filter(DBJobPosting.status == "MATCHED").all()
    for db_job in matched_jobs:
        tailored_job = tailorer.generate_tailored_cv(db_job, my_profile)
        db.commit()
        
    # Process all READY_FOR_REVIEW jobs
    ready_jobs = db.query(DBJobPosting).filter(DBJobPosting.status == "READY_FOR_REVIEW").all()
    for db_job in ready_jobs:
        notified_job = notifier.notify_user(db_job)
        db.commit()

    db.close()
    print("\\nPipeline complete. Run `uvicorn src.dashboard:app --reload` to view the dashboard.")

if __name__ == "__main__":
    main()
