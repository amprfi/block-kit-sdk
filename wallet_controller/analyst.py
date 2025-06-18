from wallet_controller.block import BaseWalletInterface
from wallet_controller.models import AnalystController
from typing import Tuple, Optional

class AnalystWalletInterface(BaseWalletInterface):
    def is_operation_compliant(
        self,
        controller_settings: AnalystController,
        operation_type: str,
        message_type: Optional[str] = None
    ) -> Tuple[bool, str]:
        if not isinstance(controller_settings, AnalystController):
            return False, "Invalid controller settings type."

        reason = "Compliant"

        # Checks if operation type is allowed
        if operation_type != 'chat_message':
            reason = f"Invalid operation type: {operation_type}"
            return False, reason

        # Checks if message type is allowed
        if message_type:
            if message_type == 'advice' and not controller_settings.advice_allowed:
                reason = "Block is not authorized to provide investment advice"
                return False, reason
            elif message_type not in ['advice', 'analysis']:
                reason = f"Invalid message type: {message_type}"
                return False, reason

        return True, reason
