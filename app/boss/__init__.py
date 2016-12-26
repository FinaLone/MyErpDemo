# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from flask import Blueprint

boss = Blueprint('boss', __name__)

from . import views