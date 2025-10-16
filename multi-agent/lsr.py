from pydantic import BaseModel
from enum import Enum


class LSRType(str, Enum):
    CONTRACT_REVIEW = "Contract Review"
    LEGAL_OPINION = "Legal Opinion"
    LITIGATION_SUPPORT = "Litigation Support"
    COMPLIANCE_REVIEW = "Compliance Review"
    INTELLECTUAL_PROPERTY = "Intellectual Property"
    EMPLOYMENT_LAW = "Employment Law"
    REGULATORY_MATTERS = "Regulatory Matters"
    OTHER = "Other"
    NONE = ""

class LSRPriority(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"
    NONE = ""

class LSRState(BaseModel):
    title: str = ''
    description: str = ''
    requestorName: str = ''
    requestorEmail: str = ''
    requestorDepartment: str = ''
    requestType: LSRType = ''
    priority: LSRPriority = ''
    dueDate: str = ''
    estimatedHours: int = 0
    notes: str = ''