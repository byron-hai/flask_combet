# -*- coding: utf-8 -*-
# @File: views.py
# @Author: byron
# @Date: 11/21/20

from flask import g, request, current_app
from app.utils.response_utils import HttpCode, success, error
from app.modules.profile import profile_bp
from app.utils.common import login_identify
from app.models.models import LoginUser
from app.utils.constants import QINIU_DOMIN_PREFIX
from app.libs import image_storage


@profile_bp.route('/user')
@login_identify
def user():
    if not g.user:
        return error(HttpCode.auth_error, "User not logged in")

    user = g.user
    return success("success", data=user.to_dict())


@profile_bp.route('/nickname', methods=['POST'])
@login_identify
def nickname():
    if not g.user:
        return error(HttpCode.auth_error, "User not logged in")

    user = g.user
    nickname = request.json.get('nickname')
    user.nickname = nickname
    err = user.update()
    if err:
        return error(HttpCode.db_error, "update user info failed")
    return success("success", data={'nickname': nickname})


@profile_bp.route('/mobile', methods=['POST'])
@login_identify
def mobile():
    pass


@profile_bp.route('/birth_date', methods=['POST'])
@login_identify
def birth_date():
    if not g.user:
        return error(HttpCode.auth_error, "User not logged in")

    user = g.user
    birth_date = request.json.get('birthday')
    user.birth_date = birth_date
    err = user.update()
    if err:
        return error(HttpCode.db_error, "update user info failed")
    return success("success", data={'birth_date': birth_date})


@profile_bp.route('/password', methods=['POST'])
@login_identify
def set_password():
    if not g.user:
        return error(HttpCode.auth_error, "User not logged in")

    user = g.user
    login_user = LoginUser.query.filter_by(user_id=user.id).first()
    if not login_user:
        return error(HttpCode.db_error, "Get user info failed")

    login_user.password = request.json.get('password')
    err = login_user.update()
    if err:
        return error(HttpCode.db_error, "update user info failed")
    return success("success")


@profile_bp.route('/avatar', methods=['POST'])
@login_identify
def upload_avatar():
    avatar_file = request.files.get('avatar')
    try:
        img_data = avatar_file.read()
        image_name = image_storage.image_storage(img_data)
    except Exception as e:
        current_app.logger.error(e)
        return error(HttpCode.db_error, "image upload failed")

    avatar_url = QINIU_DOMIN_PREFIX + image_name
    g.user.avatar_url = avatar_url
    err = g.user.update()
    if err:
        return error(HttpCode.db_error, "Update user avatar_url failed")

    return success('upload success', data={'avatar_url': avatar_url})


@profile_bp.route('/signature', methods=['POST'])
@login_identify
def signature():
    if not g.user:
        return error(HttpCode.auth_error, "User not logged in")

    user = g.user
    signature = request.json.get('signature')
    user.signature = signature
    err = user.update()
    if err:
        return error(HttpCode.db_error, "update user info failed")
    return success("success", data={'signature': signature})


@profile_bp.route('/sex', methods=['POST'])
@login_identify
def sex():
    if not g.user:
        return error(HttpCode.auth_error, "User not logged in")

    user = g.user
    sex = request.json.get('sex')
    user.sex = sex
    err = user.update()
    if err:
        return error(HttpCode.db_error, "update user info failed")
    return success("success", data={'sex': sex})
