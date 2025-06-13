from typing import Optional
from pydantic import BaseModel, PositiveInt

class BaseController(BaseModel):
    """Base model for all block types"""
    authorized: bool = False
    authorized_duration_days: Optional[PositiveInt] = None

class AnalystController(BaseController):
    """Controller for Analyst blocks"""
    portfolio_access: bool = False