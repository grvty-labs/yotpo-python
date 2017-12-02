from __future__ import unicode_literals
from future.builtins import str

import sys as _sys
import json
try:
    import requests
except ImportError:
    requests = None
from datetime import datetime, timedelta

from .exceptions import YotpoException

account_id = None
api_key = None
api_secret = None
domain = None
platform = 'general'
platform_object = None

access_token = None
access_token_date = None
# access_token = '0XAAdOrNE7PmOvql5QYmC1GoA5wicwrhzZHoGInj'
# access_token_date = datetime.now()

# Some API calls need to be sent to the normal endpoint and
# others need to be sent to v1
api_base = 'https://api.yotpo.com/apps'
api_base_bare = 'https://api.yotpo.com'
api_base_v1 = 'https://api.yotpo.com/v1/apps'

from yotpo.resources import (  # noqa
    Product, ProductGroup, Purchase, Review)

# import warnings as _warnings
# from inspect import isclass as _isclass, ismodule as _ismodule

_dogetattr = object.__getattribute__
_ALLOWED_ATTRIBUTES = (
    'account_id',
    'api_key',
    'api_secret',
)
_original_module = _sys.modules[__name__]


def authenticate():
    response = requests.post(
        # 'https://requestb.in/1o4mcv21',
        'https://api.yotpo.com/oauth/token',
        data={
          'client_id': api_key,
          'client_secret': api_secret,
          'grant_type': 'client_credentials'
        }
    )

    responseJSON = response.json()
    if response.status_code != 200:
        raise YotpoException(response)

    else:
        if 'error' in responseJSON:
            raise YotpoException(response)
        else:
            global access_token
            global access_token_date
            access_token = responseJSON['access_token']
            access_token_date = datetime.now()
            return access_token


def get_platform_name():
    global platform_object
    return platform_object['platform_type']['name']


def get_access_token():
    global access_token
    global access_token_date
    if not access_token or \
            access_token_date < datetime.now() - timedelta(days=5):
        access_token = authenticate()

    return access_token


def setPlatform(domain):
    global api_key
    global platform_object
    response = requests.post(
        'https://api.yotpo.com/apps/{}/account_platform'.format(
            api_key
        ),
        data={
          'utoken': get_access_token(),
          'account_platform': {
            'shop_domain': domain,
            'platform_type_id': '2',
          }
        }
    )

    responseJSON = response.json()
    if response.status_code != 200:
        raise YotpoException(response)

    else:
        platform_object = responseJSON['response']['account_platform']
        platform = get_platform_name()
