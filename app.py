# run_api.py
from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from api.routes.chat import chat_bp
from api.routes.history import history_bp
from api.routes.initialize import initialize_bp


def create_app():
    """Initialize and configure the Flask app."""
    app = Flask(__name__)
    app.secret_key = "super-secret-key"  # Change for production
    CORS(app, resources={r"/*": {"origins": "*"}})  # Active CORS pour toutes les routes

    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['API_TITLE'] = "Resume Matcher API"
    app.config['API_VERSION'] = 'v1'
    app.config['OPENAPI_VERSION'] = '3.0.3'
    app.config['OPENAPI_URL_PREFIX'] = '/'
    app.config['OPENAPI_SWAGGER_UI_PATH'] = '/swagger-ui'
    app.config['OPENAPI_SWAGGER_UI_URL'] = 'https://cdn.jsdelivr.net/npm/swagger-ui-dist/'
    app.config['JWT_SECRET_KEY'] = '258196649793219032652190028371592854149'

    api = Api(app)


    # Register blueprints
    api.register_blueprint(initialize_bp)
    api.register_blueprint(chat_bp)
    api.register_blueprint(history_bp)

    return app


if __name__ == '__main__':
    application = create_app()
    application.run(host='0.0.0.0', port=5000, debug=True)