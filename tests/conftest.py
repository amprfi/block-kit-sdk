import pytest
from unittest.mock import AsyncMock
from pymongo import AsyncMongoClient

@pytest.fixture
def mock_mongo_client():
    """Fixture for mock MongoDB client"""
    return AsyncMock(spec=AsyncMongoClient)

@pytest.fixture
def mock_user_manager(mock_mongo_client):
    """Fixture for mock UserManager"""
    from src.utils.user_manager import UserManager
    return UserManager(database_manager=AsyncMock(return_value=mock_mongo_client))