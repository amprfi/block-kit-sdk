from typing import Literal, Optional, List, Union
from enum import Enum
from pydantic import BaseModel, validator

# --- Fee Structure Models ---

class FeeType(str, Enum):
    """Enumeration of possible fee types that a block can specify."""
    FIXED_ONE_TIME = "fixed_one_time"
    FIXED_RECURRING = "fixed_recurring"
    PER_TRANSACTION_PERCENTAGE = "per_transaction_percentage"
    PER_TRANSACTION_FIXED = "per_transaction_fixed"

class RecurringInterval(str, Enum):
    """Enumeration of possible intervals for recurring fees."""
    DAILY = "daily"
    WEEKLY = "weekly"
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

class PerTransactionPercentageFee(BaseFee):
    """Defines a fee calculated as a percentage of the transaction amount."""
    fee_type: Literal[FeeType.PER_TRANSACTION_PERCENTAGE] = FeeType.PER_TRANSACTION_PERCENTAGE
    percentage: float  # e.g., 0.01 for 1%. Applied to the transaction amount.
    min_amount: Optional[float] = None  # Optional minimum fee amount for this percentage fee.
    max_amount: Optional[float] = None  # Optional maximum fee amount for this percentage fee.
    # currency_for_min_max: Optional[str] = None # If min/max are in a specific currency. Assumed same as transaction if None.

class PerTransactionFixedFee(BaseFee):
    """Defines a fixed fee applied to each transaction."""
    fee_type: Literal[FeeType.PER_TRANSACTION_FIXED] = FeeType.PER_TRANSACTION_FIXED
    amount: float
    currency: str

# Union type for Pydantic to handle different fee structures.
# Pydantic will use the `fee_type` field to discriminate between these models.
FeeDetail = Union[
    OneTimeFixedFee,
    RecurringFixedFee,
    PerTransactionPercentageFee,
    PerTransactionFixedFee
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
