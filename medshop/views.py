# -*- coding: utf-8 -*-
from __future__ import unicode_literals

try:
    import ujson as json
except:
    import json
import hashlib
import logging
import types
from collections import OrderedDict

from furl import furl

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt

from . import constants

_logger = logging.getLogger(__name__)


def force_utf8_str(s):
    return s.encode('utf-8') if isinstance(s, types.UnicodeType) else s


def md5_digest(text):
    return hashlib.md5(force_utf8_str(text)).hexdigest()


def json_http_response(value, dumps=True, content_type=None, request=None):
    from django.http import HttpResponse
    if content_type is None:
        content_type = "application/json"
        if request is not None:
            http_accept = request.META.get("HTTP_ACCEPT", "*/*")
            # if "text/html" in http_accept and "application/json" not in http_accept:
            if "," in http_accept and "application/json" not in http_accept:
                content_type = "text/html"
                request._hit_htmlmin = False
    return HttpResponse(json.dumps(value) if dumps else value, content_type=content_type)


def index(request):
    urlobj = furl(constants.HAOYAOSHI_PAY_URL)
    urlobj.add({'orderSn': '201432222329'})
    urlobj.add({'token': constants.HAOYAOSHI_PAY_TOKEN})
    urlobj.add({'uuid': constants.HAOYAOSHI_PAY_UUID})
    urlobj.add({'orderSource': constants.HAOYAOSHI_PAY_ORDER_SOURCE})
    urlobj.add({'amount': '0.01'})
    urlobj.add({'notifyUrl': request.build_absolute_uri(reverse('medshop:proxy_pay_callback'))})
    urlobj.add({'returnUrl': request.build_absolute_uri(reverse('medshop:proxy_pay_result'))})
    urlobj.add({'orderDesc': '好药师支付中心测试'})
    urlobj.add({'productName': '好药师支付中心测试'})
    urlobj.add({'quantity': '1'})
    urlobj.add({'channelName': '支付宝'})
    urlobj.add({'channelKey': 'alipay'})
    urlobj.add({'payType': '1'})

    params = urlobj.query.params
    params = OrderedDict(sorted(params.iteritems(), key=lambda d:d[0]))
    qs = '&'.join(['%s=%s' % (k, v) for k, v in params.items()])
    sign = md5_digest(''.join([qs, constants.HAOYAOSHI_PAY_SIGN_KEY]))
    urlobj.add({'sign': sign})

    return redirect(urlobj.url)



@csrf_exempt
def proxy_pay_result(request, *args, **kwargs):
    params = request.POST.dict()
    _logger.info('params is %s' % json.dumps(params))

    KEY_sign = 'sign'
    proxy_sign = params.get(KEY_sign)
    params = OrderedDict(sorted(params.iteritems(), key=lambda d:d[0]))
    qs = '&'.join(['%s=%s' % (k, v) for k, v in params.items() if k != KEY_sign and v != ''])
    my_sign = md5_digest(''.join([qs, constants.HAOYAOSHI_PAY_SIGN_KEY]))
    if proxy_sign == my_sign:
        _logger.info('success')
        return json_http_response('success', dumps=False)
    else:
        _logger.info('fail')
        return json_http_response('fail', dumps=False)


@csrf_exempt
def proxy_pay_callback(request, *args, **kwargs):
    params = request.POST.dict()
    _logger.info('params is %s' % json.dumps(params))

    KEY_sign = 'sign'
    proxy_sign = params.get(KEY_sign)
    params = OrderedDict(sorted(params.iteritems(), key=lambda d:d[0]))
    qs = '&'.join(['%s=%s' % (k, v) for k, v in params.items() if k != KEY_sign and v != ''])
    my_sign = md5_digest(''.join([qs, constants.HAOYAOSHI_PAY_SIGN_KEY]))
    if proxy_sign == my_sign:
        _logger.info('success')
        return json_http_response('success', dumps=False)
    else:
        _logger.info('fail')
        return json_http_response('fail', dumps=False)
