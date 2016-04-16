# -*- coding: utf-8 -*-
from flask import Blueprint

sensor = Blueprint('sensor', __name__)

from . import views