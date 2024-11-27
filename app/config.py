import os
from pathlib import Path

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    BASE_DIR = Path(__file__).resolve().parent
    UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
    ALLOWED_EXTENSIONS = {'pdf'}
    
    @staticmethod
    def init_app(app):
        # Ensure upload directory exists
        upload_dir = Config.UPLOAD_FOLDER
        if not upload_dir.exists():
            upload_dir.mkdir(parents=True, exist_ok=True)
        return app