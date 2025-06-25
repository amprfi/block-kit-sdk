from blocks.models import Manifest
from typing import Optional

class BaseBlock:
    """
    Base class for all Block types.

    Developers creating a new Block should typically inherit from `AnalystBlock`
    or `ActionBlock`, which themselves inherit from this `BaseBlock`.

    Attributes:
        manifest (Manifest): The manifest data for this block, provided upon initialization.
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

    async def connect_to_backend(self, backend_url: str):
        """
        Placeholder method for a block to connect to its own custom backend service
        via XMTP. Developers should override this or implement connection logic
        if their block requires such a connection.

        Args:
            backend_url: The URL of the XMTP backend service.
        """
        # Developer to implement if needed.
        pass

    async def send_to_backend(self, message: str):
        """
        Placeholder method to send a message to the block's custom backend via
        an established XMTP connection.
        """
        # if self.backend_ws:
        #     try:
        #         await self.backend_ws.send(message)
        #     except Exception as e:
        #         # logging.error(f"Error sending to backend: {e}")
        # else:
        #     # logging.warning("No backend XMTP connection to send message.")
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
        Placeholder method to close the XMTP connection to the custom backend.
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
