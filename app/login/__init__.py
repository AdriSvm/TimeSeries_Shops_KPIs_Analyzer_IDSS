from flask import Blueprint
#from flask_cors import CORS

login_bp = Blueprint('login_bp',__name__,template_folder='templates')

#CORS(login_bp)
from . import routes