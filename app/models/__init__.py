# CloudJobHunt Models# Import all models to register them with SQLAlchemy
from app.models.user import User
from app.models.cv import CV
from app.models.job import Job
from app.models.match import JobMatch
from app.models.preferences import SearchPreferences

__all__ = [
    "User",
    "CV",
    "Job",
    "JobMatch",
    "SearchPreferences",
]