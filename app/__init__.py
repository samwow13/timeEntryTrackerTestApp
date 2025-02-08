from flask import Flask
from flask_login import LoginManager

def create_app():
    """
    Create and configure the Flask application
    
    Returns:
        Flask: Configured Flask application instance
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    # Register the time entries API blueprint
    from .api.time_entries import bp as time_entries_blueprint
    app.register_blueprint(time_entries_blueprint)
    
    return app
