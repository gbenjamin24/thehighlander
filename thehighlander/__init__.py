from flask import Flask
from .views import app
from .api import api

app.register_blueprint(api, url_prefix="/api")