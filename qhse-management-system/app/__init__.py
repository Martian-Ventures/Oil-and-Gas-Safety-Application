import os
from flask import Flask, url_for, redirect
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") or "dev-secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # Add these Flask-Login configurations
    app.config['REMEMBER_COOKIE_DURATION'] = 3600  # 1 hour
    app.config['SESSION_PROTECTION'] = 'basic'
    

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    # Blueprints
    from app.auth.routes import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')   

    from .main.routes import bp as main_bp
    app.register_blueprint(main_bp)
    
    #from app.incidents.routes import incidents_bp
    #app.register_blueprint(incidents_bp, url_prefix='/incidents')
    
    from app.admin.routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # simple index/dashboard
    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for('main.dashboard'))  # ✅ Use url_for
        return redirect(url_for('auth.register'))  # ✅ Use url_for

    return app

if __name__ == "__main__":
    create_app().run(debug=True)
