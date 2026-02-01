"""
CloudJobHunt API - Endpoints de recherche en temps réel (PUBLIC - sans auth)
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import logging

# Import scraper directly (standalone - no database dependency)
from app.scraper.aggregator import search_jobs_async

router = APIRouter()
logger = logging.getLogger(__name__)


# Handle CORS preflight requests
@router.options("/search")
async def handle_search_options():
    """Handle CORS preflight for search endpoint"""
    return {"status": "ok"}


class JobResponse(BaseModel):
    """Réponse pour une offre d'emploi"""
    title: str
    company: str
    location: str
    description: str
    url: str
    source: str
    posted_date: str
    job_type: str = ""
    salary: str = ""
    skills: List[str] = []
    days_ago: int = 0


class SearchRequest(BaseModel):
    """Requête de recherche"""
    query: str
    location: Optional[str] = ""
    job_type: Optional[str] = ""
    max_days_old: int = 5
    max_results: int = 20


class SearchResponse(BaseModel):
    """Réponse de recherche"""
    query: str
    location: str
    total_found: int
    jobs: List[JobResponse]
    searched_at: str


@router.get("/search", response_model=SearchResponse)
async def search_jobs_get(
    q: str = Query(..., description="Poste ou mot-clé"),
    location: str = Query("", description="Localisation"),
    job_type: str = Query("", description="Type: cdi, cdd, stage, freelance"),
    max_days_old: int = Query(5, description="Offres des derniers X jours"),
    max_results: int = Query(20, description="Nombre maximum de résultats")
):
    """Recherche GET - génère des offres réalistes sans scraping externe"""
    try:
        logger.info(f"🔍 Recherche: {q} à {location}")
        
        # Générer des offres réalistes (pas de scraping externe)
        # Use await directly since we're in an async context
        jobs_data = await search_jobs_async(
            query=q,
            location=location,
            job_type=job_type,
            max_days_old=max_days_old,
            max_results=max_results
        )
        
        # Si pas de résultats, retourner un message
        if not jobs_data:
            return SearchResponse(
                query=q,
                location=location or "France",
                total_found=0,
                jobs=[],
                searched_at=datetime.now().isoformat()
            )
        
        # Convertir en objets JobResponse
        jobs = [JobResponse(**job) for job in jobs_data]
        
        logger.info(f"✅ {len(jobs)} offres générées")
        
        return SearchResponse(
            query=q,
            location=location or "France",
            total_found=len(jobs),
            jobs=jobs,
            searched_at=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"❌ Erreur recherche: {e}")
        # Retourner des données par défaut en cas d'erreur
        return SearchResponse(
            query=q,
            location=location or "France",
            total_found=0,
            jobs=[],
            searched_at=datetime.now().isoformat()
        )


@router.post("/search", response_model=SearchResponse)
async def search_jobs(request: SearchRequest):
    """Recherche POST - génère des offres réalistes sans scraping externe"""
    return await search_jobs_get(
        q=request.query,
        location=request.location,
        job_type=request.job_type,
        max_days_old=request.max_days_old,
        max_results=request.max_results
    )


@router.get("/sources")
async def get_sources():
    """Liste des sources de données disponibles"""
    return {
        "sources": [
            {
                "name": "linkedin",
                "display": "LinkedIn",
                "description": "Le plus grand réseau professionnel",
                "url": "https://www.linkedin.com"
            },
            {
                "name": "indeed",
                "display": "Indeed",
                "description": "Moteur de recherche d'emplois",
                "url": "https://www.indeed.fr"
            },
            {
                "name": "junglejobs",
                "display": "Welcome to the Jungle",
                "description": "Startups et entreprises innovantes",
                "url": "https://www.welcometothejungle.com"
            }
        ],
        "note": "Offres générées localement - pas de rate limiting"
    }


@router.get("/trending")
async def get_trending_jobs():
    """Jobs populaires du moment"""
    return {
        "trending": [
            {"query": "développeur python", "location": "Paris"},
            {"query": "devops engineer", "location": "Lyon"},
            {"query": "data scientist", "location": "France"},
            {"query": "full stack", "location": "Berlin"},
            {"query": "product manager", "location": "France"},
        ],
        "message": "Recherches populaires en ce moment"
    }
