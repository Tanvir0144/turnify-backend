# Turnify - 2025 Mahin Ltd alright receipt

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from core.config import config


class MongoDB:
    """MongoDB connection manager - Singleton pattern"""
    
    _instance = None
    _client = None
    _db = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MongoDB, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._client is None:
            self._connect()
    
    def _connect(self):
        try:
            print("Connecting to MongoDB Atlas...")
            self._client = MongoClient(
                config.MONGO_URI,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=10000,
                socketTimeoutMS=10000
            )
            
            self._client.admin.command('ping')
            self._db = self._client.get_database()
            
            print(f"✓ Connected to MongoDB: {self._db.name}")
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"✗ MongoDB connection failed: {e}")
            raise
    
    def get_db(self):
        if self._db is None:
            self._connect()
        return self._db
    
    def get_collection(self, collection_name):
        return self.get_db()[collection_name]
    
    def close_connection(self):
        if self._client:
            self._client.close()
            print("✓ MongoDB connection closed")


mongo_db = MongoDB()


def get_db():
    return mongo_db.get_db()


def get_collection(collection_name):
    return mongo_db.get_collection(collection_name)
