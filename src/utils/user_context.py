# src/utils/user_context.py
from typing import Optional, AsyncGenerator, Dict, Any, Callable, Awaitable
from blocks.models import UserModel
from utils.user_manager import UserManager
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

class UserContext:
    """Class to hold and manage user context information"""

    def __init__(self, user: UserModel, user_manager: UserManager):
        """
        Initialize the user context with user information

        Args:
            user: The user model containing all user information
            user_manager: The user manager instance
        """
        self.user = user
        self.user_manager = user_manager
        self._is_active = False
        self._start_time = None
        self._additional_context = {}

    async def activate(self):
        """Activate the user context"""
        self._is_active = True
        self._start_time = datetime.now(timezone.utc)
        logger.debug(f"Activated user context for {self.user.ens_name}")

    async def deactivate(self):
        """Deactivate the user context"""
        self._is_active = False
        duration = datetime.now(timezone.utc) - self._start_time
        logger.debug(f"Deactivated user context for {self.user.ens_name} after {duration.total_seconds()} seconds")

    @property
    def is_active(self) -> bool:
        """Check if the context is active"""
        return self._is_active

    @property
    def session_duration(self) -> Optional[float]:
        """Get the duration of the current session in seconds"""
        if not self._start_time:
            return None
        return (datetime.now(timezone.utc) - self._start_time).total_seconds()

    def add_context(self, key: str, value: Any):
        """Add additional context information"""
        self._additional_context[key] = value

    def get_context(self, key: str) -> Optional[Any]:
        """Get additional context information"""
        return self._additional_context.get(key)

    async def update_last_login(self):
        """Update the user's last login timestamp"""
        if self._is_active:
            await self.user_manager.update_last_login(self.user.ens_name)
            logger.debug(f"Updated last login for {self.user.ens_name}")

class UserContextManager:
    """Manages user context lifecycle for block operations"""

    def __init__(self, user_manager: UserManager):
        """
        Initialize the user context manager

        Args:
            user_manager: The user manager instance
        """
        self.user_manager = user_manager

    @asynccontextmanager
    async def user_context(self, ens_name: str) -> AsyncGenerator[UserContext, None]:
        """
        Context manager for handling user context within a block

        Args:
            ens_name: The ENS name of the user

        Yields:
            An active UserContext instance

        Raises:
            ValueError: If the user is not found
        """
        # Get the user from the database
        user = await self.user_manager.get_user(ens_name)
        if not user:
            logger.error(f"User {ens_name} not found")
            raise ValueError(f"User {ens_name} not found")

        # Create and activate the user context
        context = UserContext(user, self.user_manager)
        await context.activate()

        try:
            yield context
        finally:
            await context.deactivate()
            await context.update_last_login()

    async def with_additional_context(
        self,
        ens_name: str,
        context_setup: Callable[['UserContext'], Awaitable[None]]
    ) -> AsyncGenerator[UserContext, None]:
        """
        Context manager that allows for additional context setup after initialization

        Args:
            ens_name: The ENS name of the user
            context_setup: Async function that takes a UserContext and adds additional context

        Yields:
            A fully configured UserContext instance
        """
        async with self.user_context(ens_name) as context:
            await context_setup(context)
            yield context