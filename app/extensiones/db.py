from mongoengine import connect

def init_db(app):
   kwargs = {
       "db": app.config["MONGO_DB"],
       "host": app.config["MONGO_URI"]
   }
   
   # Add mongo_client_class for testing with mongomock
   if "MONGO_CLIENT_CLASS" in app.config:
       kwargs["mongo_client_class"] = app.config["MONGO_CLIENT_CLASS"]
   
   connect(**kwargs)