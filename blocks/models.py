from typing import Literal, Optional, List, Union
from enum import Enum
from pydantic import BaseModel

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

class BaseFee(BaseModel):
    """Base model for all fee types, providing a common description field."""
    description: Optional[str] = None

class OneTimeFixedFee(BaseFee):
    """Defines a fixed, one-time fee."""
    fee_type: Literal[FeeType.FIXED_ONE_TIME] = FeeType.FIXED_ONE_TIME
    amount: float
    currency: str  # e.g., "USD", "ETH"

class RecurringFixedFee(BaseFee):
    """Defines a fixed fee that recurs at a specified interval."""
    fee_type: Literal[FeeType.FIXED_RECURRING] = FeeType.FIXED_RECURRING
    amount: float
    currency: str
    interval: RecurringInterval

# Union type for Pydantic to handle different fee structures.
# Pydantic will use the `fee_type` field to discriminate between these models.
FeeDetail = Union[
    OneTimeFixedFee,
    RecurringFixedFee,
]

# --- Core Block Models ---

class Manifest(BaseModel):
    """
    Describes the metadata and capabilities of a block.
    This information is provided by the block developer.
    """
    name: str
    version: str
    block_type: Literal["analyst", "action"]
    publisher: str
    description: str
    license: Optional[str] = None
    fees: Optional[List[FeeDetail]] = None # Updated to use the structured fee models

class TransactionProposal(BaseModel):
    """
    Represents a transaction proposed by a block to the Wallet Core.
    """
    block_id: str  # Identifier for the block instance proposing the transaction (e.g., manifest.name or a unique instance ID)
    action_type: str  # e.g., "buy", "sell", "stake", "unstake", "swap"
    asset_id: str  # Identifier for the primary asset involved (e.g., token symbol, contract address)
    amount: float   # Amount of the primary asset
    currency: str   # Currency of the 'amount' field (e.g., "USD" if amount is a monetary value, or asset_id if amount is in units of the asset)
    # For more complex transactions like swaps, additional fields might be needed:
    # to_asset_id: Optional[str] = None
    # to_amount: Optional[float] = None
    justification: Optional[str] = None  # Optional reason or analysis supporting the proposal
