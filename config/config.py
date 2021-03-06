# -*- coding: utf-8 -*-
# @File: config.py
# @Author: byron
# @Date: 11/19/20
import logging
from redis import StrictRedis


class Config:
    DEBUG = False
    SECRET_KEY = "\xc6\xb4\xa2f\xd0\xcb#\xe1\xf0j(\t\xef\xc2\xb7/\x85\xd9\xcdaK\xc6yG\xed\x05\x0b\xc7&\x0bO\x17"
    # Mysql database configure
    DIALECT = "mysql"
    DRIVER = "pymysql"
    USERNAME = "root"
    PASSWORD = "root1234"
    HOSTNAME = "127.0.0.1"
    PORT = "3306"
    DATABASE = "flask_combet"
    URI = "{}+{}://{}:{}@{}:{}/{}".format(DIALECT, DRIVER, USERNAME, PASSWORD,
                                          HOSTNAME, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = URI
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Redis database configure
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = "6379"

    # config session
    SESSION_TYPE = "redis"
    SESSION_USE_SINGER = True  # make cookie_id encrypted and signed
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # Instance a redis session

    # logging config
    LOG_LEVEL = logging.INFO
    LOG_DIR = "logs/log"

    # Login authentication
    AUTH_TYPE = "token"  # Options: session, token

    # image storage keys
    QINIU_ACCESS_KEY = '7DtupNyj7TaqXzVU0TIxlLVkV6***uQeWoqkCfPV'
    QINIU_SECRET_KEY = 'Cew1X0fTSRQaIkBUHqSRxxvqVI598DgkeJ6*****'
    QINIU_BUCKET = 'byron-bucket'


class DevelopConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG


class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = logging.ERROR


class UnittestConfig(Config):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG


configs = {
    "development": DevelopConfig,
    "production": ProductionConfig,
    "test": UnittestConfig
}
