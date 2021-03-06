# -*- coding: UTF-8 -*-
"""
微信账号体系相关的Account
"""
import time
import random
import urlparse
import urllib

from django.http import HttpResponseRedirect, HttpResponse

from common.log import logger
import settings as weixin_settings
from .api import WeiXinApi, QyWeiXinApi
from .models import BkWeixinUser


class WeixinAccountSingleton(object):
    """
    单例基类
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        '''
        @param class_:
        '''
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance


class WeixinAccount(WeixinAccountSingleton):
    """
    微信账号体系相关的基类Account
    提供通用的账号功能
    """
    # 跳转到微信重定向链接
    WEIXIN_OAUTH_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize'

    def __init__(self):
        if weixin_settings.IS_QY_WEIXIN:
            self.weixin_api = QyWeiXinApi()
        else:
            self.weixin_api = WeiXinApi()

    def is_weixin_visit(self, request):
        """
        是否来自微信访问
        """
        if weixin_settings.USE_WEIXIN and request.path.startswith(weixin_settings.WEIXIN_SITE_URL) and \
                request.get_host() == weixin_settings.WEIXIN_APP_EXTERNAL_HOST:
            return True
        return False

    def set_weixin_oauth_state(self, request, length=32):
        """
        生成随机的state，并存储到session中
        """
        allowed_chars = 'abcdefghijkmnpqrstuvwxyzABCDEFGHIJKLMNPQRSTUVWXYZ0123456789'
        state = ''.join(random.choice(allowed_chars) for _ in range(length))
        request.session['WEIXIN_OAUTH_STATE'] = state
        request.session['WEIXIN_OAUTH_STATE_TIMESTAMP'] = time.time()
        return state

    def get_oauth_redirect_url(self, callback_url, state='authenticated'):
        """
        获取oauth访问链接
        """
        params = {
            'appid': weixin_settings.WEIXIN_APP_ID,
            'redirect_uri': callback_url,
            'response_type': 'code',
            'scope': weixin_settings.WEIXIN_SCOPE,
            'state': state
        }
        params = urllib.urlencode(params)
        redirect_uri = '%s?%s#wechat_redirect' % (self.WEIXIN_OAUTH_URL, params)
        return redirect_uri

    def redirect_weixin_login(self, request):
        """
        跳转到微信登录
        """
        url = urlparse.urlparse(request.build_absolute_uri())
        path = weixin_settings.WEIXIN_LOGIN_URL
        query = urllib.urlencode({'curl': request.get_full_path()})
        callback_url = urlparse.urlunsplit((url.scheme, url.netloc, path, query, url.fragment))
        state = self.set_weixin_oauth_state(request)
        redirect_uri = self.get_oauth_redirect_url(callback_url, state)
        return HttpResponseRedirect(redirect_uri)

    def verify_weixin_oauth_state(self, request, expires_in=60):
        """
        验证state是否正确，防止csrf攻击
        """
        try:
            state = request.GET.get('state')
            raw_state = request.session.get('WEIXIN_OAUTH_STATE')
            raw_timestamp = request.session.get('WEIXIN_OAUTH_STATE_TIMESTAMP')
            # 验证state
            if not raw_state or raw_state != state:
                return False
            # 验证时间戳
            if not raw_timestamp or time.time() - raw_timestamp > expires_in:
                return False
            # 验证成功后清空session
            request.session['WEIXIN_OAUTH_STATE'] = None
            request.session['WEIXIN_OAUTH_STATE_TIMESTAMP'] = None
            return True
        except Exception, e:
            logger.exception(u"验证请求weixin code的 state参数出错： %s" % e)
            return False

    def verfiy_weixin_oauth_code(self, request):
        """
        验证Code有效性
        """
        code = request.GET.get('code')
        is_ok, data = self.weixin_api.check_login_code(code)
        return is_ok, data

    def get_user_info(self, base_data):
        """
        根据access_token, userid获取用户信息
        """
        userid = base_data.get('userid')
        access_token = base_data.get('access_token')
        userinfo = self.weixin_api.get_user_info_for_account(access_token, userid)
        return userinfo

    def get_callback_url(self, request):
        """
        获取实际访问的URL
        """
        callback_url = request.GET.get('c_url') or weixin_settings.WEIXIN_SITE_URL
        return callback_url

    def login(self, request):
        """
        微信登录后回调
        """
        if not self.is_weixin_visit(request):
            # TODO 改造为友好页面
            return HttpResponse(u"非微信访问，或应用未启动微信访问")
        # 验证回调state
        if not self.verify_weixin_oauth_state(request):
            # TODO 改造为友好页面
            return HttpResponse(u"State验证失败")
        # 验证code有效性
        is_code_vaild, base_data = self.verfiy_weixin_oauth_code(request)
        if not is_code_vaild:
            # TODO 改造为友好页面
            return HttpResponse(u"登录失败")

        # 获取用户信息并设置用户
        userinfo = self.get_user_info(base_data)
        userid = userinfo.pop('userid')
        user = BkWeixinUser.objects.get_update_or_create_user(userid, **userinfo)
        # 设置session
        request.session['weixin_user_id'] = user.id
        setattr(request, 'weixin_user', user)

        # 跳转到用户实际访问URL
        callback_url = self.get_callback_url(request)
        return HttpResponseRedirect(callback_url)
