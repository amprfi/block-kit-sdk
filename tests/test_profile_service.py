import pytest
from unittest.mock import AsyncMock, patch
from utils.profile_service import ProfileService
from blocks.models import UserProfile

@pytest.mark.asyncio
async def test_profile_operations():
    """Test profile service operations"""
    with patch('src.utils.profile_service.UserManager') as mock_user_manager:
        mock_manager = AsyncMock()
        mock_user_manager.return_value = mock_manager

        # Setup mock user data
        mock_user = AsyncMock()
        mock_user.profile = UserProfile(display_name="Old Name")
        mock_manager.get_user.return_value = mock_user

        service = ProfileService(mock_user_manager)

        # Test get profile
        profile = await service.get_user_profile("test.eth")
        assert profile.display_name == "Old Name"

        # Test update display name
        await service.update_display_name("test.eth", "New Name")
        mock_manager.update_user_profile.assert_called_once_with(
            "test.eth", {"display_name": "New Name"}
        )

        # Test get specific field
        field = await service.get_profile_field("test.eth", "display_name")
        assert field == "Old Name"