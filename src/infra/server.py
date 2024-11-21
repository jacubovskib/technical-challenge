from flask import Flask
from src.infra.api.routes.user.user_routes import UserRoutes
app = Flask(__name__)

app.register_blueprint(UserRoutes().get_blueprint())