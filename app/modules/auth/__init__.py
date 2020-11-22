# -*- coding: utf-8 -*-
# @File: __init__.py.py
# @Author: byron
# @Date: 11/19/20

from flask import Blueprint
from flask_restful import Api
from .apis import LoginApi, RegisterApi, ImgVerifyApi

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
api = Api(auth_bp)

api.add_resource(LoginApi, "/login")
api.add_resource(RegisterApi, "/register")
api.add_resource(ImgVerifyApi, "/image_code")
