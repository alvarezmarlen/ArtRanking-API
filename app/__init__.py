from flask import Flask
from app.extensiones.db import db
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['MONGODB_SETTINGS'] = {
        'host': os.getenv('MONGO_URI')
    }
    
    # Inicializar extensiones
    db.init_app(app)
    
    @app.route('/')
    def index():
        return "SERVIDOR FUNCIONANDO"
        
    return app