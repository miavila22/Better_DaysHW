#External imports
from flask import Flask
from flask_migrate import Migrate


#Internal imports
from .blueprints.site.routes import site
from .blueprints.authentication.routes import authentication
from config import Config
from .models import login_manager, db

app = Flask(__name__)
app.config.from_object(Config)

#Wrapping time. This needs to happen so we can use it wherever we want in our app.
login_manager.init_app(app)
login_manager.login_view = 'authentication.sign_in'
login_manager.login_message = 'Login Please! Thanks!'
login_manager.login_message_category = 'warning'


app.register_blueprint(site)
app.register_blueprint(authentication)

#Instantiating our database & wrapping our app
db.init_app(app)
migrate = Migrate(app,db)