from typing import Dict, Optional, List
from pydantic import BaseModel
import logging
from datetime import datetime, timezone
from blocks.models import UserModel, UserProfile
from utils.database_manager import DatabaseManager

logger = logging.getLogger(__name__)

class UserManager:
    """Handles user registration and management for the Ampr wallet system"""

    def __init__(self, database_manager: Optional[DatabaseManager] = None, database_name: str = "ampr_users"):
        """
        Initialize the user manager

        Args:
            database_manager: Optional DatabaseManager instance
            database_name: Name of the database to use
        """
        self.db_manager = database_manager or DatabaseManager()
        self.database_name = database_name

    async def initialize(self):
        """Initialize indexes and ensure database connection"""
        await self._create_indexes()

    async def _create_indexes(self):
        """Create necessary database indexes"""
        indexes = [
            {"keys": [("ens_name", 1)], "options": {"unique": True}},
            {"keys": [("jurisdiction", 1)]},
            {"keys": [("last_login", 1)]}
        ]
        await self.db_manager.create_indexes(self.database_name, "users", indexes)

    async def register_user(self, ens_name: str, jurisdiction: str) -> UserModel:
        """
        Register a new user with the system

        Args:
            ens_name: User's ENS name
            jurisdiction: User's jurisdiction (country code)

        Returns:
            The registered UserModel object
        """
        # Check if user already exists
        existing_user = await self.db_manager.find_one(
            self.database_name, "users", {"ens_name": ens_name}
        )
        if existing_user:
            logger.info(f"User {ens_name} already registered")
            return UserModel(**existing_user)

        # Create new user record
        new_user = UserModel(
            ens_name=ens_name,
            last_login=datetime.now(timezone.utc),
            jurisdiction=jurisdiction
        )

        # Store in database
        await self.db_manager.insert_one(
            self.database_name, "users", new_user.model_dump()
        )
        logger.info(f"Registered new user {ens_name}")

        return new_user

    async def get_user(self, ens_name: str) -> Optional[UserModel]:
        """
        Retrieve a user by ENS name

        Args:
            ens_name: User's ENS name

        Returns:
            UserModel if found, None otherwise
        """
        user_data = await self.db_manager.find_one(
            self.database_name, "users", {"ens_name": ens_name}
        )
        if user_data:
            return UserModel(**user_data)
        return None

    async def update_user_profile(self, ens_name: str, profile_data: Dict) -> bool:
        """
        Update a user's profile information

        Args:
            ens_name: User's ENS name
            profile_data: Dictionary of profile updates

        Returns:
            True if update was successful, False otherwise
        """
        return await self.db_manager.update_one(
            self.database_name,
            "users",
            {"ens_name": ens_name},
            {"profile": profile_data}
        )

    async def update_last_login(self, ens_name: str) -> bool:
        """
        Update a user's last login timestamp

        Args:
            ens_name: User's ENS name

        Returns:
            True if update was successful, False otherwise
        """
        return await self.db_manager.update_one(
            self.database_name,
            "users",
            {"ens_name": ens_name},
            {"last_login": datetime.now(timezone.utc)}
        )

    async def get_users_by_jurisdiction(self, jurisdiction: str) -> List[UserModel]:
        """
        Retrieve all users from a specific jurisdiction

        Args:
            jurisdiction: Jurisdiction (country code) to filter by

        Returns:
            List of UserModel objects
        """
        users_data = await self.db_manager.find(
            self.database_name, "users", {"jurisdiction": jurisdiction}
        )
        return [UserModel(**user) for user in users_data]

    async def close(self):
        """Close the database connection"""
        await self.db_manager.close()