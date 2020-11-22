# -*- coding: utf-8 -*-
# @File: img_captcha.py
# @Author: byron
# @Date: 11/19/20

import random
import string
from io import BytesIO
from captcha.image import ImageCaptcha
from flask import current_app
from app import redis_store


def generate_random_text(length=4):
    source = list(string.ascii_letters) + [str(i) for i in range(10)]
    return "".join(random.sample(source, length))


def generate_captcha(text_length=4, img_type="JPEG"):
    format_map = {"JPEG": ".jpg", "PNG": ".png"}

    if img_type not in format_map.keys():
        raise ValueError("img_type only support JPEG, PNG")

    # generate random text
    text = generate_random_text(text_length)
    img = ImageCaptcha()
    image = img.generate_image(text)

    image_name = text + format_map.get(img_type)

    buf = BytesIO()
    image.save(buf, format=img_type)
    image_data = buf.getvalue()
    return text, image_name, image_data


def captcha_verify(img_code_id, img_code):
    redis_img_code = None
    try:
        redis_img_code = redis_store.get("img_code:%s" % img_code_id)
    except Exception as e:
        current_app.logger.error(e)

    if not redis_img_code:
        return 1, "Image code expired"

    if redis_img_code.lower() != img_code.lower():
        return 2, "image code not matched"

    return 0, "success"
