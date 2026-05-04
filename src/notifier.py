from .database import DBJobPosting

class NotificationAgent:
    def notify_user(self, db_job: DBJobPosting):
        print(f"\\n[EMAIL SENT] To: user@example.com")
        print(f"Subject: New Tailored CV Ready for {db_job.job_title} at {db_job.employer_name}")
        print(f"Body: Hi! We found a great job for you. Check your dashboard.")
        print(f"Job Link: {db_job.job_apply_link}")
        print(f"CV Download: {db_job.tailored_cv_path}\\n")
        
        db_job.status = "NOTIFIED"
        return db_job
