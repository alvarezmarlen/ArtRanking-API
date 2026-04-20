from flask import Flask
from config import DevelopmentConfig
from app.extensiones.db import init_db
from mongoengine.connection import get_db

def create_app(config_class=DevelopmentConfig):
   app = Flask(__name__)
   app.config.from_object(config_class)

   # Inicializar DB
   init_db(app)

   @app.route("/")
   def home():
       return {"message": "ArtRanking API running"}
    
   @app.route("/test-db")
   def test_db():
      db = get_db()
      collections = db.list_collection_names()
      return {"collections": collections}

   return app