from app import db
from . import admin_bp
from flask import request, jsonify, session, current_app
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from sqlalchemy.orm import Session
from app.models import User
@admin_bp.route('/get_users/', methods=['GET'])
@jwt_required()
def get_users():
    current_user = get_jwt_identity()
    sql_session = db.session

    user = sql_session.query(User).filter_by(fldIdUsuario=current_user).first()

    if not user or not user.is_admin():
        return jsonify({"msg": "Solo administradores pueden crear usuarios"}), 403

    users = sql_session.query(User).filter_by(fldIdGestion='PDAS').all()
    users = [u.to_dict() for u in users]
    sql_session.close()

    return jsonify({'users': users})

# Función para eliminar un usuario existente
@admin_bp.route('/delete_user/', methods=['POST'])
@jwt_required()
def delete_user():
    current_user = get_jwt_identity()
    sql_session = db.session

    user = sql_session.query(User).filter_by(fldIdUsuario=current_user).first()

    if not user or not user.is_admin():
        return jsonify({"msg": "Solo administradores pueden eliminar usuarios"}), 403

    if user.fldIdUsuario == request.json.get('username'):
        return jsonify({'message': 'Cannot delete yourself'}), 400

    u = sql_session.query(User).filter_by(fldIdUsuario=request.json.get('username'),fldIdGestion='PDAS').first()
    if not u:
        return jsonify({'message': 'User not found'}), 404

    sql_session.delete(u)
    sql_session.commit()
    sql_session.close()
    return jsonify({'message': 'User deleted successfully'})


