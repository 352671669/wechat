# -*- coding: utf-8 -*-
from config import RUN_VER
if RUN_VER == 'open':
    from blueapps.patch.settings_open_saas import *  # noqa
else:
    from blueapps.patch.settings_paas_services import  * # noqa

# 预发布环境
RUN_MODE = 'STAGING'

# 正式环境的日志级别可以在这里配置
# V2
# import logging
# logging.getLogger('root').setLevel('INFO')
# V3
# import logging
# logging.getLogger('app').setLevel('INFO')


# 预发布环境数据库可以在这里配置

DATABASES.update(
    {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': '120173501028_root',
            'USER': '孙宇成1',
            'PASSWORD': 'szy6368718',
            'HOST': '10.0.2.8',
            'PORT': '3306',
        },
    }
)

