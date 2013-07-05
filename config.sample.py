# -*- coding: utf-8 -*-
class Config(object):
    DEBUG = False
    MONGODB_SETTINGS = {'DB': 'dev_blog2'}
    SECRET_KEY = 'lask+mongoengine=<3'
    MAIN_TITLE = u'Sea_Kudo的博客'
    SITE_URL = 'http://tuzii.me'
    KEYWORDS = 'u前端开发, 互联网, 技术博客, 个人博客, 生活记录'
    DESCRIPTION  = u'并不是所有唯美的故事 都伴有精彩的风景. 我只愿尽我所能 带你看遍整个春夏秋冬.'
    EMAIL = 'he.kang@dev-engine.com'

class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_TB_PANELS = (
            'flask.ext.debugtoolbar.panels.versions.VersionDebugPanel',
            'flask.ext.debugtoolbar.panels.timer.TimerDebugPanel',
            'flask.ext.debugtoolbar.panels.headers.HeaderDebugPanel',
            'flask.ext.debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
            'flask.ext.debugtoolbar.panels.template.TemplateDebugPanel',
            'flask.ext.debugtoolbar.panels.logger.LoggingPanel',
            'flask.ext.mongoengine.panels.MongoDebugPanel'
            )
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SITE_URL = 'http://vm.tuzii.me'

class SmtpConfig(Config):
    SERVER = 'smtp.gmail.com'
    PORT = 587
    USER = 'no-reply@dev-engine.com'
    PASSWORD = ''

class UpyunConfig(Config):
    URL = ''
    BUCKET = ''
    ADMIN = ''
    PASSWORD = ''
