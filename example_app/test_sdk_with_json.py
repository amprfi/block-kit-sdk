"""
Test script that demonstrates using the Blocks SDK with an actual JSON configuration file.
"""

import json
from pathlib import Path
from blocks import SDKValidator
from pydantic import ValidationError

def load_config_from_file(config_path: str = "app_config.json") -> dict:
    """
    Load configuration from a JSON file.

    Args:
        config_path: Path to the configuration file

    Returns:
        Dictionary containing the configuration

    Raises:
        FileNotFoundError: If the configuration file doesn't exist
        json.JSONDecodeError: If the configuration file contains invalid JSON
    """
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Configuration file not found at {config_path}")

    with open(path, 'r', encoding='utf-8') as config_file:
        return json.load(config_file)

def test_sdk_with_json_config():
    """
    Test the SDK by loading a configuration from an actual JSON file.
    """
    try:
        # Load the configuration from the JSON file
        config = load_config_from_file()

        print("Loaded configuration from JSON file:")
        print(json.dumps(config, indent=2))

        # Validate the configuration using the SDK
        print("\nValidating configuration with SDK...")
        validated_config = SDKValidator.validate_config(config)

        print("\nConfiguration validation successful!")
        print("Validated Manifest:", validated_config['manifest'])

        if 'fee' in validated_config:
            print("Validated Fee:", validated_config['fee'])

        return True

    except ValidationError as e:
        print(f"\nConfiguration validation failed: {e}")
        return False
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        return False

if __name__ == "__main__":
    print("Starting SDK test with JSON configuration...")
    success = test_sdk_with_json_config()
    print("\nTest completed with", "SUCCESS" if success else "FAILURE")