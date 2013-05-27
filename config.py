# -*- coding: utf-8 -*-
class Config(object):
    DEBUG = False
    MONGODB_SETTINGS = {'DB': 'dev_blog2'}
    SECRET_KEY = 'lask+mongoengine=<3'
    MAIN_TITLE = u'Sea_Kudo的博客'


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
