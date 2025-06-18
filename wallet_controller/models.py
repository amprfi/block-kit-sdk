from typing import Optional, Literal
from pydantic import BaseModel, PositiveInt

class BaseController(BaseModel):
    """Base model for all block types"""
    authorized: bool = False
    authorized_duration_days: Optional[PositiveInt] = None

class AnalystController(BaseController):
    """Controller for Analyst blocks"""
    portfolio_access: bool = False
    advice_allowed: bool = False

OperationType = Literal['chat_message']
MessageType = Literal['advice', 'analysis']

class Operation(BaseModel):
    operation_type: OperationType
    message: Optional['Message'] = None

class Message(BaseModel):
    message_type: MessageType
    content: str