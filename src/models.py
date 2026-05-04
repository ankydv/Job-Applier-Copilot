from pydantic import BaseModel, Field
from typing import List, Optional

class UserProfile(BaseModel):
    """Represents the user's base information."""
    name: str
    raw_cv_text: str

class SearchParameters(BaseModel):
    """The targeted queries extracted from a user's CV."""
    job_titles: List[str] = Field(description="Target job titles (e.g., 'Backend Developer')")
    locations: List[str] = Field(description="Target locations or 'Remote'")
    keywords: List[str] = Field(description="Key skills to include in the search")

class JobPosting(BaseModel):
    """A standardized representation of a job posting from the API."""
    job_id: str
    employer_name: Optional[str] = "Unknown Company"
    job_title: str
    job_city: Optional[str] = None
    job_is_remote: bool = False
    job_apply_link: Optional[str] = None
    job_description: Optional[str] = None
