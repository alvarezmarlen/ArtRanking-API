from mongoengine import connect

def init_db(app):
   connect(
       db=app.config["MONGO_DB"],
       host=app.config["MONGO_URI"]
   )