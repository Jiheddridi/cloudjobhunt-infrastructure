"""
CloudJobHunt Jobs API
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.crud.job import (
    get_job_by_id,
    get_jobs,
    search_jobs,
    create_job,
    update_job,
    delete_job,
    count_jobs,
    get_user_job_matches,
    create_job_match,
    update_job_match,
)
from app.schemas.job import (
    JobCreate,
    JobUpdate,
    Job,
    JobListResponse,
    JobMatchCreate,
    JobMatchUpdate,
    JobMatch,
    JobMatchListResponse,
)
from app.api.auth import get_current_active_user, TokenData

router = APIRouter()


# Job endpoints
@router.get("/", response_model=JobListResponse)
async def get_jobs_list(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    company: Optional[str] = None,
    location: Optional[str] = None,
    is_remote: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user),
):
    """Get list of jobs with optional filters"""
    jobs = get_jobs(
        db,
        skip=skip,
        limit=limit,
        company=company,
        location=location,
        is_remote=is_remote,
    )
    total = count_jobs(db)
    total_pages = (total + limit - 1) // limit
    
    return JobListResponse(
        jobs=jobs,
        total=total,
        page=skip // limit + 1,
        page_size=limit,
        total_pages=total_pages,
    )


@router.get("/search")
async def search_jobs_list(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user),
):
    """Search jobs by query"""
    jobs = search_jobs(db, query=q, skip=skip, limit=limit)
    return {"jobs": jobs, "count": len(jobs)}


@router.get("/{job_id}", response_model=Job)
async def get_job_details(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user),
):
    """Get job details by ID"""
    job = get_job_by_id(db, job_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return job


@router.post("/", response_model=Job)
async def create_new_job(
    job_data: JobCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user),
):
    """Create a new job (admin/scraper only)"""
    job = create_job(db, job_data)
    return job


@router.put("/{job_id}", response_model=Job)
async def update_job_by_id(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user),
):
    """Update a job (admin only)"""
    job = update_job(db, job_id, job_data)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return job


@router.delete("/{job_id}")
async def delete_job_by_id(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user),
):
    """Delete a job (admin only)"""
    success = delete_job(db, job_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job not found"
        )
    return {"message": "Job deleted successfully"}


# Job Match endpoints
@router.get("/matches/", response_model=JobMatchListResponse)
async def get_user_matches(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = None,
    is_favorite: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user),
):
    """Get job matches for current user"""
    matches = get_user_job_matches(
        db,
        user_id=current_user.user_id,
        skip=skip,
        limit=limit,
        status=status,
        is_favorite=is_favorite,
    )
    return JobMatchListResponse(matches=matches, total=len(matches))


@router.post("/matches/", response_model=JobMatch)
async def create_match(
    match_data: JobMatchCreate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user),
):
    """Create a job match for current user"""
    match_data.user_id = current_user.user_id
    match = create_job_match(db, match_data)
    return match


@router.put("/matches/{job_id}", response_model=JobMatch)
async def update_match(
    job_id: int,
    match_data: JobMatchUpdate,
    db: Session = Depends(get_db),
    current_user: TokenData = Depends(get_current_active_user),
):
    """Update a job match status"""
    match = update_job_match(
        db,
        user_id=current_user.user_id,
        job_id=job_id,
        match_data=match_data,
    )
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job match not found"
        )
    return match
