"""
MongoDB database connection module using Motor (async driver).
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "chl_datastore_db"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()

# Global MongoDB client instance
client: Optional[AsyncIOMotorClient] = None


async def connect_to_mongo():
    """Create database connection."""
    global client
    try:
        client = AsyncIOMotorClient(settings.mongodb_url)
        # Test the connection
        await client.admin.command('ping')
        print(f"Connected to MongoDB: {settings.mongodb_url}")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise


async def close_mongo_connection():
    """Close database connection."""
    global client
    if client:
        client.close()
        print("MongoDB connection closed")


def get_database():
    """Get database instance."""
    if client is None:
        raise RuntimeError("Database connection not initialized")
    return client[settings.database_name]
