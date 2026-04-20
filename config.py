import os
from dotenv import load_dotenv

load_dotenv()

class BaseConfig:
   SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")
   MONGO_DB = os.getenv("MONGO_DB", "artranking")

class DevelopmentConfig(BaseConfig):
   DEBUG = True
   MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/artranking")

class ProductionConfig(BaseConfig):
   DEBUG = False
   MONGO_URI = os.getenv("MONGO_URI")