# -*- coding: utf-8 -*-
# @File: apis.py
# @Author: byron
# @Date: 11/19/20

from flask import request, current_app, make_response, session
from flask_restful import Resource, reqparse, inputs
from app.models.models import LoginUser, UserInfo
from app.utils.response_utils import HttpCode, success, error
from app.utils.img_captcha import generate_captcha, captcha_verify
from app.utils import constants
from app.utils.auth_helper import Auth
from app import redis_store
from datetime import datetime
from config.config import Config


def parse_args():
    # bundle_errors: pring multi-errors
    parser = reqparse.RequestParser(bundle_errors=True)
    parser.add_argument("mobile", type=inputs.regex(r"1[356789]\d{9}$"), required=True,
                        location=['json'], help="Mobile not correct")

    parser.add_argument("password", type=str, required=True,
                        location=['json'], help="Password not correct")

    parser.add_argument("img_code", type=str, required=True,
                        location=['json'], help="Image code not correct")

    parser.add_argument("img_code_id", type=str, required=True,
                        location=['json'], help="image code id not provided")

    args = parser.parse_args()
    return args


class LoginApi(Resource):
    def post(self):
        """
        1) Verify params
        2) password verification

        :return:
        """

        args = parse_args()
        mobile = args.get('mobile')
        password = args.get('password')
        img_code = args.get('img_code')
        img_code_id = args.get('img_code_id')

        if not all([mobile, password, img_code, img_code_id]):
            return error(code=HttpCode.params_error, msg="params not all filled")

        rtn_code, msg = captcha_verify(img_code_id, img_code)
        if rtn_code != 0:
            return error(HttpCode.params_error, msg=msg)

        user_login = LoginUser.query.filter_by(mobile=mobile).first()
        if not user_login:
            return error(HttpCode.db_error, msg="User not found")

        if not user_login.check_password(password):
            return error(HttpCode.params_error, msg="Password error")

        user_login.last_login = datetime.now()
        err = user_login.update()
        if err:
            current_app.logger.error(err)
            return error(HttpCode.db_error, "Store login user info failed")

        user_login = LoginUser.query.filter_by(mobile=mobile).first()
        if Config.AUTH_TYPE == 'session':
            session['user_id'] = user_login.user_id
            session['mobile'] = user_login.mobile
            return success("Login success")
        else:
            token_data = Auth().generate_token(user_login.user_id, user_login.last_login)
            return success("login success", data={'token':token_data})


class RegisterApi(Resource):
    @staticmethod
    def post():
        args = parse_args()
        mobile = args.get('mobile')
        password = args.get('password')
        img_code = args.get('img_code')
        img_code_id = args.get('img_code_id')

        if not all([mobile, password, img_code, img_code_id]):
            return error(code=HttpCode.params_error, msg="params not all filled")

        rtn_code, msg = captcha_verify(img_code_id, img_code)
        if rtn_code != 0:
            return error(HttpCode.params_error, msg=msg)

        user = UserInfo(mobile=mobile, nickname=mobile)
        err = user.add(user)
        if err:
            current_app.logger.error(err)
            return error(HttpCode.db_error, msg="Store user info failed")

        login_user = LoginUser()
        login_user.mobile = mobile
        login_user.password = password
        login_user.user_id = user.id

        err = login_user.add(login_user)
        if err:
            current_app.logger(err)
            return error(HttpCode.db_error, msg="Store login-user failed")

        return success("Register success")


class ImgVerifyApi(Resource):
    def post(self):
        """
        1) get request params
        2) Gen verification image
        3) img_id: picture_value store to redis
        4) return image to front
        :return:
        """
        #cur_id = request.args.get('cur_id')
        #pre_id = request.args.get('pre_id')
        cur_id = request.json.get('cur_id')
        pre_id = request.json.get('pre_id')

        text, img_name, img_data = generate_captcha()
        print(f"***** {text} *****")

        try:
            redis_store.set("img_code:%s" % cur_id, text, constants.IMAGE_CODE_EXPIRE_TIME)
            if pre_id:
                redis_store.delete("img_code:%s" % pre_id)
        except Exception as e:
            current_app.logger.error(e)
            return error(HttpCode.db_error, msg="Get image code from redis failed")

        response = make_response(img_data)
        response.headers["Content-Type"] = "image/jpg"

        return response
