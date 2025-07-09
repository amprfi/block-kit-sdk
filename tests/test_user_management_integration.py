# tests/test_integration.py
import pytest
from unittest.mock import AsyncMock, patch
from utils.user_manager import UserManager
from utils.profile_service import ProfileService
from utils.user_context import UserContextManager
from blocks.models import UserModel, UserProfile
from datetime import datetime, timezone

@pytest.mark.asyncio
async def test_full_user_flow():
    """Test the complete user management flow"""
    # Setup mock database
    mock_db = AsyncMock()
    mock_db.users = AsyncMock()

    # Create services
    user_manager = UserManager(database_manager=AsyncMock(return_value=mock_db))
    profile_service = ProfileService(user_manager)
    context_manager = UserContextManager(user_manager)

    # Test user registration
    new_user = await user_manager.register_user("test.eth", "USA")
    assert isinstance(new_user, UserModel)

    # Test profile update
    await profile_service.update_display_name("test.eth", "Test User")

    # Test context management
    async with context_manager.user_context("test.eth") as context:
        assert context.user.ens_name == "test.eth"
        assert context.is_active

    # Verify updates
    profile = await profile_service.get_user_profile("test.eth")
    assert profile.display_name == "Test User"