from flask_security import SQLAlchemyUserDatastore
from application.models import db, Users, Role

user_datastore = SQLAlchemyUserDatastore(db, Users, Role)
