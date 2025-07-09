# src/utils/database_manager.py
from typing import Optional, Dict, Any, List, TypeVar, Generic
from pymongo import AsyncMongoClient
from pymongo.collection import Collection
from pymongo.database import Database
import logging
from datetime import datetime, timezone
from bson import ObjectId

logger = logging.getLogger(__name__)

# Generic type for document conversion
T = TypeVar('T')

class DatabaseManager:
    """
    Manages database connections and operations using PyMongo Async API.
    Provides a centralized way to handle database connections across the application.
    """

    def __init__(self, mongo_uri: str = "mongodb://localhost:27017"):
        """
        Initialize the database manager.

        Args:
            mongo_uri: MongoDB connection URI
        """
        self.mongo_uri = mongo_uri
        self.client: Optional[AsyncMongoClient] = None
        self._databases: Dict[str, Database] = {}

    async def connect(self) -> AsyncMongoClient:
        """
        Establish a connection to MongoDB using PyMongo Async API.

        Returns:
            The connected AsyncMongoClient instance
        """
        if not self.client:
            self.client = AsyncMongoClient(self.mongo_uri)
            logger.info("Established MongoDB connection using PyMongo Async API")
        return self.client

    async def get_database(self, db_name: str) -> Database:
        """
        Get a database instance. Creates a connection if one doesn't exist.

        Args:
            db_name: Name of the database to retrieve

        Returns:
            The requested Database instance
        """
        if not self.client:
            await self.connect()

        if db_name not in self._databases:
            self._databases[db_name] = self.client[db_name]
            logger.debug(f"Retrieved database: {db_name}")

        return self._databases[db_name]

    async def get_collection(self, db_name: str, collection_name: str) -> Collection:
        """
        Get a collection from a specific database.

        Args:
            db_name: Name of the database
            collection_name: Name of the collection

        Returns:
            The requested Collection instance
        """
        db = await self.get_database(db_name)
        return db[collection_name]

    async def create_indexes(self, db_name: str, collection_name: str, indexes: List[Dict]) -> None:
        """
        Create indexes on a collection.

        Args:
            db_name: Name of the database
            collection_name: Name of the collection
            indexes: List of index specifications
        """
        collection = await self.get_collection(db_name, collection_name)
        for index in indexes:
            keys = index["keys"]
            options = index.get("options", {})
            await collection.create_index(keys, **options)
            logger.info(f"Created index on {collection_name}: {keys}")

    async def insert_one(self, db_name: str, collection_name: str, document: Dict) -> str:
        """
        Insert a single document into a collection.

        Args:
            db_name: Name of the database
            collection_name: Name of the collection
            document: Document to insert

        Returns:
            The inserted document's ID
        """
        collection = await self.get_collection(db_name, collection_name)
        result = await collection.insert_one(document)
        return str(result.inserted_id)

    async def insert_many(self, db_name: str, collection_name: str, documents: List[Dict]) -> List[str]:
        """
        Insert multiple documents into a collection.

        Args:
            db_name: Name of the database
            collection_name: Name of the collection
            documents: List of documents to insert

        Returns:
            List of inserted document IDs
        """
        collection = await self.get_collection(db_name, collection_name)
        result = await collection.insert_many(documents)
        return [str(id) for id in result.inserted_ids]

    async def find_one(self, db_name: str, collection_name: str, query: Dict) -> Optional[Dict]:
        """
        Find a single document in a collection.

        Args:
            db_name: Name of the database
            collection_name: Name of the collection
            query: Query to execute

        Returns:
            The found document or None
        """
        collection = await self.get_collection(db_name, collection_name)
        return await collection.find_one(query)

    async def find(self, db_name: str, collection_name: str, query: Dict = None) -> List[Dict]:
        """
        Find multiple documents in a collection.

        Args:
            db_name: Name of the database
            collection_name: Name of the collection
            query: Query to execute (defaults to all documents)

        Returns:
            List of found documents
        """
        collection = await self.get_collection(db_name, collection_name)
        cursor = collection.find(query or {})
        return await cursor.to_list(None)

    async def update_one(self, db_name: str, collection_name: str, query: Dict, update: Dict) -> bool:
        """
        Update a single document in a collection.

        Args:
            db_name: Name of the database
            collection_name: Name of the collection
            query: Query to select the document
            update: Update to apply

        Returns:
            True if a document was updated, False otherwise
        """
        collection = await self.get_collection(db_name, collection_name)
        result = await collection.update_one(query, {"$set": update})
        return result.modified_count > 0

    async def update_many(self, db_name: str, collection_name: str, query: Dict, update: Dict) -> int:
        """
        Update multiple documents in a collection.

        Args:
            db_name: Name of the database
            collection_name: Name of the collection
            query: Query to select documents
            update: Update to apply

        Returns:
            Number of documents updated
        """
        collection = await self.get_collection(db_name, collection_name)
        result = await collection.update_many(query, {"$set": update})
        return result.modified_count

    async def delete_one(self, db_name: str, collection_name: str, query: Dict) -> bool:
        """
        Delete a single document from a collection.

        Args:
            db_name: Name of the database
            collection_name: Name of the collection
            query: Query to select the document

        Returns:
            True if a document was deleted, False otherwise
        """
        collection = await self.get_collection(db_name, collection_name)
        result = await collection.delete_one(query)
        return result.deleted_count > 0

    async def delete_many(self, db_name: str, collection_name: str, query: Dict) -> int:
        """
        Delete multiple documents from a collection.

        Args:
            db_name: Name of the database
            collection_name: Name of the collection
            query: Query to select documents

        Returns:
            Number of documents deleted
        """
        collection = await self.get_collection(db_name, collection_name)
        result = await collection.delete_many(query)
        return result.deleted_count

    async def close(self) -> None:
        """Close the database connection"""
        if self.client:
            self.client.close()
            self.client = None
            self._databases = {}
            logger.info("Closed MongoDB connection")