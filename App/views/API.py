from flask import Blueprint, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user as jwt_current_user

api_views = Blueprint('api_views',__name__, url_prefix='/api')

@api_views.route('/ping',methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200