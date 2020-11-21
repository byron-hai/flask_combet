# -*- coding: utf-8 -*-
# @File: image_storage.py
# @Author: byron
# @Date: 11/21/20

from qiniu import Auth, put_file, etag, urlsafe_base64_encode, put_data
import qiniu.config
from config.config import Config

access_key = Config.QINIU_ACCESS_KEY
secret_key = Config.QINIU_SECRET_KEY

q = Auth(access_key, secret_key)
bucket_name = Config.QiNIU_BUCKET


def image_storage(image_data):
    token = q.upload_token(bucket_name, None, 3600)
    # Upload image
    ret, info = put_data(token, None, image_data)

    # success if info.status_code = 200
    if info.status_code == 200:
        return ret.get("key")
    else:
        return ""




