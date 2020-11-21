# -*- coding: utf-8 -*-
# @File: auth_helper.py
# @Author: byron
# @Date: 11/20/20

import time
import datetime
import time
import jwt
from config.config import Config
from app.models.models import UserInfo
from app.utils.response_utils import HttpCode, error, success


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
                    'id': user_id,
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
            if 'data' in payload and 'id' in payload['data']:
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return "Token expired"
        except jwt.InvalidTokenError:
            return "Invalid token"

    def generate_token(self, user_id):
        """
        login success, return token; login failed, return failure
        :param user_id:
        :return:
        """
        login_time = int(time.time())
        token = self._encode_auth_token(user_id, login_time)
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
                    user_id = payload.get('data').get('id')
                    login_time = payload.get('data').get('login_time')
                    user = UserInfo.query.get(user_id)

                    if not user:
                        return {'code': HttpCode.db_error, 'msg': "User does not exist"}
                    else:
                        if user.last_login == login_time:
                            return {'code': HttpCode.success, 'data': payload.get('data')}

        return {'code': HttpCode.auth_error, 'msg': "authentication failed"}
