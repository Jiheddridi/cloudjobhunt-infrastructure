"""
CloudJobHunt Base Scraper Class
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from app.schemas.job import JobCreate


class BaseScraper(ABC):
    """Base class for job scrapers"""
    
    def __init__(self):
        self.name = "base"
        self.source = "base"
    
    @abstractmethod
    def scrape_jobs(self, **kwargs) -> List[JobCreate]:
        """Scrape jobs from source"""
        pass
    
    @abstractmethod
    def search_jobs(self, query: str, **kwargs) -> List[JobCreate]:
        """Search jobs by query"""
        pass
    
    def validate_job_data(self, job_data: dict) -> Optional[JobCreate]:
        """Validate job data before creating"""
        try:
            return JobCreate(**job_data)
        except Exception as e:
            print(f"Invalid job data: {e}")
            return None
    
    def close(self):
        """Cleanup resources"""
        pass
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
