from typing import Literal, Optional, Union, Any, Dict
from enum import Enum
from pydantic import BaseModel, model_validator, ValidationError, PositiveFloat, HttpUrl, field_validator
from pydantic_extra_types.country import CountryAlpha3
from datetime import datetime, timezone

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
    """Enumeration of accepted fee currencies."""
    DAI = "DAI"
    USDC = "USDC"
    USDT = "USDT"
    AMPR = "AMPR"
    ETH = "ETH"
    BTC = "BTC"
    SOL = "SOL"

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
    publisher: tuple[str, str]
    description: str
    license: Optional[tuple[str, HttpUrl]] = None
    fee: Optional[Union[OneTimeFixedFee, RecurringFixedFee]] = None
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
    
class UserProfile(BaseModel):
    """User preferences and settings"""
    display_name: Optional[str] = None
    language: Optional[str] = "en"
    notifications: Optional[Dict] = {}
    privacy_settings: Optional[Dict] = {
        "share_portfolio_data": False,
    }

class UserModel(BaseModel):
    """
    Comprehensive user model for the Ampr wallet system.
    Uses ENS as the primary identifier with additional validation.
    """
    ens_name: str
    registration_date: datetime = datetime.now(timezone.utc)
    last_login: datetime
    profile: UserProfile = UserProfile()
    jurisdiction: CountryAlpha3

    @field_validator('ens_name')
    def validate_ens_name(cls, v: str) -> str:
        """
        Validate ENS name format.
        Basic validation for ENS names (simplified version).
        """
        # Basic ENS name validation pattern
        if not re.match(r'^[a-z0-9-]+\.eth$', v.lower()):
            raise ValueError(
                "Invalid ENS name format. Must be in format 'name.eth' and contain only alphanumeric characters and hyphens."
            )
        return v.lower()
    
    @property
    def primary_identifier(self) -> str:
        """Returns the primary identifier for system-wide use"""
        return self.ens_name

    def add_registered_block(self, block_identifier: str, block_specific_id: str):
        """Add a block to the user's registered blocks"""
        if block_identifier not in self.registered_blocks:
            self.registered_blocks[block_identifier] = {
                "block_specific_id": block_specific_id,
                "registration_date": datetime.utcnow().isoformat()
            }

    def update_block_specific_id(self, block_identifier: str, new_id: str):
        """Update a block-specific ID for a registered block"""
        if block_identifier in self.registered_blocks:
            self.registered_blocks[block_identifier]["block_specific_id"] = new_id