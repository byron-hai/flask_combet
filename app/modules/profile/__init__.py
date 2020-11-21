# -*- coding: utf-8 -*-
# @File: __init__.py.py
# @Author: byron
# @Date: 11/19/20

from flask import Blueprint
from .views import views

profile_bp = Blueprint("profile", __name__, url_prefix="/profile")


