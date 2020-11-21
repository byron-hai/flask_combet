# -*- coding: utf-8 -*-
# @File: __init__.py.py
# @Author: byron
# @Date: 11/19/20

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
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

    # init redis_store
    global redis_store
    redis_store = StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT, decode_responses=True)

    # init flask session
    Session(app)

    # Register blueprint: auth_bp
    from app.modules.auth import auth_bp
    app.register_blueprint(auth_bp)

    # Register blueprint: profile_bp
    from app.modules.profile import profile_bp
    app.register_blueprint(profile_bp)

    return app

