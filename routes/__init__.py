from fastapi import APIRouter, HTTPException, Body
from typing import Dict, Optional
import uuid # Still useful for proposal IDs or other internal uses if needed

from blocks.models import Manifest, TransactionProposal
from controller.models import ControllerSettings
from blocks.base import AnalystBlock, ActionBlock, BaseBlock
from controller.manager import ControllerManager

router = APIRouter()

# --- Single Block Instance Configuration ---
# This section would typically be loaded from a config file or env vars at app startup.
# For now, we'll hardcode a default block for demonstration.
# Users of this library would configure their specific block's details here.

BLOCK_TYPE = "action"  # or "analyst". Developer using the SDK would set this.

DEFAULT_MANIFEST = Manifest(
    name="My Default Action Block",
    version="0.1.0",
    block_type=BLOCK_TYPE, # Ensure this matches BLOCK_TYPE
    publisher="Block Kit Developer",
    description="A default action block instance using the Block Kit library."
)

# ControllerSettings are only relevant for ActionBlocks
DEFAULT_CONTROL_SETTINGS: Optional[ControllerSettings] = None
if BLOCK_TYPE == "action":
    DEFAULT_CONTROL_SETTINGS = ControllerSettings(
        authorized_duration_days=30,
        asset_id="BTC", # Example
        max_amount_per_transaction=1.0, # Example: 1 BTC
        cumulative_max_amount=10.0 # Example: 10 BTC
    )

# --- Initialize the single block instance ---
block_instance: BaseBlock
if BLOCK_TYPE == "action":
    if DEFAULT_CONTROL_SETTINGS is None:
        # This should not happen if configured correctly
        raise RuntimeError("Action block configured but no controller settings provided.")
    block_instance = ActionBlock(manifest=DEFAULT_MANIFEST, controller_settings=DEFAULT_CONTROL_SETTINGS)
elif BLOCK_TYPE == "analyst":
    block_instance = AnalystBlock(manifest=DEFAULT_MANIFEST)
else:
    raise RuntimeError(f"Invalid BLOCK_TYPE configured: {BLOCK_TYPE}")

controller_manager = ControllerManager()
# For tracking cumulative spend for the ActionBlock (if applicable)
# This state needs to persist for the lifetime of the block's authorized duration.
# For a stateless server, this would need external storage (e.g., Redis, DB).
# For a stateful block instance, it could be an instance variable if the app server is long-lived.
# Simplified in-memory for now:
current_cumulative_spend: float = 0.0


@router.get("/manifest", response_model=Manifest)
async def get_manifest():
    """
    Returns the manifest of this block instance.
    """
    return block_instance.manifest

@router.post("/propose_transaction")
async def propose_transaction_endpoint(proposal_input: TransactionProposal):
    """
    Endpoint for the block to propose a transaction.
    The wallet core would call this if it's designed for the block to push proposals.
    Alternatively, the block's internal logic might call its own propose_transaction method,
    and this endpoint might be for the wallet core to *request* a proposal or trigger an action.

    Let's assume this endpoint is how the block, after its internal logic,
    communicates a decided proposal outwards (e.g., to the wallet core via an API call
    if this server is exposed to the wallet core, or this is called by the block's agent logic).
    """
    global current_cumulative_spend # Modifying global state, use with caution in real apps

    # The proposal_input.block_id should ideally match our block's ID from its manifest,
    # or be set by this block instance.
    # For now, let's ensure the proposal reflects this block's identity.
    # A more robust system might have a unique instance ID for the block.
    # proposal_input.block_id = block_instance.manifest.name # Or a more unique ID from manifest

    if isinstance(block_instance, ActionBlock):
        # ActionBlock specific logic: check against controllers
        if block_instance.controller_settings is None: # Should be set at init for ActionBlock
             raise HTTPException(status_code=500, detail="Internal error: Controllers not configured for action block.")

        is_compliant, reason = controller_manager.is_proposal_compliant(
            proposal=proposal_input,
            controller_settings=block_instance.controller_settings,
            current_cumulative_spent=current_cumulative_spend
        )

        if not is_compliant:
            return {"status": "rejected_by_library_core", "reason": reason, "proposal": proposal_input.model_dump()}

        # If compliant, proceed with block's own proposal logic
        response = block_instance.propose_transaction(proposal_input) # ActionBlock's method

        # If the block's own checks also pass and it's "proposed"
        if response.get("status") == "proposed":
            current_cumulative_spend += proposal_input.amount
            return response
        else:
            # Block's internal pre-check might have rejected it
            return response

    elif isinstance(block_instance, AnalystBlock):
        # Analyst block proposes transaction
        response = block_instance.propose_transaction(proposal_input)
        return response
    
    # This case should ideally not be reached if block_instance is always Analyst or Action
    raise HTTPException(status_code=500, detail="Internal error: Unknown block instance type.")

# Optional: Endpoint to get current controller settings for an ActionBlock
if BLOCK_TYPE == "action":
    @router.get("/controller_settings", response_model=ControllerSettings)
    async def get_controller_settings():
        if isinstance(block_instance, ActionBlock) and block_instance.controller_settings:
            return block_instance.controller_settings
        raise HTTPException(status_code=404, detail="Controller settings not applicable or not found for this block.")

# (Consider adding a POST /configure endpoint later if needed for runtime configuration by wallet core)
