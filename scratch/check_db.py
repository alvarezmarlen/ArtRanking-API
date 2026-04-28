
import os
from mongoengine import connect
from app.models.envio import Envio
from app.models.usuario import Usuario
from app.models.concurso import Concurso
from mongoengine.errors import DoesNotExist

# Try to connect using the URI if available in environment, or default local
mongo_uri = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/artranking') # Adjust DB name if needed
connect(host=mongo_uri)


print(f"Total envios: {Envio.objects.count()}")

obras_query = Envio.objects().order_by('-votos').limit(10)
count_valid = 0
for o in obras_query:
    try:
        # Check if autor and concurso exist by trying to access them
        autor_exists = o.autor is not None
        concurso_exists = o.concurso is not None
        
        if autor_exists and concurso_exists:
            print(f"Valid: {o.titulo} (Votos: {o.votos}) - Autor: {o.autor.email} - Concurso: {o.concurso.titulo}")
            count_valid += 1
        else:
            print(f"Invalid (null ref): {o.titulo} - Autor: {autor_exists}, Concurso: {concurso_exists}")
    except DoesNotExist:
        print(f"Invalid (DoesNotExist): {o.titulo}")

print(f"Valid count in top 10: {count_valid}")
