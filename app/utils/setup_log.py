# -*- coding: utf-8 -*-
# @File: setup_log.py
# @Author: byron
# @Date: 11/19/20

import logging
from logging.handlers import RotatingFileHandler
from config.config import configs


def setup_log(config_name):
    config = configs[config_name]
    logging.basicConfig(level=config.LOG_LEVEL)
    log_file_handler = RotatingFileHandler(config.LOG_DIR, maxBytes=1024*1024*100, backupCount=10)
    formatter = logging.Formatter('%(levelname)s %(filename)s: %(lineno)d %(message)s')
    log_file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(log_file_handler)

