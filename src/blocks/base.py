from abc import ABC, abstractmethod
from typing import Optional
from blocks.models import Manifest, FeeType, FeeCurrency

class BaseBlock(ABC):
    """
    Abstract base class for all Block types with required core methods
    and optional concrete implementations.
    """

    @abstractmethod
    def __init__(self, manifest: Manifest):
        """
        Required initialization method for all blocks.

        Args:
            manifest: An instance of the `Manifest` model containing metadata for this block.
        """
        self.manifest = manifest
        self.backend_ws = None

    @abstractmethod
    async def initialize(self) -> None:
        """
        Required initialization method that all blocks must implement.
        This is called when the block is first loaded.
        """
        pass

    @abstractmethod
    async def get_fee_structure(self) -> dict:
        """
        Required method to specify the fee structure for this block.
        All blocks must implement this method.

        Returns:
            Dictionary containing the fee structure information
        """
        pass

    async def connect_to_backend(self, backend_url: str) -> None:
        """
        Optional method to connect to a custom backend service via XMTP.
        Default implementation does nothing.
        """
        pass

    async def send_to_backend(self, message: str) -> None:
        """
        Optional method to send a message to the block's custom backend.
        Default implementation does nothing.
        """
        if self.backend_ws:
            try:
                await self.backend_ws.send(message)
            except Exception as e:
                print(f"Error sending to backend: {e}")
        else:
            print("No backend XMTP connection to send message.")

    async def receive_from_backend(self) -> Optional[str]:
        """
        Optional method to receive a message from the block's custom backend.
        Default implementation returns None.
        """
        if self.backend_ws:
            try:
                return await self.backend_ws.recv()
            except Exception as e:
                print(f"Error receiving from backend: {e}")
        return None

    async def close_backend_connection(self) -> None:
        """
        Optional method to close the XMTP connection to the custom backend.
        Default implementation does nothing.
        """
        if self.backend_ws:
            try:
                await self.backend_ws.close()
            except Exception as e:
                print(f"Error closing backend connection: {e}")
            finally:
                self.backend_ws = None

class AnalystBlock(BaseBlock):
    """
    Abstract base class for Analyst Blocks with required analysis methods.
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

    async def get_fee_structure(self) -> dict:
        """
        Required method to specify the fee structure for this analyst block.
        All blocks must implement this method.

        Returns:
            Dictionary containing the fee structure information
        """
        return {
            "type": FeeType.FIXED_ONE_TIME.value,
            "currency": FeeCurrency.ETH.value,
            "amount": 0,
            "interval": None  # Only relevant for recurring fees
        }