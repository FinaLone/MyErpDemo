# -*- coding:utf-8 -*- 
import sys

reload(sys)
sys.setdefaultencoding('utf8')

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = 'you do not know the key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True


    FLASKY_MAIL_SUBJECT_PREFIX = '[MyErpDemo]'                      #邮件标题的前缀
    FLASKY_MAIL_SENDER = 'MyErpDemo Admin <lvwebmail@126.com>'      #显示在发件人栏
    FLASKY_ADMIN = 'lvwebmail@126.com'                              #管理员的默认email


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'lvwebmail'
    MAIL_PASSWORD = 'myerpdemo1'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
