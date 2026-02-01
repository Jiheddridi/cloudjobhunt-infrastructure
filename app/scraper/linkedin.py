"""
CloudJobHunt LinkedIn Scraper
"""
from typing import List, Optional
from datetime import datetime
import requests
from bs4 import BeautifulSoup

from app.config import settings
from app.scraper.base import BaseScraper
from app.schemas.job import JobCreate


class LinkedInScraper(BaseScraper):
    """LinkedIn job scraper"""
    
    def __init__(self):
        super().__init__()
        self.name = "linkedin"
        self.source = "linkedin"
        self.base_url = "https://www.linkedin.com"
        self.session = requests.Session()
    
    def _get_headers(self) -> dict:
        """Get headers for LinkedIn requests"""
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
    
    def scrape_jobs(self, location: str = None, keywords: str = None, **kwargs) -> List[JobCreate]:
        """Scrape jobs from LinkedIn"""
        jobs = []
        
        # Note: LinkedIn requires authentication for most job listings
        # This is a simplified example - in production, you'd need proper auth
        try:
            search_url = f"{self.base_url}/jobs/search/"
            params = {}
            if keywords:
                params["keywords"] = keywords
            if location:
                params["location"] = location
            
            response = self.session.get(
                search_url,
                params=params,
                headers=self._get_headers(),
                timeout=30,
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")
                jobs = self._parse_jobs(soup)
            
        except Exception as e:
            print(f"LinkedIn scraper error: {e}")
        
        return jobs
    
    def search_jobs(self, query: str, **kwargs) -> List[JobCreate]:
        """Search jobs on LinkedIn"""
        return self.scrape_jobs(keywords=query, **kwargs)
    
    def _parse_jobs(self, soup: BeautifulSoup) -> List[JobCreate]:
        """Parse job listings from LinkedIn HTML"""
        jobs = []
        
        # This is a placeholder - LinkedIn's structure changes frequently
        # and requires authentication
        job_cards = soup.find_all("div", class_="job-card-container")
        
        for card in job_cards:
            try:
                job_data = self._extract_job_data(card)
                if job_data:
                    jobs.append(job_data)
            except Exception as e:
                print(f"Error parsing job card: {e}")
                continue
        
        return jobs
    
    def _extract_job_data(self, card) -> Optional[JobCreate]:
        """Extract job data from a job card"""
        try:
            title_elem = card.find("h3", class_="job-card-title")
            company_elem = card.find("h4", class_="job-card-company")
            location_elem = card.find("span", class_="job-card-location")
            link_elem = card.find("a", class_="job-card-container__link")
            
            title = title_elem.text.strip() if title_elem else None
            company = company_elem.text.strip() if company_elem else None
            location = location_elem.text.strip() if location_elem else None
            url = f"{self.base_url}{link_elem.get('href')}" if link_elem else None
            
            if not title or not company:
                return None
            
            return JobCreate(
                title=title,
                company=company,
                location=location,
                url=url,
                source=self.source,
                posted_at=datetime.utcnow(),
            )
        
        except Exception as e:
            print(f"Error extracting job data: {e}")
            return None
    
    def close(self):
        """Close the session"""
        if self.session:
            self.session.close()
