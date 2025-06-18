from wallet_interface.analyst import AnalystWalletInterface
from wallet_controller.models import AnalystController
from typing import Tuple, Optional

class ControllerManager:
    def __init__(self):
        """
        Initializes the ControllerManager
        """
        self.wallet_interface = AnalystWalletInterface()

    def is_operation_compliant(
        self,
        controller_settings: AnalystController,
        operation_type: str,
        message_type: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Checks if an operation is compliant with the given controller settings.

        Args:
            controller_settings: The AnalystController settings for the block instance.
            operation_type: The type of operation being performed.
            message_type: The type of message being sent ('advice' or 'analysis') (optional).

        Returns:
            A tuple (is_compliant: bool, reason: str) indicating compliance status and reason.
        """
        return self.wallet_interface.is_operation_compliant(controller_settings, operation_type, message_type)
