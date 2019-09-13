from functools import wraps
from flask import request, make_response, jsonify
from flask_login import current_user
import logging

logger = logging.getLogger('visit_log')
logger.setLevel(logging.INFO)


def logging(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = current_user.id
        message = func(*args, **kwargs)
        ip = request.remote_addr
        path = request.path
        status = message.status_code
        logger.info(f"{path} {status} {user_id} {ip}")
        return message
    return wrapper


def simple_message(msg, status=200):
    return make_response(jsonify({"message": msg}), status)