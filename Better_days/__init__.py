#External imports
from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager


#Internal imports
from .blueprints.site.routes import site
from .blueprints.authentication.routes import authentication
from .blueprints.api.routes import api
from config import Config
from .models import login_manager, db
from .helpers import JSONEncoder

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

#Wrapping time. This needs to happen so we can use it wherever we want in our app.
login_manager.init_app(app)
login_manager.login_view = 'authentication.sign_in'
login_manager.login_message = 'Login Please! Thanks!'
login_manager.login_message_category = 'warning'


app.register_blueprint(site)
app.register_blueprint(authentication)
app.register_blueprint(api)

#Instantiating our database & wrapping our app
db.init_app(app)
migrate = Migrate(app,db)
app.json_encoder = JSONEncoder
cors = CORS(app)
