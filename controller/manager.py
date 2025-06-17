from controller.models import AnalystController
from typing import Optional, Tuple

class ControllerManager:
    def __init__(self):
        """
        Initializes the ControllerManager
        """
        pass

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
        if not isinstance(controller_settings, AnalystController):
            return False, "Invalid controller settings type."

        reason = "Compliant"

        # Checks if the block is authorized
        if not controller_settings.authorized:
            reason = "Block is not authorized"
            return False, reason
        
        # Checks if authorization is still valid
        if controller_settings.authorized_duration_days is not None and controller_settings.authorized_duration_days <= 0:
            reason = "Authorization has expired"
            return False, reason
        
        # Checks if operation type is allowed
        if operation_type is not 'chat_message':
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