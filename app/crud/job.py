"""
CloudJobHunt Job CRUD Operations
"""
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.job import Job
from app.models.match import JobMatch
from app.schemas.job import JobCreate, JobUpdate, JobMatchCreate, JobMatchUpdate


def get_job_by_id(db: Session, job_id: int) -> Optional[Job]:
    """Get a job by ID"""
    return db.query(Job).filter(Job.id == job_id).first()


def get_job_by_external_id(db: Session, external_id: str) -> Optional[Job]:
    """Get a job by external ID"""
    return db.query(Job).filter(Job.external_id == external_id).first()


def get_jobs(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    company: Optional[str] = None,
    location: Optional[str] = None,
    is_remote: Optional[bool] = None,
) -> List[Job]:
    """Get jobs with optional filters"""
    query = db.query(Job).filter(Job.is_active == True)
    
    if company:
        query = query.filter(Job.company.ilike(f"%{company}%"))
    if location:
        query = query.filter(Job.location.ilike(f"%{location}%"))
    if is_remote is not None:
        query = query.filter(Job.is_remote == is_remote)
    
    return query.order_by(desc(Job.scraped_at)).offset(skip).limit(limit).all()


def search_jobs(db: Session, query: str, skip: int = 0, limit: int = 100) -> List[Job]:
    """Search jobs by title, company, or description"""
    search_query = db.query(Job).filter(
        Job.is_active == True
    ).filter(
        (Job.title.ilike(f"%{query}%")) |
        (Job.company.ilike(f"%{query}%")) |
        (Job.description.ilike(f"%{query}%"))
    )
    return search_query.order_by(desc(Job.scraped_at)).offset(skip).limit(limit).all()


def create_job(db: Session, job_data: JobCreate) -> Job:
    """Create a new job"""
    db_job = Job(**job_data.model_dump())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def update_job(db: Session, job_id: int, job_data: JobUpdate) -> Optional[Job]:
    """Update a job"""
    db_job = get_job_by_id(db, job_id)
    if not db_job:
        return None
    
    update_data = job_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_job, field, value)
    
    db.commit()
    db.refresh(db_job)
    return db_job


def delete_job(db: Session, job_id: int) -> bool:
    """Delete a job"""
    db_job = get_job_by_id(db, job_id)
    if not db_job:
        return False
    
    db.delete(db_job)
    db.commit()
    return True


def count_jobs(db: Session) -> int:
    """Count total active jobs"""
    return db.query(Job).filter(Job.is_active == True).count()


# Job Match CRUD operations
def get_job_match(db: Session, user_id: int, job_id: int) -> Optional[JobMatch]:
    """Get a job match by user_id and job_id"""
    return db.query(JobMatch).filter(
        JobMatch.user_id == user_id,
        JobMatch.job_id == job_id
    ).first()


def get_user_job_matches(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    is_favorite: Optional[bool] = None,
) -> List[JobMatch]:
    """Get job matches for a user"""
    query = db.query(JobMatch).filter(JobMatch.user_id == user_id)
    
    if status:
        query = query.filter(JobMatch.status == status)
    if is_favorite is not None:
        query = query.filter(JobMatch.is_favorite == is_favorite)
    if is_favorite is None:
        query = query.filter(JobMatch.is_hidden == False)
    
    return query.order_by(desc(JobMatch.matched_at)).offset(skip).limit(limit).all()


def create_job_match(db: Session, match_data: JobMatchCreate) -> JobMatch:
    """Create a new job match"""
    db_match = JobMatch(**match_data.model_dump())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


def update_job_match(
    db: Session,
    user_id: int,
    job_id: int,
    match_data: JobMatchUpdate
) -> Optional[JobMatch]:
    """Update a job match"""
    db_match = get_job_match(db, user_id, job_id)
    if not db_match:
        return None
    
    update_data = match_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_match, field, value)
    
    db.commit()
    db.refresh(db_match)
    return db_match


def count_user_job_matches(db: Session, user_id: int) -> int:
    """Count job matches for a user"""
    return db.query(JobMatch).filter(
        JobMatch.user_id == user_id,
        JobMatch.is_hidden == False
    ).count()
