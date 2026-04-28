import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
   SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
   MONGO_DB = os.getenv("MONGO_DB", "artranking")
   
   # Configuración de subida de archivos
   UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app/static/uploads')
   ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}
   MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max

class DevelopmentConfig(BaseConfig):
   DEBUG = True
   MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/artranking")

class ProductionConfig(BaseConfig):
   DEBUG = False
   MONGO_URI = os.getenv("MONGO_URI")