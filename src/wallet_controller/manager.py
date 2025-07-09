from wallet_controller.block import BaseWalletInterface
from wallet_controller.models import BaseController
from typing import Tuple, Optional

class ControllerManager:
    def __init__(self, wallet_interface: BaseWalletInterface):
        """
        Initializes the ControllerManager with a specific wallet interface.

        Args:
            wallet_interface: An instance of a wallet interface that implements BaseWalletInterface.
        """
        self.wallet_interface = wallet_interface

    def is_operation_compliant(
        self,
        controller_settings: BaseController,
        operation_type: str,
        message_type: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Checks if an operation is compliant with the given controller settings.

        Args:
            controller_settings: The controller settings for the block instance.
            operation_type: The type of operation being performed.
            message_type: The type of message being sent (optional).

        Returns:
            A tuple (is_compliant: bool, reason: str) indicating compliance status and reason.
        """
        return self.wallet_interface.is_operation_compliant(controller_settings, operation_type, message_type)