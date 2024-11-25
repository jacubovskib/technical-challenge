from dotenv import load_dotenv
import os
import pathlib

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
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///database/storage')

    # API
    API_VERSION = os.getenv('API_VERSION', 'v1')
    API_PREFIX = os.getenv('API_PREFIX', '/api')

    # Security
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-super-secret-key-here')
    JWT_EXPIRATION_MINUTES = int(os.getenv('JWT_EXPIRATION_MINUTES', 60))

    def set_test_database(self):
        self.DATABASE_URL = "sqlite:///:memory:"

    def ensure_database_directory(self):
        if 'sqlite' in self.DATABASE_URL and '/:memory:' not in self.DATABASE_URL:
            db_path = self.DATABASE_URL.replace('sqlite:///', '')
            directory = os.path.dirname(db_path)
            pathlib.Path(directory).mkdir(parents=True, exist_ok=True)


settings = Settings()
settings.ensure_database_directory()