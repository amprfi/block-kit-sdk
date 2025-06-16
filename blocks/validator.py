from typing import Dict, Any, Union
from pydantic import ValidationError
from .models import Manifest, OneTimeFixedFee, RecurringFixedFee, Fee

class SDKValidator:
    """
    Main class for SDK validation functionality. Provides a clean interface for
    blocks to validate their configurations.
    """

    @staticmethod
    def validate_manifest(manifest_data: Dict[str, Any]) -> Manifest:
        """
        Validate a manifest configuration.

        Args:
            manifest_data: Dictionary containing manifest data to validate

        Returns:
            Validated Manifest object

        Raises:
            ValidationError: If the manifest data is invalid
        """
        try:
            return Manifest.model_validate(manifest_data)
        except ValidationError as e:
            raise ValidationError(f"Manifest validation failed: {str(e)}") from e

    @staticmethod
    def validate_fee(fee_data: Dict[str, Any]) -> Fee:
        """
        Validate a fee configuration.

        Args:
           fee_data: Dictionary containing fee data to validate

        Returns:
            Validated Fee object (either OneTimeFixedFee or RecurringFixedFee)

        Raises:
            ValidationError: If the fee data is invalid
        """
        try:
            fee_type = fee_data.get("fee_type")

            if fee_type == "fixed_one_time":
                return OneTimeFixedFee.model_validate(fee_data)
            elif fee_type == "fixed_recurring":
                return RecurringFixedFee.model_validate(fee_data)
            else:
                raise ValidationError(f"Unknown fee type: {fee_type}")
            
        except ValidationError as e:
            raise ValidationError(f"Fee validation failed: {str(e)}") from e

    @staticmethod
    def validate_config(config_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a complete configuration including manifest and fees.

        Args:
            config_data: Dictionary containing the complete configuration

        Returns:
            Dictionary with validated components

        Raises:
            ValidationError: If any part of the configuration is invalid
        """
        try:
            # Validate the manifest portion - this uses config_data
            validated_manifest = SDKValidator.validate_manifest(config_data)

            # Create a result dictionary with the validated manifest
            result = {"manifest": validated_manifest}

            # Check if there's a fee in the manifest and validate it
            if validated_manifest.fee:
                # Extract the fee data from the validated manifest
                fee_data = validated_manifest.fee.model_dump()
                # Validate the fee separately
                validated_fee = SDKValidator.validate_fee(fee_data)
                result["fee"] = validated_fee

            return result

        except ValidationError as e:
            raise ValidationError(f"Configuration validation failed: {str(e)}") from e
