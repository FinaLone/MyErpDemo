# -*- coding:utf-8 -*-
import sys

reload(sys)
sys.setdefaultencoding('utf8')

from functools import wraps
from flask import abort
from flask.ext.login import current_user
from .models import Permission
import json
from datetime import datetime, date

def permission_required(permission):                #使用Permission.*作为参数
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)

def am_required(f):
    return permission_required(Permission.ACCOUNTMANAGER)(f)

def fm_required(f):
    return permission_required(Permission.FINANCIALMANAGER)(f)

def boss_required(f):
    return permission_required(Permission.BOSS)(f)


class CJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)
