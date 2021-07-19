#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations


import typing as t

from logging import getLogger
from inspect import getmembers
from eventlet.green import http
from service_green.core.green import json
from service_green.core.green import urllib3
from service_consul.exception import ConsulError

if t.TYPE_CHECKING:
    # 接口类型
    ConsulAPI = t.TypeVar('ConsulAPI', bound='BaseConsulAPI')
    # 客户端类型
    ConsulClient = t.TypeVar('ConsulClient', bound='BaseConsulClient')


logger = getLogger(__name__)

class ConsulAPIMixin(object):
    """ Consul接口扩展类 """

    @staticmethod
    def was_api(obj: t.Any) -> bool:
        """ 是接口实例吗?

        @param obj: 任意对象
        @return: bool
        """
        return isinstance(obj, BaseConsulAPI)


class BaseConsulAPI(ConsulAPIMixin):
    """ Consul接口基类 """

    def set_client(self, client) -> None:
        """ 创建接口实例

        @param data: 数据
        @return: ConsulAPI
        """
        self.client = client

    def __init__(self, client: t.Optional[ConsulClient] = None) -> None:
        """ 初始化实例

        @param client: 客户端
        """
        self.client = client

    def __new__(cls, *args: t.Any, **kwargs: t.Any) -> ConsulAPI:
        """ 创建接口实例

        @param args  : 位置参数
        @param kwargs: 接口参数
        """
        instance = super(BaseConsulAPI, cls).__new__(cls, *args, **kwargs)
        for name, api in getmembers(cls, predicate=cls.was_api):
            api.set_client(instance.client)
            setattr(instance, name, api)
        return instance

    def _get(self, url, **kwargs) -> t.Any:
        """ GET请求方法

        :param url: 请求地址
        :param kwargs: 命名参数
        :return: t.Any
        """
        kwargs['base_url'] = getattr(self, 'base_url', '') or ''
        return self.client.get(url, **kwargs)

    def _post(self, url, **kwargs) -> t.Any:
        """ POST请求方法

        :param url: 请求地址
        :param kwargs: 命名参数
        :return: t.Any
        """
        kwargs['base_url'] = getattr(self, 'base_url', '') or ''
        return self.client.post(url, **kwargs)

    def _put(self, url, **kwargs) -> t.Any:
        """ PUT请求方法

        :param url: 请求地址
        :param kwargs: 命名参数
        :return: t.Any
        """
        kwargs['base_url'] = getattr(self, 'base_url', '') or ''
        return self.client.put(url, **kwargs)

    def _patch(self, url, **kwargs) -> t.Any:
        """ PATCH请求方法

        :param url: 请求地址
        :param kwargs: 命名参数
        :return: t.Any
        """
        kwargs['base_url'] = getattr(self, 'base_url', '') or ''
        return self.client.patch(url, **kwargs)

    def _delete(self, url, **kwargs) -> t.Any:
        """ DELETE请求方法

        :param url: 请求地址
        :param kwargs: 命名参数
        :return: t.Any
        """
        kwargs['base_url'] = getattr(self, 'base_url', '') or ''
        return self.client.delete(url, **kwargs)


class BaseConsulClient(ConsulAPIMixin):
    """ Consul客户端基类 """

    def __init__(self,
                 host: t.Text = '127.0.0.1',
                 port: int = 8500,
                 scheme: t.Text = 'http',
                 verify: bool = False,
                 cert: t.Optional[t.Text] = None,
                 token: t.Optional[t.Text] = None,
                 pool_size: int = 1024):
        """ 初始化实例

        @param host: 目标地址
        @param port: 目标端口
        @param scheme: 使用协议
        @param verify: 是否验证
        @param cert: 指定证书
        @param token: 请求令牌
        @param pool_size: 请求池大小
        """
        self.host = host
        self.port = port
        self.schema = scheme
        self.cert = cert
        self.token = token
        self.verify = verify
        self.base_url = f'{scheme}://{host}:{port}'
        self.http = urllib3.PoolManager(num_pools=pool_size)

    def __new__(cls, *args: t.Any, **kwargs: t.Any) -> ConsulClient:
        """ 创建接口实例

        @param args  : 位置参数
        @param kwargs: 接口参数
        """
        instance = super(BaseConsulClient, cls).__new__(cls, *args, **kwargs)
        print(getmembers(cls))
        for name, api in getmembers(cls, predicate=cls.was_api):
            api.set_client(instance)
            setattr(instance, name, api)
        return instance

    def request(self, method: t.Text, url: t.Text, **kwargs: t.Text) -> t.Any:
        """ 请求处理方法

        :param method: 请求方法
        :param url: 请求地址
        :param kwargs: 请求参数
        :return: t.Any
        """
        kwargs.setdefault('timeout', None)
        kwargs.setdefault('headers', {})
        kwargs.setdefault('retries', None)
        self.token and kwargs['headers'].update({'X-Consul-Token': self.token})
        base_url = kwargs.pop('base_url', '') or self.base_url
        url = url if url.startswith(('http', 'https')) else '{}{}'.format(base_url, url)
        resp = self.http.request(method, url, **kwargs)
        data = resp.data.decode('utf-8')
        if resp.status != http.HTTPStatus.OK.value:
            raise ConsulError(data)
        print('!' * 100)
        print(data)
        print('!' * 100)
        return json.loads(data)

    def get(self, url: t.Text, **kwargs: t.Text) -> t.Any:
        """ GET请求方法

        :param url: 请求地址
        :param kwargs: 请求参数
        :return: t.Any
        """
        method = 'GET'
        return self.request(method, url, **kwargs)

    def post(self, url: t.Text, **kwargs: t.Text) -> t.Any:
        """ POST请求方法

        :param url: 请求地址
        :param kwargs: 请求参数
        :return: t.Any
        """
        method = 'POST'
        return self.request(method, url, **kwargs)

    def put(self, url: t.Text, **kwargs: t.Text) -> t.Any:
        """ PUT请求方法

        :param url: 请求地址
        :param kwargs: 请求参数
        :return: ...
        """
        method = 'PUT'
        return self.request(method, url, **kwargs)

    def patch(self, url: t.Text, **kwargs: t.Text) -> t.Any:
        """ PATCH请求方法

        :param url: 请求地址
        :param kwargs: 请求参数
        :return: t.Any
        """
        method = 'PATCH'
        return self.request(method, url, **kwargs)

    def delete(self, url: t.Text, **kwargs: t.Text) -> t.Any:
        """ DELETE请求方法

        :param url: 请求地址
        :param kwargs: 请求参数
        :return: t.Any
        """
        method = 'DELETE'
        return self.request(method, url, **kwargs)
