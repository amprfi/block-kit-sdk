from blocks.models import Manifest, TransactionProposal
from control.models import ControlSettings
from typing import Optional

class BaseBlock:
    """
    Base class for all Block types.

    Developers creating a new Block should typically inherit from `AnalystBlock`
    or `ActionBlock`, which themselves inherit from this `BaseBlock`.

    Attributes:
        manifest (Manifest): The manifest data for this block, provided upon initialization.
        backend_ws: Placeholder for a WebSocket connection object. Blocks requiring
                    communication with a custom backend service (e.g., a proprietary
                    data API, an LLM) can use this attribute to store their
                    WebSocket client. This is separate from the block's communication
                    with the Wallet Core.
    """
    def __init__(self, manifest: Manifest):
        """
        Initializes the BaseBlock.

        Args:
            manifest: An instance of the `Manifest` model containing metadata for this block.
        """
        self.manifest = manifest
        self.backend_ws = None # Initialize to None; developer must manage actual connection.
        # Consider replacing print with logging in a real SDK:
        # import logging
        # logging.info(f"Block '{self.manifest.name}' initialized.")

    def propose_transaction(self, proposal_data: TransactionProposal) -> dict:
        """
        Formats a transaction proposal to be sent from the block to the Wallet Core.

        Block developers should ensure their block's logic culminates in creating a
        `TransactionProposal` object and then can use this method (or override it)
        to structure the final output. The actual submission of this proposal to
        the Wallet Core is handled by the Block Kit server infrastructure via its API.

        Args:
            proposal_data: A `TransactionProposal` model instance detailing the transaction.

        Returns:
            A dictionary representing the proposal, typically including a 'status'
            and the 'proposal' details (e.g., after model dumping).
            Example: `{"status": "proposed", "proposal": proposal_data.model_dump()}`
        """
        # This base implementation simply returns a standard structure.
        # Specific block types (like ActionBlock) may add pre-checks or modifications.
        return {"status": "proposed", "proposal": proposal_data.model_dump()}

    async def connect_to_backend(self, backend_url: str):
        """
        Placeholder method for a block to connect to its own custom backend service
        via WebSockets. Developers should override this or implement connection logic
        if their block requires such a connection.

        Example using the 'websockets' library (ensure it's an installed dependency):
        ```python
        # import websockets # Make sure 'websockets' library is installed
        # try:
        #     self.backend_ws = await websockets.connect(backend_url)
        #     # logging.info(f"Block '{self.manifest.name}' connected to backend: {backend_url}")
        # except Exception as e:
        #     # logging.error(f"Block '{self.manifest.name}' backend connection error: {e}")
        #     self.backend_ws = None
        ```

        Args:
            backend_url: The URL of the custom backend WebSocket service.
        """
        # Developer to implement if needed.
        pass

    async def send_to_backend(self, message: str):
        """
        Placeholder method to send a message to the block's custom backend via
        an established WebSocket connection (self.backend_ws).
        """
        # if self.backend_ws:
        #     try:
        #         await self.backend_ws.send(message)
        #     except Exception as e:
        #         # logging.error(f"Error sending to backend: {e}")
        # else:
        #     # logging.warning("No backend WebSocket connection to send message.")
        pass

    async def receive_from_backend(self) -> Optional[str]:
        """
        Placeholder method to receive a message from the block's custom backend.
        """
        # if self.backend_ws:
        #     try:
        #         return await self.backend_ws.recv()
        #     except Exception as e:
        #         # logging.error(f"Error receiving from backend: {e}")
        # return None
        return None # Explicitly return None if not implemented or no connection

    async def close_backend_connection(self):
        """
        Placeholder method to close the WebSocket connection to the custom backend.
        """
        # if self.backend_ws:
        #     try:
        #         await self.backend_ws.close()
        #     except Exception as e:
        #         # logging.error(f"Error closing backend connection: {e}")
        #     finally:
        #         self.backend_ws = None
        pass

class AnalystBlock(BaseBlock):
    """
    Base class for Analyst Blocks.

    Analyst Blocks are designed primarily for research, data gathering, and providing
    analytical insights. They may propose transactions based on their analysis,
    or expose other methods for the Wallet Core to retrieve reports or data.
    """
    def __init__(self, manifest: Manifest):
        """
        Initializes the AnalystBlock.

        Args:
            manifest: An instance of the `Manifest` model. Must have `block_type` set to "analyst".
        
        Raises:
            ValueError: If the provided manifest's `block_type` is not "analyst".
        """
        if manifest.block_type != "analyst":
            raise ValueError("Manifest 'block_type' must be 'analyst' for AnalystBlock.")
        super().__init__(manifest)
        # logging.info(f"AnalystBlock '{self.manifest.name}' initialized.")

    # Developers can add custom methods here, e.g., get_market_report(), analyze_asset(asset_id), etc.
    # They can still use `propose_transaction` if their analysis leads to a suggestion.

class ActionBlock(BaseBlock):
    """
    Base class for Action Blocks.

    Action Blocks are designed to execute automated strategies, by
    proposing transactions. They operate under `ControlSettings` defined by the
    end-user via their wallet application.

    Attributes:
        control_settings (ControlSettings): The operational limits and permissions
                                            for this block instance.
    """
    def __init__(self, manifest: Manifest, control_settings: ControlSettings):
        """
        Initializes the ActionBlock.

        Args:
            manifest: An instance of the `Manifest` model. Must have `block_type` set to "action".
            control_settings: An instance of `ControlSettings` defining the block's operational limits.
        
        Raises:
            ValueError: If the provided manifest's `block_type` is not "action".
        """
        if manifest.block_type != "action":
            raise ValueError("Manifest 'block_type' must be 'action' for ActionBlock.")
        super().__init__(manifest)
        self.control_settings = control_settings
        # logging.info(f"ActionBlock '{self.manifest.name}' initialized with control settings.")

    def propose_transaction(self, proposal_data: TransactionProposal) -> dict:
        """
        Proposes a transaction, performing preliminary checks against its `ControlSettings`.

        Note: A more comprehensive compliance check against `ControlSettings` (including
        aspects like cumulative limits and duration) is expected to be performed by
        the Wallet Core, using the `ControlManager`. This method provides an initial
        safeguard within the block itself.

        Args:
            proposal_data: A `TransactionProposal` model instance.

        Returns:
            A dictionary indicating the status of the proposal. If preliminary checks
            fail, status may be "rejected_by_block_pre_check". Otherwise, it calls
            the base class's `propose_transaction` method.
        """
        # Perform preliminary checks against control settings.
        if proposal_data.asset_id != self.control_settings.asset_id:
            # logging.warning(f"ActionBlock '{self.manifest.name}': Proposal asset '{proposal_data.asset_id}' "
            #                 f"mismatches controlled asset '{self.control_settings.asset_id}'.")
            return {
                "status": "rejected_by_block_pre_check",
                "reason": "Asset mismatch with block's control settings.",
                "proposal": proposal_data.model_dump()
            }

        if proposal_data.amount > self.control_settings.max_amount_per_transaction:
            # logging.warning(f"ActionBlock '{self.manifest.name}': Proposal amount {proposal_data.amount} "
            #                 f"exceeds max_amount_per_transaction {self.control_settings.max_amount_per_transaction}.")
            return {
                "status": "rejected_by_block_pre_check",
                "reason": "Exceeds maximum amount per transaction defined in block's control settings.",
                "proposal": proposal_data.model_dump()
            }

        # If preliminary checks pass, proceed with the standard proposal process.
        return super().propose_transaction(proposal_data)
