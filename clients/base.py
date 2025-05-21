# clients/base.py
from abc import ABC, abstractmethod
from typing import List, Optional
from pydantic import BaseModel

class Incident(BaseModel):
    id: str
    created_at: str
    detected_at: Optional[str] = None
    acknowledged_at: Optional[str] = None 
    resolved_at: Optional[str] = None
    priority: Optional[str] = None

class IncidentClient(ABC):
    @abstractmethod
    def list_incidents(self) -> List[Incident]:
        ...
