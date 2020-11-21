# -*- coding: utf-8 -*-
# @File: common.py
# @Author: byron
# @Date: 11/21/20

from functools import wraps
from flask import session, g, current_app, request
from app.utils.auth_helper import Auth
from app.utils.response_utils import error, HttpCode
from app.models.models import UserInfo


# login check by Session
def login_session_verify(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        user = None

        if user_id:
            try:
                user = UserInfo.query.get(user_id)
            except Exception as e:
                current_app.logger.error(e)
        g.user = user
        return func(*args, **kwargs)
    return wrapper


# login check by token
def login_auth_identify(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        rtn = Auth().identify_token(request)
        if rtn['code'] == 200:
            user_id = rtn.get('user_id')
            g.user = UserInfo.query.get(user_id)

            return func(*args, **kwargs)
        else:
            return error(HttpCode.auth_error, "Authentication failed")
    return wrapper
