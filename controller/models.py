from typing import Optional
from pydantic import BaseModel

class ControllerSettings(BaseModel):
    # block_id: str # This might be managed by the wallet core, linking settings to a block instance
    # For now, let's assume these settings are generic and applied by the wallet core.
    # If these settings are to be part of a payload for registering/updating controls for a block,
    # then a block_id or similar identifier would be needed.
    # Let's include an identifier for which block these settings apply to, if passed around.
    # However, an ActionBlock instance would likely just receive these values, not the block_id itself.
    # For now, defining the settings themselves:

    authorized_duration_days: int
    asset_id: str  # The specific asset these controls apply to
    max_amount_per_transaction: float
    cumulative_max_amount: float # Max total amount that can be transacted during the authorized duration
    # Consider adding:
    # allowed_actions: Optional[list[str]] = None # e.g., ["buy", "sell"]
    # allowed_counterparties: Optional[list[str]] = None
