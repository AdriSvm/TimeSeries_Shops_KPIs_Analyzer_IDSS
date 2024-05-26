import datetime
from app import db
from . import login_bp
from flask import request, jsonify, session, current_app
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from sqlalchemy.orm import Session
from app.models import User, Almacen
@login_bp.route("/register/", methods=["POST"])
@jwt_required()
def register():
    current_user = get_jwt_identity()
    sql_session = db.session

    user = sql_session.query(User).filter_by(fldIdUsuario=current_user).first()

    if not user or not user.is_admin():
        return jsonify({"msg": "Solo administradores pueden crear usuarios"}), 403


    data = request.json

    if not sql_session.query(Almacen).filter_by(fldIdAlmacen=data.get('idalmacen','0')).first():
        sql_session.close()
        return jsonify({"message": "Invalid warehouse"}), 400


    u_m = sql_session.query(User).filter_by(fldIdUsuario=data.get('username', None),fldIdGestion='PDAS').first()
    if u_m:
        u_m.fldIdAlmacen = data.get('idalmacen', u_m.fldIdAlmacen)
        u_m.fldIdNivelAcceso = '1111' if data.get('is_admin', True if u_m.fldIdNivelAcceso == '1111' else False) else '0000'
        u_m.fldIdClaveAcceso = data.get('password', u_m.fldIdClaveAcceso)

        sql_session.commit()
        sql_session.close()
        return jsonify({'message': 'User updated successfully'})

    new_user = User(
        fldIdUsuario=data.get('username',None),
        fldIdClaveAcceso=data.get('password',None),
        fldIdAlmacen=data.get('idalmacen',None),
        fldIdNivelAcceso='1111' if data.get('is_admin',False) else '0000',
        fldIdGestion='PDAS',
        fldGrabar=0,
        fldBorrar=0,
        fldTarifaVisible=0,
        fldBotonVentas=0
    )

    if not new_user.is_valid():
        print(new_user.to_dict())
        return jsonify({'message': 'Invalid user data'}), 400

    sql_session.add(new_user)
    sql_session.commit()
    sql_session.close()

    return jsonify({'message': 'User created successfully'}), 201


@login_bp.route("/login/", methods=["POST"])
def login():
    username = request.json.get("username")
    password = request.json.get("password")
    if not username or not password:
        return jsonify({"message": "Invalid username or password"}), 400

    sql_session = db.session
    user = sql_session.query(User).filter_by(fldIdGestion='PDAS',fldIdUsuario=username,fldIdClaveAcceso=password).first()
    if user:
        expires = datetime.timedelta(hours=8)
        access_token = create_access_token(identity=username,expires_delta=expires)
        is_admin = user.fldIdNivelAcceso == '1111'
        sql_session.close()
        return jsonify({"access_token": access_token,'is_admin':is_admin})
    sql_session.close()
    return jsonify({"message": "Invalid username or password"}), 401