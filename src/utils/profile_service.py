# src/utils/profile_service.py
from typing import Optional, Dict, Any
from blocks.models import UserModel, UserProfile
from utils.user_manager import UserManager
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class ProfileService:
    """Service for managing user profile information"""

    def __init__(self, user_manager: UserManager):
        """
        Initialize the profile service

        Args:
            user_manager: UserManager instance for database operations
        """
        self.user_manager = user_manager

    async def get_user_profile(self, ens_name: str) -> Optional[UserProfile]:
        """
        Retrieve a user's profile information

        Args:
            ens_name: User's ENS name

        Returns:
            UserProfile if found, None otherwise
        """
        user = await self.user_manager.get_user(ens_name)
        if user:
            return user.profile
        return None

    async def update_user_profile(
        self,
        ens_name: str,
        profile_data: Dict[str, Any]
    ) -> bool:
        """
        Update a user's profile information

        Args:
            ens_name: User's ENS name
            profile_data: Dictionary containing profile updates

        Returns:
            True if update was successful, False otherwise
        """
        # Get current user to validate
        user = await self.user_manager.get_user(ens_name)
        if not user:
            logger.error(f"User {ens_name} not found for profile update")
            return False

        # Create updated profile by merging existing with new data
        updated_profile = user.profile.model_copy(update=profile_data)

        # Update in database
        return await self.user_manager.update_user_profile(ens_name, updated_profile.model_dump())

    async def update_display_name(self, ens_name: str, display_name: str) -> bool:
        """
        Update a user's display name

        Args:
            ens_name: User's ENS name
            display_name: New display name

        Returns:
            True if update was successful, False otherwise
        """
        return await self.update_user_profile(ens_name, {"display_name": display_name})

    async def update_language(self, ens_name: str, language: str) -> bool:
        """
        Update a user's language preference

        Args:
            ens_name: User's ENS name
            language: New language code

        Returns:
            True if update was successful, False otherwise
        """
        return await self.update_user_profile(ens_name, {"language": language})

    async def update_notification_settings(
        self,
        ens_name: str,
        notification_settings: Dict[str, Any]
    ) -> bool:
        """
        Update a user's notification settings

        Args:
            ens_name: User's ENS name
            notification_settings: Dictionary of notification settings

        Returns:
            True if update was successful, False otherwise
        """
        return await self.update_user_profile(ens_name, {"notifications": notification_settings})

    async def update_privacy_settings(
        self,
        ens_name: str,
        privacy_settings: Dict[str, bool]
    ) -> bool:
        """
        Update a user's privacy settings

        Args:
            ens_name: User's ENS name
            privacy_settings: Dictionary of privacy settings

        Returns:
            True if update was successful, False otherwise
        """
        return await self.update_user_profile(ens_name, {"privacy_settings": privacy_settings})

    async def get_profile_field(
        self,
        ens_name: str,
        field_name: str
    ) -> Optional[Any]:
        """
        Get a specific field from a user's profile

        Args:
            ens_name: User's ENS name
            field_name: Name of the field to retrieve

        Returns:
            The requested field value if found, None otherwise
        """
        profile = await self.get_user_profile(ens_name)
        if profile:
            return getattr(profile, field_name, None)
        return None