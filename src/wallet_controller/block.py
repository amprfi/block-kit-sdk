from abc import ABC
from wallet_controller.models import AnalystController
from typing import Tuple, Optional

class BaseWalletInterface(ABC):
    def is_operation_compliant(
        self,
        controller_settings: AnalystController,
    ) -> Tuple[bool, str]:
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