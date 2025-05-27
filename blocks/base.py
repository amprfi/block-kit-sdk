from blocks.models import Manifest, TransactionProposal
from control.models import ControlSettings # Assuming ControlSettings will be passed here
from typing import Optional # For ActionBlock's control_settings

class BaseBlock:
    def __init__(self, manifest: Manifest):
        self.manifest = manifest
        # Placeholder for WebSocket connection to the block's own backend (if any)
        self.backend_ws = None
        print(f"Block '{self.manifest.name}' initialized.")

    def propose_transaction(self, proposal_data: TransactionProposal) -> dict:
        """
        Block proposes a transaction.
        The proposal_data should be a TransactionProposal model instance.
        API endpoints are responsible for converting raw request data to this model.
        """
        # In a real scenario, this would involve more complex logic.
        # For now, just log and return a standardized response.
        print(f"Block '{self.manifest.name}' proposing transaction: {proposal_data}")
        # This method would typically be called by the wallet core after receiving
        # a trigger or upon the block's own internal logic (if it were actively running).
        # The proposal is then sent to the wallet core.
        # Here, we simulate the block generating the proposal structure.

        # For the purpose of this base class, let's assume it returns the proposal
        # that would then be sent to the wallet core.
        return {"status": "proposed", "proposal": proposal_data.model_dump()}

    async def connect_to_backend(self, backend_url: str):
        # Placeholder for block connecting to its own backend (e.g., an LLM service)
        # import websockets # External library, not our ws_handlers
        # try:
        #     self.backend_ws = await websockets.connect(backend_url)
        #     print(f"Block '{self.manifest.name}' connected to its backend at {backend_url}")
        # except Exception as e:
        #     print(f"Block '{self.manifest.name}' failed to connect to backend: {e}")
        pass

    async def send_to_backend(self, message: str):
        # if self.backend_ws:
        #     await self.backend_ws.send(message)
        pass

    async def receive_from_backend(self):
        # if self.backend_ws:
        #     return await self.backend_ws.recv()
        return None

    async def close_backend_connection(self):
        # if self.backend_ws:
        #     await self.backend_ws.close()
        pass

class AnalystBlock(BaseBlock):
    def __init__(self, manifest: Manifest):
        if manifest.block_type != "analyst":
            raise ValueError("Manifest block_type must be 'analyst' for AnalystBlock.")
        super().__init__(manifest)
        print(f"AnalystBlock '{self.manifest.name}' initialized.")

    # Analyst blocks typically provide insights, not direct transaction proposals.
    # However, they might still use propose_transaction to suggest actions based on analysis.
    # Or they might have other methods like `get_analysis_report()`.

class ActionBlock(BaseBlock):
    def __init__(self, manifest: Manifest, control_settings: ControlSettings):
        if manifest.block_type != "action":
            raise ValueError("Manifest block_type must be 'action' for ActionBlock.")
        super().__init__(manifest)
        self.control_settings = control_settings
        print(f"ActionBlock '{self.manifest.name}' initialized with control settings.")

    def propose_transaction(self, proposal_data: TransactionProposal) -> dict:
        """
        ActionBlock proposes a transaction, potentially first checking against its controls.
        Note: Full compliance check against controls would typically happen in the wallet core
        or a dedicated ControlManager, using the user-defined ControlSettings for this block instance.
        A block might do a preliminary check.
        """
        print(f"ActionBlock '{self.manifest.name}' proposing transaction: {proposal_data.model_dump()}")

        # Preliminary check (example - not exhaustive)
        if proposal_data.asset_id != self.control_settings.asset_id:
            print(f"Proposal asset '{proposal_data.asset_id}' does not match controlled asset '{self.control_settings.asset_id}'.")
            return {"status": "rejected_by_block_pre_check", "reason": "Asset mismatch with controls", "proposal": proposal_data.model_dump()}

        if proposal_data.amount > self.control_settings.max_amount_per_transaction:
            print(f"Proposal amount {proposal_data.amount} exceeds max_amount_per_transaction {self.control_settings.max_amount_per_transaction}.")
            return {"status": "rejected_by_block_pre_check", "reason": "Exceeds max amount per transaction", "proposal": proposal_data.model_dump()}

        # Call BaseBlock's propose_transaction for common logic/formatting
        return super().propose_transaction(proposal_data)
