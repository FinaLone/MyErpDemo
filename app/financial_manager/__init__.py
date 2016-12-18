# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from flask import Blueprint

financial_manager = Blueprint('financial_manager', __name__)

from . import views