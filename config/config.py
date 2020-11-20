# -*- coding: utf-8 -*-
# @File: config.py
# @Author: byron
# @Date: 11/19/20
import logging


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

    # logging config
    LOG_LEVEL = logging.INFO
    LOG_DIR = "logs/log"


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
