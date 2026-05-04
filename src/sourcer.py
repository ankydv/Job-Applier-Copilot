import requests
from typing import List
from .models import SearchParameters, JobPosting

class JSearchSourcer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://jsearch.p.rapidapi.com/search"
        self.headers = {
            "Content-Type": "application/json",
            "x-rapidapi-host": "jsearch.p.rapidapi.com",
            "x-rapidapi-key": self.api_key
        }

    def _build_query_string(self, params: SearchParameters) -> str:
        """Combines parameters into a single string for JSearch."""
        # E.g., "Software Engineer Python in Chicago"
        title = params.job_titles[0] if params.job_titles else "Developer"
        location = params.locations[0] if params.locations else "USA"
        keywords = " ".join(params.keywords[:2]) # Use top 2 keywords
        
        return f"{title} {keywords} in {location}"

    def fetch_jobs(self, search_params: SearchParameters, num_pages: int = 1) -> List[JobPosting]:
        """Fetches jobs from RapidAPI and returns structured models."""
        query = self._build_query_string(search_params)
        print(f"Executing search with query: '{query}'")
        
        querystring = {
            "query": query,
            "page": "1",
            "num_pages": str(num_pages),
            "country": "us",
            "date_posted": "all" # Can be updated to 'today' or '3days'
        }

        try:
            response = requests.get(
                self.base_url, 
                headers=self.headers, 
                params=querystring
            )
            response.raise_for_status() # Raise exception for 4xx/5xx errors
            
            data = response.json().get("data", [])
            return self._parse_results(data)
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching jobs: {e}")
            return []

    def _parse_results(self, raw_data: list) -> List[JobPosting]:
        """Converts raw API dictionaries into JobPosting Pydantic models."""
        jobs = []
        for item in raw_data:
            # Safely extract data, providing fallbacks where necessary
            job = JobPosting(
                job_id=item.get("job_id", ""),
                employer_name=item.get("employer_name"),
                job_title=item.get("job_title", "Unknown Title"),
                job_city=item.get("job_city"),
                job_is_remote=item.get("job_is_remote", False),
                job_apply_link=item.get("job_apply_link"),
                job_description=item.get("job_description")
            )
            jobs.append(job)
        return jobs
