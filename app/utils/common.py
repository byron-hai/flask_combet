# -*- coding: utf-8 -*-
# @File: common.py
# @Author: byron
# @Date: 11/21/20

from functools import wraps
from flask import session, g, current_app, request
from app.utils.auth_helper import Auth
from app.utils.response_utils import error, HttpCode
from app.models.models import UserInfo
from config.config import Config


# login check by Session
def login_identify(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if Config.AUTH_TYPE == "session":
            user_id = session.get("user_id")
        # For else, use token authentication
        else:
            rtn = Auth().identify_token(request)
            if rtn['code'] != 200:
                return error(HttpCode.auth_error, "Authentication failed")
            user_id = rtn['data'].get('user_id')

        if user_id:
            try:
                user = UserInfo.query.get(user_id)
            except Exception as e:
                current_app.logger.error(e)
                return error(HttpCode.db_error, "Get user info failed")

            g.user = user
            return func(*args, **kwargs)
        return error(HttpCode.auth_error, "Authentication failed")
    return wrapper
