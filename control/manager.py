from blocks.models import TransactionProposal
from control.models import ControlSettings # Renamed from Control to ControlSettings in models

class ControlManager:
    def __init__(self):
        # In a more complex scenario, this manager might load/cache control settings
        # or interact with a database of them. For now, it's stateless.
        pass

    def is_proposal_compliant(
        self,
        proposal: TransactionProposal,
        control_settings: ControlSettings,
        current_cumulative_spent: float = 0.0 # This would need to be tracked by the wallet core per block instance
    ) -> tuple[bool, str]:
        """
        Checks if a transaction proposal is compliant with the given control settings.

        Args:
            proposal: The TransactionProposal object.
            control_settings: The ControlSettings for the block instance.
            current_cumulative_spent: The total amount already spent by this block
                                      under these controls within the current duration.

        Returns:
            A tuple (is_compliant: bool, reason: str).
        """
        reason = "Compliant"

        # Check asset ID
        if proposal.asset_id != control_settings.asset_id:
            reason = f"Asset mismatch: Proposal for '{proposal.asset_id}', control is for '{control_settings.asset_id}'."
            return False, reason

        # Check max amount per transaction
        if proposal.amount <= 0:
            reason = "Transaction amount must be positive."
            return False, reason
            
        if proposal.amount > control_settings.max_amount_per_transaction:
            reason = f"Amount {proposal.amount} exceeds max per transaction ({control_settings.max_amount_per_transaction})."
            return False, reason

        # Check cumulative max amount
        if (current_cumulative_spent + proposal.amount) > control_settings.cumulative_max_amount:
            reason = (
                f"Cumulative amount {current_cumulative_spent + proposal.amount} would exceed "
                f"limit ({control_settings.cumulative_max_amount})."
            )
            return False, reason
        
        # Note: authorized_duration_days would need to be checked by the wallet core,
        # ensuring the block is still operating within its authorized time window.
        # This function focuses on transactional limits.

        return True, reason
