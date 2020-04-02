from functools import wraps
from flask import request, make_response, jsonify
from flask_jwt_extended import get_jwt_identity
import logging
from flask_jwt import current_identity

logger = logging.getLogger('visit_log')
logger.setLevel(logging.INFO)


def logging(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        message = func(*args, **kwargs)
        ip = request.remote_addr
        path = request.path
        status = message.status_code
        logger.info(f"{path} {status} {user_id} {ip}")
        return message
    return wrapper


def simple_message(msg, status=200):
    return make_response(jsonify({"message": msg}), status)
