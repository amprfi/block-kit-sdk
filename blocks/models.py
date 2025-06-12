from typing import Literal, Optional, Union, Any
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
    fee_type: Literal[FeeType.FIXED_ONE_TIME] = FeeType.FIXED_ONE_TIME
    amount: PositiveFloat

class RecurringFixedFee(BaseFee):
    """Defines a fixed fee that recurs at a specified interval."""
    fee_type: Literal[FeeType.FIXED_RECURRING] = FeeType.FIXED_RECURRING
    amount: PositiveFloat
    interval: RecurringInterval

FeeType = Union[OneTimeFixedFee, RecurringFixedFee]
    
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
    fee: Optional[FeeType] = None
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

class TransactionProposal(BaseModel):
    """
    Represents a transaction proposed by a block to the Wallet Core.
    """
    block_id: str  # Identifier for the block instance proposing the transaction (e.g., manifest.name or a unique instance ID)
    action_type: str  # e.g., "buy", "sell", "stake", "unstake", "swap"
    asset_id: str  # Identifier for the primary asset involved (e.g., token symbol, contract address)
    amount: PositiveFloat   # Amount of the primary asset
    currency: str   # Currency of the 'amount' field (e.g., "USD" if amount is a monetary value, or asset_id if amount is in units of the asset)
    # For more complex transactions like swaps, additional fields might be needed:
    # to_asset_id: Optional[str] = None
    # to_amount: Optional[float] = None
    justification: Optional[str] = None  # Optional reason or analysis supporting the proposal

# Manual testing (to be removed)
try:
    manifest = Manifest(
        name="Example Block",
        version="1.0",
        block_type="analyst",
        publisher="Example Publisher",
        description="An example block",
        allowed_jurisdictions=["USA", "CAN"],
         fee=[         
            OneTimeFixedFee(amount=10.0, fee_currency="USDT"),
         ]
    )
    print(manifest)
except ValidationError as e:
    print(f"Validation error: {e}")