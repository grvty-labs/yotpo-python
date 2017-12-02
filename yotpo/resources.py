# - Requests is the preferred HTTP library
# - Google App Engine has urlfetch
# - Use Pycurl if it's there (at least it verifies SSL certs)
# - Fall back to urllib2 with a warning if needed
try:
    import urllib2
    # import contextlib
except ImportError:
    import urllib.request
    import urllib.error

try:
    import requests
except ImportError:
    requests = None

from datetime import timedelta, datetime
from .exceptions import YotpoException
import json
import yotpo


class Product:
    def __init__(self, id=None, name=None, url=None, image=None,
                 description=None, price=None, tags=None, specs=dict()):
        super(Product, self).__init__()
        self.id = id
        self.name = name
        self.url = url
        self.image = image
        self.description = description
        self.price = price
        self.tags = tags
        self.specs = specs

    def retrieveBottomLine(self):
        if not self.id:
            raise Exception('Data does not have the required keys')

        response = requests.get(
            '{}/products/{}/{}/bottomline?callback="none"'.format(
                yotpo.api_base_bare,
                yotpo.api_key,
                self.id))
        if response.status_code != 200:
            raise YotpoException(response)

        content = response.content.decode('utf-8')[7:-2]
        return json.loads(content)['response']['bottomline']

    @classmethod
    def retrieveAll(self):
        response = requests.get(
            '{}/{}/products?utoken={}'.format(
                yotpo.api_base_v1,
                yotpo.api_key,
                yotpo.get_access_token()))
        if response.status_code != 200:
            raise YotpoException(response)
        return response.json()['products']

    def to_json(self):
        return {
            'name': self.name,
            'url': self.url,
            'image': self.image,
            'description': self.description,
            'price': self.price,
            'product_tags': self.tags,
            'specs': self.specs,
        }


class ProductGroup:
    def __init__(self, name):
        super(ProductGroup, self).__init__()
        self.name = name

    def create(self):
        if not self.name:
            raise Exception('Name is required')
        response = requests.post(
            '{}/{}/products_groups'.format(
                yotpo.api_base_v1,
                yotpo.api_key),
            data={
                'utoken': yotpo.get_access_token(),
                'group_name': self.name,
            })
        if response.status_code != 200:
            raise YotpoException(response)
        return True

    @classmethod
    def retrieveAll(self):
        response = requests.get(
            '{}/{}/products_groups?utoken={}'.format(
                yotpo.api_base_v1,
                yotpo.api_key,
                yotpo.get_access_token()))
        if response.status_code != 200:
            raise YotpoException(response)
        print(response.json())
        return response.json()['response']['products_groups']


class Purchase:
    def __init__(self, id=None, user_email=None, user_name=None,
                 currency_iso=None, order_id=None, products=None):
        super(Purchase, self).__init__()
        self.id = id
        self.user_email = user_email
        self.user_name = user_name
        self.currency_iso = currency_iso
        self.order_id = order_id
        self.products = products

    @classmethod
    def retrieveAll(self, count=10, since_id=0):
        response = requests.get(
            '{}/{}/purchases?utoken={}&count={}&since_id={}'.format(
                yotpo.api_base,
                yotpo.api_key,
                yotpo.get_access_token(),
                count,
                since_id))
        if response.status_code != 200:
            raise YotpoException(response)
        return response.json()['response']['purchases']

    def create(self):
        if not self.user_email or not self.user_name or not self.currency_iso \
                or not self.order_id or not self.products:
            raise Exception('Data does not have the required keys')
        response = requests.post(
            '{}/{}/purchases'.format(
                yotpo.api_base,
                yotpo.api_key),
            data={
                'validate_data': True,
                'platform': yotpo.platform,
                'utoken': yotpo.get_access_token(),
                'email': self.user_email,
                'customer_name': self.user_name,
                'order_id': self.order_id,
                'currency_iso': self.currency_iso,
                'products': self.build_products_json(),
            })
        if response.status_code != 200:
            raise YotpoException(response)
        return True

    def build_products_json(self):
        products = dict()
        for product in self.products:
            products[product.id] = product.to_json()
        return products


class Review:

    @classmethod
    def retrieveBottomLineAllProducts(self, count=100, page=1, since_id='0'):
        response = requests.get(
            '{}/{}/bottom_lines?utoken={}&page={}&count={}&since_id={}'.format(
                yotpo.api_base,
                yotpo.api_key,
                yotpo.get_access_token(),
                page,
                count,
                since_id))
        if response.status_code != 200:
            raise YotpoException(response)
        return response.json()['response']['bottomlines']

    @classmethod
    def retrieveAll(self):
        response = requests.get(
            '{}/{}/reviews?utoken={}'.format(
                yotpo.api_base_v1,
                yotpo.api_key,
                yotpo.get_access_token()))
        if response.status_code != 200:
            raise YotpoException(response)
        return response.json()['reviews']
