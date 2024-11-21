from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class Settings:
    # Application
    APP_NAME = os.getenv('APP_NAME', 'PicPay Challenge')
    APP_ENV = os.getenv('APP_ENV', 'development')
    APP_DEBUG = os.getenv('APP_DEBUG', 'True').lower() == 'true'
    APP_PORT = int(os.getenv('APP_PORT', 8000))
    APP_HOST = os.getenv('APP_HOST', '0.0.0.0')
    # Database
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///data/data.sqlite3')

    # API
    API_VERSION = os.getenv('API_VERSION', 'v1')
    API_PREFIX = os.getenv('API_PREFIX', '/api')

    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-super-secret-key-here')
    JWT_EXPIRATION_MINUTES = int(os.getenv('JWT_EXPIRATION_MINUTES', 60))


settings = Settings()
