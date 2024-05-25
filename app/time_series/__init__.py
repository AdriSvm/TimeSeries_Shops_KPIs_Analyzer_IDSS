from flask import Blueprint
#from flask_cors import CORS

timeseries_bp = Blueprint('timeseries_bp',__name__,template_folder='templates')

#CORS(login_bp)
from . import routes