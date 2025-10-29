# Here's a comprehensive line-by-line explanation of your Pydantic Settings configuration class for managing application settings and environment variables:
from typing import ClassVar
import redis.asyncio as redis
from pydantic_settings import BaseSettings, SettingsConfigDict
# ClassVar: Type hint indicating a class variable (not an instance variable)
# redis.asyncio as redis: Async Redis client for non-blocking operations
# BaseSettings: Pydantic's base class for settings management with environment variable support
# SettingsConfigDict: Configuration dictionary for settings behavior
#=================================================================================================================================
class Settings(BaseSettings):
# class Settings(BaseSettings): Inherits from Pydantic's BaseSettings for automatic environment variable loading
# Key benefit: Automatically reads values from environment variables and .env files
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
# Line-by-line breakdown:
# DATABASE_URL: str: Required field - PostgreSQL connection string from environment
# JWT_SECRET: str: Required field - Secret key for JWT token signing
# JWT_ALGORITHM: str: Required field - JWT signing algorithm (e.g., "HS256")
# REDIS_HOST: str = "localhost": Optional field with default - Redis server host
# REDIS_PORT: int = 6379: Optional field with default - Redis server port
# Environment variable mapping:
# Pydantic automatically looks for DATABASE_URL, JWT_SECRET, etc. in environment variables
# Case-insensitive: Can use database_url or DATABASE_URL in .env file
#=================================================================================================================================
    redis_client: ClassVar[redis.Redis] = redis.from_url("redis://localhost:6379")
# Line-by-line breakdown:
# redis_client: ClassVar[redis.Redis]: Class variable - shared across all instances
# ClassVar: Tells Pydantic this is NOT a setting field, but a class-level attribute
# redis.from_url("redis://localhost:6379"): Creates Redis client from connection URL
# Purpose: Provides a ready-to-use Redis client for the application
# Why ClassVar?
# Not a setting: This isn't loaded from environment variables
# Shared resource: Single Redis connection pool shared by all parts of the app
# Pydantic exclusion: ClassVar fields are ignored during settings validation
#================================================================================================================================
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
# Line-by-line breakdown:
# model_config = SettingsConfigDict(...):
# model_config: Pydantic v2 way to configure model behavior
# SettingsConfigDict: Specialized configuration for settings classes
# Configuration Options:
# env_file=".env": Loads environment variables from .env file
# Automatically reads key-value pairs from .env file in current directory
# Priority: Environment variables override .env file values
# Example: If .env contains DATABASE_URL=..., it gets loaded automatically
# extra="ignore": Ignores extra fields in .env file that don't match class fields
# Without this: Pydantic would raise validation errors for unknown fields
# With this: Unknown environment variables are silently ignored
# Benefit: Clean separation between app settings and other environment variables
#=====================================================================================================================
Config = Settings()
# Config = Settings(): Creates a singleton instance of the settings class
# Automatic loading: When instantiated, Pydantic automatically:
# Reads system environment variables
# Loads values from .env file
# Applies defaults for missing optional fields
# Validates all field types
# Raises errors for missing required fields