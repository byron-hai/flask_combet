# -*- coding: utf-8 -*-
# @File: __init__.py.py
# @Author: byron
# @Date: 11/19/20

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config.config import configs
from redis import StrictRedis
from app.utils.setup_log import setup_log


db = SQLAlchemy()
redis_store = None


def create_app(config_name):
    config = configs[config_name]
    setup_log(config_name)

    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    global redis_store
    redis_store = StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)

    return app
