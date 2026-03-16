from pydantic import BaseModel

from typing import List, Optional

class SOPRequest(BaseModel):
    process_description: str

class SOPResponse(BaseModel):
    title: str
    purpose: str
    scope: str
    responsibilities: List[str]
    materials: List[str]
    steps: List[str]
    kpis: List[str]
    risks: List[str]
    version: str
    notes: Optional[str] = None
