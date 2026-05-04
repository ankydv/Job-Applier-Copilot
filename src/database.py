from sqlalchemy import create_engine, Column, Integer, String, Boolean, Text
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./job_copilot.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class DBJobPosting(Base):
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(String, unique=True, index=True)
    employer_name = Column(String)
    job_title = Column(String)
    job_city = Column(String, nullable=True)
    job_is_remote = Column(Boolean, default=False)
    job_apply_link = Column(String, nullable=True)
    job_description = Column(Text, nullable=True)
    
    # Status can be: NEW, MATCHED, REJECTED, READY_FOR_REVIEW, NOTIFIED, APPLIED
    status = Column(String, default="NEW")
    match_score = Column(Integer, nullable=True)
    tailored_cv_path = Column(String, nullable=True)

class DBUserProfile(Base):
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    raw_cv_text = Column(Text)

# Create tables
Base.metadata.create_all(bind=engine)
