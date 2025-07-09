from abc import ABC, abstractmethod
from wallet_controller.models import BaseController
from typing import Tuple, Optional

class BaseWalletInterface(ABC):
    """
    Abstract base class defining the required wallet interface methods
    that all wallet interfaces must implement.
    """

    @abstractmethod
    def is_operation_compliant(
        self,
        controller_settings: BaseController,
        operation_type: str,
        message_type: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Required method to check if an operation is compliant with controller settings.

        Args:
            controller_settings: The controller settings for the block instance
            operation_type: The type of operation being performed
            message_type: The type of message being sent (optional)

        Returns:
            A tuple (is_compliant: bool, reason: str) indicating compliance status and reason
        """
        reason = "Compliant"

        # Checks if the block is authorized
        if not controller_settings.authorized:
            reason = "Block is not authorized"
            return False, reason

        # Checks if authorization is still valid
        if controller_settings.authorized_duration_days is not None and controller_settings.authorized_duration_days <= 0:
            reason = "Authorization has expired"
            return False, reason

        return True, reason