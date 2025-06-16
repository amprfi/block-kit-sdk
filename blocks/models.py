from typing import Literal, Optional, Union, Any, Dict
from enum import Enum
from pydantic import BaseModel, model_validator, ValidationError, PositiveFloat, HttpUrl
from pydantic_extra_types.country import CountryAlpha3

# --- Fee Structure Models ---

class FeeType(str, Enum):
    """Enumeration of possible fee types that a block can specify."""
    FIXED_ONE_TIME = "fixed_one_time"
    FIXED_RECURRING = "fixed_recurring"

class RecurringInterval(str, Enum):
    """Enumeration of possible intervals for recurring fees."""
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    ANNUALLY = "annually"

class FeeCurrency(str, Enum):
    """Enumeration of possible currencies for fees."""
    DAI = "DAI"
    USDC = "USDC"
    USDT = "USDT"
    AMPR = "AMPR"
    ETH = "ETH"

class BaseFee(BaseModel):
    """Base model for all fee types"""
    fee_currency: FeeCurrency
    description: Optional[str] = None

class OneTimeFixedFee(BaseFee):
    """Defines a fixed, one-time fee."""
    fee_type: Literal[FeeType.FIXED_ONE_TIME]
    amount: PositiveFloat

class RecurringFixedFee(BaseFee):
    """Defines a fixed fee that recurs at a specified interval."""
    fee_type: Literal[FeeType.FIXED_RECURRING]
    amount: PositiveFloat
    interval: RecurringInterval

Fee = Union[OneTimeFixedFee, RecurringFixedFee]
    
# --- Core Block Models ---

class Manifest(BaseModel):
    """
    Describes the metadata and capabilities of a block.
    This information is provided by the block developer.
    """
    name: str
    version: str
    block_type: Literal["analyst", "action", "custodial"]
    publisher: str
    description: str
    license: Optional[tuple[str, HttpUrl]] = None
    fee: Optional[Fee] = None
    allowed_jurisdictions: Optional[list[CountryAlpha3]] = None

    @model_validator(mode='before')
    @classmethod
    def check_fee_type(cls, data: Any) -> Any:
        if isinstance(data, dict) and 'fee' in data:
            if isinstance(data['fee'], list):
                if len(data['fee']) > 1:
                    raise ValueError("Only one type of fee is allowed")
                elif len(data['fee']) == 1:
                    # If it's a single-item list, extract the item
                    data['fee'] = data['fee'][0]
        return data