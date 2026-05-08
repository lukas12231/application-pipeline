from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from abc import ABC, abstractmethod

class JobLead(BaseModel):
    """Standardized model for a job opportunity."""
    title: str = Field(..., description="The original job title")
    ai_summary_title: Optional[str] = Field(None, description="AI-generated concise title")
    company: str
    location: str
    is_remote: bool = False
    source: str
    url: str
    date_posted: Optional[str] = None
    description: Optional[str] = None
    tags: List[str] = []
    fit_score: float = 0.0
    fit_reasoning: Optional[str] = None

class SearchConfig(BaseModel):
    """Configuration for a search operation."""
    job_titles: List[str]
    location: str
    radius_km: int = 50
    negative_keywords: List[str] = []
    min_salary_eur: int = 0
    required_education: Optional[str] = "Master"
    semantic_matching: bool = True
    remote_flexibility: bool = True

class UserProfile(BaseModel):
    """Candidate profile for semantic matching."""
    name: str
    target_roles: List[str]
    core_skills: List[str]
    experience_level: str
    languages: List[str]
    education_level: str
    preferred_locations: List[str] = []
    min_salary: int = 0

class BasePortalPlugin(ABC):
    """Abstract base class for all job portal plugins."""
    
    @abstractmethod
    def fetch_leads(self, config: SearchConfig) -> List[JobLead]:
        """Fetch leads from the specific portal and return a list of JobLead models."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the plugin."""
        pass
