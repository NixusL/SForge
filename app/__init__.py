from flask import Flask
from pathlib import Path

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-key"  # change later if you like

    # Folder for uploaded PDFs
    upload_folder = Path("uploads").absolute()
    upload_folder.mkdir(parents=True, exist_ok=True)
    app.config["UPLOAD_FOLDER"] = str(upload_folder)

    # Register routes
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app