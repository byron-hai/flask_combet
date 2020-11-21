# -*- coding: utf-8 -*-
# @File: response_utils.py
# @Author: byron
# @Date: 11/19/20

from flask import jsonify


class HttpCode(object):
    success = 200
    params_error = 400
    server_error = 500
    auth_error = 401
    db_error = 1001


def resp_result(code, msg, data):
    return jsonify(code=code, msg=msg, data=data or {})


def success(msg, data=None):
    return resp_result(code=HttpCode.success, msg=msg, data=data)


def error(code, msg, data=None):
    return resp_result(code=code, msg=msg, data=data)
