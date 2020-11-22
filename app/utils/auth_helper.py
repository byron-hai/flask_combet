# -*- coding: utf-8 -*-
# @File: auth_helper.py
# @Author: byron
# @Date: 11/20/20

import datetime
import time
import jwt
from config.config import Config
from app.models.models import LoginUser
from app.utils.response_utils import HttpCode


class Auth:
    @staticmethod
    def _encode_auth_token(user_id, login_time):
        """
        Encode authentication token
        :param user_id: int
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
                'iat': datetime.datetime.utcnow(),
                'data': {
                    'user_id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(payload,
                              Config.SECRET_KEY,
                              algorithm='HS256'
                              )
        except Exception as e:
            return e

    @staticmethod
    def _decode_auth_token(auth_token):
        """
        Decode authentication token
        :param auth_token:
        :return:
        """
        try:
            payload = jwt.decode(auth_token, Config.SECRET_KEY,
                                 leeway=datetime.timedelta(days=1))
            if 'data' in payload and 'user_id' in payload['data']:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return "Token expired"
        except jwt.InvalidTokenError:
            return "Invalid token"

    def generate_token(self, user_id, login_time):
        """
        login success, return token; login failed, return failure
        :param user_id: int
        :param login_time: datetime
        :return:
        """
        login_time_stamp = int(time.mktime(login_time.timetuple()))
        token = self._encode_auth_token(user_id, login_time_stamp)
        return str(token, encoding='utf-8')

    def identify_token(self, request):
        """
        Identify Auth token
        Checking login_time is for verify single login
        :param request: headers:{"Authorization": "JWT token"}
        :return:
        """
        auth_header = request.headers.get("Authorization")
        if auth_header:
            auth_token_arr = auth_header.split(" ")
            if auth_token_arr and auth_token_arr[0] == 'JWT' and len(auth_token_arr) == 2:
                auth_token = auth_token_arr[1]
                payload = self._decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    user_id = payload.get('data').get('user_id')
                    login_time = payload.get('data').get('login_time')
                    login_user = LoginUser.query.filter_by(user_id=user_id).first()

                    if not login_user:
                        return {'code': HttpCode.db_error, 'msg': "User does not exist"}
                    else:
                        db_login_time = time.mktime(login_user.last_login.timetuple())
                        if db_login_time == login_time:
                            return {'code': HttpCode.success, 'data': payload.get('data')}
                return {'code': HttpCode.auth_error, 'msg': "Auth token decode error"}
            return {'code': HttpCode.auth_error, 'msg': "Auto token expects starts with JWT"}
        return {'code': HttpCode.auth_error, 'msg': "request headers has no 'Authorization' data"}
