from flask import Flask
from .blueprints.site.routes import site

app = Flask(__name__)

app.register_blueprint(site)