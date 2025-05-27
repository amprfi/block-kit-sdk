from typing import Literal, Optional
from pydantic import BaseModel

class Manifest(BaseModel):
    name: str
    version: str
    block_type: Literal["analyst", "action"]
    publisher: str
    description: str
    license: Optional[str] = None
    fees: Optional[str] = None

class TransactionProposal(BaseModel):
    block_id: str  # Identifier for the block proposing the transaction
    action_type: str  # e.g., "buy", "sell", "stake", "unstake"
    asset_id: str  # Identifier for the asset (e.g., token symbol, contract address)
    amount: float
    currency: str  # Currency of the amount (e.g., "USD" or the asset_id itself if amount is in asset units)
    justification: Optional[str] = None  # Optional reason/analysis for the proposal
