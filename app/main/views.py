# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from flask import render_template
from . import main


@main.route('/')
def index():
    return render_template('index.html')
