# tests/test_user_manager.py
import pytest
from unittest.mock import AsyncMock, patch
from utils.user_manager import UserManager
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
async def test_user_registration(mock_user):
    """Test user registration functionality"""
    with patch('src.utils.user_manager.DatabaseManager') as mock_db_manager:
        mock_db = AsyncMock()
        mock_db_manager.return_value = mock_db
        mock_db.find_one.return_value = None
        mock_db.insert_one.return_value.inserted_id = "test_id"

        manager = UserManager(database_manager=mock_db_manager)
        result = await manager.register_user("test.eth", "USA")

        assert isinstance(result, UserModel)
        assert result.ens_name == "test.eth"
        mock_db.insert_one.assert_called_once()

@pytest.mark.asyncio
async def test_get_user(mock_user):
    """Test getting a user"""
    with patch('src.utils.user_manager.DatabaseManager') as mock_db_manager:
        mock_db = AsyncMock()
        mock_db_manager.return_value = mock_db
        mock_db.find_one.return_value = mock_user.model_dump()

        manager = UserManager(database_manager=mock_db_manager)
        result = await manager.get_user("test.eth")

        assert isinstance(result, UserModel)
        assert result.ens_name == "test.eth"
        mock_db.find_one.assert_called_once_with("users", {"ens_name": "test.eth"})

@pytest.mark.asyncio
async def test_update_user_profile(mock_user):
    """Test updating user profile"""
    with patch('src.utils.user_manager.DatabaseManager') as mock_db_manager:
        mock_db = AsyncMock()
        mock_db_manager.return_value = mock_db
        mock_db.update_one.return_value.modified_count = 1

        manager = UserManager(database_manager=mock_db_manager)
        result = await manager.update_user_profile("test.eth", {"display_name": "Test User"})

        assert result is True
        mock_db.update_one.assert_called_once()