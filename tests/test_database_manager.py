# tests/test_database_manager.py
import pytest
from unittest.mock import AsyncMock, patch
from src.utils.database_manager import DatabaseManager
from pymongo import AsyncMongoClient
from pymongo.collection import Collection

@pytest.mark.asyncio
async def test_database_connection():
    """Test database connection establishment"""
    with patch('src.utils.database_manager.AsyncMongoClient') as mock_client:
        mock_db = AsyncMock()
        mock_client.return_value = mock_db

        manager = DatabaseManager("mongodb://test")
        await manager.connect()

        assert manager.client is not None
        mock_client.assert_called_once_with("mongodb://test")

@pytest.mark.asyncio
async def test_get_database():
    """Test getting a database instance"""
    with patch('src.utils.database_manager.AsyncMongoClient') as mock_client:
        mock_db = AsyncMock()
        mock_client.return_value = mock_db

        manager = DatabaseManager("mongodb://test")
        db = await manager.get_database("test_db")

        assert db == mock_db["test_db"]
        assert "test_db" in manager._databases

@pytest.mark.asyncio
async def test_crud_operations():
    """Test basic CRUD operations"""
    with patch('src.utils.database_manager.AsyncMongoClient') as mock_client:
        mock_collection = AsyncMock(spec=Collection)
        mock_db = AsyncMock()
        mock_db.__getitem__.return_value = mock_collection
        mock_client.return_value = mock_db

        manager = DatabaseManager("mongodb://test")

        # Test insert
        mock_collection.insert_one.return_value.inserted_id = "test_id"
        result = await manager.insert_one("test_db", "test_collection", {"key": "value"})
        assert result == "test_id"

        # Test find
        mock_collection.find_one.return_value = {"key": "value"}
        result = await manager.find_one("test_db", "test_collection", {"key": "value"})
        assert result == {"key": "value"}

        # Test update
        mock_collection.update_one.return_value.modified_count = 1
        result = await manager.update_one("test_db", "test_collection", {"key": "value"}, {"$set": {"key": "new_value"}})
        assert result is True

        # Test delete
        mock_collection.delete_one.return_value.deleted_count = 1
        result = await manager.delete_one("test_db", "test_collection", {"key": "value"})
        assert result is True