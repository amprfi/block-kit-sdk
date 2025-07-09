import pytest
from unittest.mock import AsyncMock, patch
from utils.user_context import UserContext, UserContextManager
from blocks.models import UserModel, UserProfile
from datetime import datetime, timezone

@pytest.fixture
def mock_user():
    return UserModel(
        ens_name="test.eth",
        registration_date=datetime.now(timezone.utc),
        last_login=datetime.now(timezone.utc),
        profile=UserProfile(),
        jurisdiction="USA"
    )

@pytest.mark.asyncio
async def test_user_context_lifecycle(mock_user):
    """Test user context lifecycle management"""
    with patch('src.utils.user_context.UserManager') as mock_user_manager:
        mock_manager = AsyncMock()
        mock_user_manager.return_value = mock_manager
        mock_manager.get_user.return_value = mock_user

        manager = UserContextManager(mock_user_manager)
        async with manager.user_context("test.eth") as context:
            assert context.is_active
            assert context.user.ens_name == "test.eth"

        assert not context.is_active

@pytest.mark.asyncio
async def test_additional_context(mock_user):
    """Test adding additional context"""
    with patch('src.utils.user_context.UserManager') as mock_user_manager:
        mock_manager = AsyncMock()
        mock_user_manager.return_value = mock_manager
        mock_manager.get_user.return_value = mock_user

        manager = UserContextManager(mock_user_manager)

        async def setup_context(context):
            context.add_context("test_key", "test_value")

        async with manager.with_additional_context("test.eth", setup_context) as context:
            assert context.get_context("test_key") == "test_value"