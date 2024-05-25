from datetime import datetime,timedelta
import logging

from app import db
from . import timeseries_bp
from flask import request, jsonify, session, current_app
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from sqlalchemy.orm import Session
from app.models import User, Cliente,TiquetLinea,TiquetCabecera
from .models import TimeSeries

@timeseries_bp.route("/get_info", methods=["GET"])
@jwt_required()
def timeseries_info():
    logger = logging.getLogger(__name__)
    logger.debug(f"Getting timeseries...")

    current_user = get_jwt_identity()

    sql_session = db.session

    user = sql_session.query(User).filter_by(fldIdUsuario=current_user).first()

    min_date = request.args.get('min_date', None)
    max_date = request.args.get('max_date', None)

    try:
        min_date = datetime.strptime(min_date, '%Y-%m-%d') if min_date else None
        max_date = datetime.strptime(max_date, '%Y-%m-%d') if max_date else None
    except ValueError as e:
        logger.error(f"Error parsing dates: {e}")
        return jsonify({"message": "Invalid date format"}), 400

    t = TimeSeries(sql_session,min_date,max_date)

    return jsonify({'status':'ok'})