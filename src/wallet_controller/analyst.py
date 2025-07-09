from wallet_controller.block import BaseWalletInterface
from wallet_controller.models import AnalystController
from typing import Tuple, Optional

class AnalystWalletInterface(BaseWalletInterface):
    """
    Concrete implementation of the wallet interface for Analyst blocks.
    Implements the required compliance checking with analyst-specific rules.
    """

    def is_operation_compliant(
        self,
        controller_settings: AnalystController,
        operation_type: str,
        message_type: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Checks if an operation is compliant with the given controller settings.

        Args:
            controller_settings: The AnalystController settings for the block instance
            operation_type: The type of operation being performed
            message_type: The type of message being sent ('advice' or 'analysis') (optional)

        Returns:
            A tuple (is_compliant: bool, reason: str) indicating compliance status and reason
        """
        if not isinstance(controller_settings, AnalystController):
            return False, "Invalid controller settings type."

        # First check the base compliance rules
        is_compliant, reason = super().is_operation_compliant(controller_settings, operation_type, message_type)
        if not is_compliant:
            return is_compliant, reason

        # Check analyst-specific rules
        if operation_type != 'chat_message':
            return False, f"Invalid operation type: {operation_type}"

        if message_type:
            if message_type == 'advice' and not controller_settings.advice_allowed:
                return False, "Block is not authorized to provide investment advice"
            elif message_type not in ['advice', 'analysis']:
                return False, f"Invalid message type: {message_type}"

        return True, "Compliant"