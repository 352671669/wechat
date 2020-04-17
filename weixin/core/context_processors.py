# -*- coding: utf-8 -*-
"""
context_processor for weixin(setting)
"""
from django.conf import settings


def basic(request):
    # 微信相关配置
    weixin_site_url = getattr(settings, "WEIXIN_SITE_URL", None)
    weixin_static_url = getattr(settings, "WEIXIN_STATIC_URL", None)
    return {
        'WEIXIN_SITE_URL': weixin_site_url,
        'WEIXIN_STATIC_URL': weixin_static_url
    }
