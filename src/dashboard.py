from fastapi import FastAPI, Depends, Request
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
import os

from .database import SessionLocal, DBJobPosting

app = FastAPI(title="Job Co-Pilot Dashboard")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    jobs = db.query(DBJobPosting).order_by(DBJobPosting.id.desc()).all()
    
    html_content = """
    <html>
        <head>
            <title>Job Application Co-Pilot Dashboard</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 40px; background-color: #f9f9f9;}
                .container { max-width: 1200px; margin: auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
                table { border-collapse: collapse; width: 100%; margin-top: 20px; }
                th, td { border: 1px solid #eee; padding: 12px; text-align: left; }
                th { background-color: #f2f2f2; }
                .status-notified { font-weight: bold; color: #2ecc71; }
                .status-rejected { color: #e74c3c; }
                .status-matched { color: #f39c12; }
                a { color: #3498db; text-decoration: none; }
                a:hover { text-decoration: underline; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Your Job Dashboard</h1>
                <table>
                    <tr>
                        <th>Company</th>
                        <th>Title</th>
                        <th>Match Score</th>
                        <th>Status</th>
                        <th>Action</th>
                    </tr>
    """
    
    for job in jobs:
        status_class = ""
        if job.status == "NOTIFIED": status_class = "status-notified"
        elif job.status == "REJECTED": status_class = "status-rejected"
        elif job.status == "MATCHED": status_class = "status-matched"
        
        cv_link = f"<a href='/download/{job.id}'>Download CV</a>" if job.tailored_cv_path else "-"
        apply_link = f"<a href='{job.job_apply_link}' target='_blank'>Apply Here</a>" if job.job_apply_link else "-"
        
        html_content += f"""
                    <tr>
                        <td>{job.employer_name}</td>
                        <td>{job.job_title}</td>
                        <td>{job.match_score if job.match_score else '-'}</td>
                        <td class='{status_class}'>{job.status}</td>
                        <td>{cv_link} | {apply_link}</td>
                    </tr>
        """
        
    html_content += """
                </table>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.get("/download/{job_id}")
def download_cv(job_id: int, db: Session = Depends(get_db)):
    job = db.query(DBJobPosting).filter(DBJobPosting.id == job_id).first()
    if job and job.tailored_cv_path and os.path.exists(job.tailored_cv_path):
        return FileResponse(job.tailored_cv_path, filename=os.path.basename(job.tailored_cv_path))
    return {"error": "File not found"}
