# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from flask import Blueprint

account_manager = Blueprint('account_manager', __name__)

from . import views