from src.infra.server import app
from src.infra.config.settings import settings


if __name__ == "__main__":
    print(f"Starting {settings.APP_NAME}")
    print(f"Running on port {settings.APP_PORT}")
    print(f"Environment: {settings.APP_ENV}")
    app.run(host=settings.APP_HOST, port=settings.APP_PORT)

