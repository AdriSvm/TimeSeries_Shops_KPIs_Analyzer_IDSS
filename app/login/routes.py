import datetime
from app import db
from . import login_bp
from flask import request, jsonify, session, current_app
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from sqlalchemy.orm import Session
from app.models import User, Almacen
@login_bp.route("/register", methods=["POST"])
@jwt_required()
def register():
    current_user = get_jwt_identity()
    sql_session = db.session

    user = sql_session.query(User).filter_by(fldIdUsuario=current_user).first()

    if not user or not user.is_admin():
        return jsonify({"msg": "Solo administradores pueden crear usuarios"}), 403

    username = request.json.get("username")
    password = request.json.get("password")
    idalmacen = request.json.get("idalmacen")
    is_admin = request.json.get("is_admin",False)
    if not username or not password or len(username) != 6:
        sql_session.close()
        return jsonify({"message": "Invalid username or password"}), 400

    if sql_session.query(User).filter_by(fldIdGestion='PDAS',fldIdUsuario=username).first() is not None:
        sql_session.close()
        return jsonify({"message": "Username already exists"}), 400

    if not sql_session.query(Almacen).filter_by(fldIdAlmacen=idalmacen).first():
        sql_session.close()
        return jsonify({"message": "Invalid warehouse"}), 400

    new_user = User(fldIdGestion='PDAS',fldIdUsuario=username,fldIdAlmacen=idalmacen,fldIdClaveAcceso=password,
                    fldIdNivelAcceso='1111' if is_admin else '0000', fldGrabar=0,fldBorrar=0,fldTarifaVisible=0,
                    fldBotonVentas=0)
    sql_session.add(new_user)
    sql_session.commit()
    sql_session.close()

    return jsonify({"message": "User registered successfully"})

@login_bp.route("/login", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    if not username or not password:
        return jsonify({"message": "Invalid username or password"}), 400

    sql_session = db.session
    if sql_session.query(User).filter_by(fldIdGestion='PDAS',fldIdUsuario=username,fldIdClaveAcceso=password).first() is not None:
        expires = datetime.timedelta(hours=8)
        access_token = create_access_token(identity=username,expires_delta=expires)
        sql_session.close()
        return jsonify({"access_token": access_token})
    sql_session.close()
    return jsonify({"message": "Invalid username or password"}), 401