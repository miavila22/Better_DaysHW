from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy #ORM (Object Relationa Mapper) remember this! 
from flask_login import UserMixin, LoginManager
from datetime import datetime
import uuid #PK primary key

#now we need to instantiate all our classes. Needs objects for database and login
db = SQLAlchemy()
login_manager = LoginManager()

@login_manager.user_loader
#function time for user_loader
def load_user(user_id):
    """
    Given *user_id*, return the associated User object

    """
    return User.query.get(user_id)

#Now a class for user that is ogin got to keep all information email, password, name, username, etc object=database object...
class User(db.Model, UserMixin):
    user_id = db.Column(db.String, primary_key=True)
    first_name = db.Column(db.String(30)) #the interger is like VARCHAR remember that. 
    last_name = db.Column(db.String(30))
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

#Now we INSERT INTO
    def __init__(self, username, email, password, first_name="", last_name=""):
        self.user_id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = self.set_password(password)

#Methods for attributes 
    def set_id(self):
        return str(uuid.uuid4())
    
    def get_id(self):
        return str(self.user_id)
    
    def set_password(self, password):
        return generate_password_hash(password)
    
    def __repr__(self):
        return f"<User: {self.username}>"

