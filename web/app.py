# flask create app
# Author : Ji-yong219
# Project Start:: 2021.07.30
# Last Modified from Ji-yong 2021.07.30

from flask import Flask
from .views import views
import os

def create_app():
    app = Flask(__name__)
    app.register_blueprint(views)
    app.secret_key = "asS0Sallic4ntwa1t"
    
    # UPLOAD_FOLDER = os.getcwd() + r'\web\static\org_image'
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    return app