#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import logging
import typing as t

from http import HTTPStatus
from logging import getLogger
from inspect import getmembers
from urllib.parse import urlencode
from service_green.core.green import urllib3
from service_consul.exception import ConsulError

logger = getLogger(__name__)

__all__ = ['BaseConsulClient', 'BaseConsulAPI']


def is_consul_api(obj: t.Any) -> bool:
    """ 是否为Consul api?

    @param obj: 任意对象
    @return: bool
    """
    return isinstance(obj, BaseConsulAPI)


class BaseConsulClient(object):
    """ Consul客户端基类 """

    def __init__(
            self,
            host: t.Optional[t.Text] = None,
            port: t.Optional[int] = None,
            debug: t.Optional[bool] = None,
            scheme: t.Optional[t.Text] = None,
            acl_token: t.Optional[t.Text] = None,
            pool_size: t.Optional[int] = None,
            data_center: t.Optional[t.Text] = None
    ) -> None:
        """ 初始化实例 """
        self.port = port or 8500
        self.acl_token = acl_token
        self.host = host or '127.0.0.1'
        self.schema = scheme or 'http'
        req_logger = getLogger('urllib3')
        debug and req_logger.setLevel(
            level=logging.DEBUG
        )
        pool_size = pool_size or 10240
        self.http = urllib3.PoolManager(
            num_pools=pool_size
        )
        self.registered_services = {}
        self.data_center = data_center or ''

    def __new__(cls, *args: t.Any, **kwargs: t.Any) -> BaseConsulClient:
        """ 创建接口实例

        @param args  : 位置参数
        @param kwargs: 命名参数
        """
        instance = super(BaseConsulClient, cls).__new__(cls)
        curr_consul_client_instance = instance
        # 获取当前类中为BaseConsulAPI实例的类属性
        all_apis = getmembers(cls, predicate=is_consul_api)
        for name, api in all_apis:
            # 向子API实例传递客户端CLIENT实例
            api.client = instance
            setattr(instance, name, api)
        return curr_consul_client_instance

    def get(self, url: t.Text, **kwargs: t.Text) -> t.Any:
        """ 请求方法 - GET

        @param url: 请求地址
        @param kwargs: 请求参数
        @return: t.Any
        """
        method = 'GET'
        return self.request(method, url, **kwargs)

    def post(self, url: t.Text, **kwargs: t.Text) -> t.Any:
        """ 请求方法 - POST

        @param url: 请求地址
        @param kwargs: 请求参数
        @return: t.Any
        """
        method = 'POST'
        return self.request(method, url, **kwargs)

    def put(self, url: t.Text, **kwargs: t.Text) -> t.Any:
        """ 请求方法 - PUT

        @param url: 请求地址
        @param kwargs: 请求参数
        @return: t.Any
        """
        method = 'PUT'
        return self.request(method, url, **kwargs)

    def patch(self, url: t.Text, **kwargs: t.Text) -> t.Any:
        """ 请求方法 - PATCH

        @param url: 请求地址
        @param kwargs: 请求参数
        @return: t.Any
        """
        method = 'PATCH'
        return self.request(method, url, **kwargs)

    def delete(self, url: t.Text, **kwargs: t.Text) -> t.Any:
        """ 请求方法 - DELETE

        @param url: 请求地址
        @param kwargs: 请求参数
        @return: t.Any
        """
        method = 'DELETE'
        return self.request(method, url, **kwargs)

    def request(self, method: t.Text, url: t.Text, **kwargs: t.Text) -> t.Any:
        """ 请求处理方法

        :param method: 请求方法
        :param url: 请求地址
        :param kwargs: 请求参数
        :return: t.Any
        """
        # https://urllib3.readthedocs.io/en/stable/user-guide.html#query-parameters
        if method.upper() not in ('GET', 'HEAD', 'DELETE'):
            url = f'{url}?{urlencode(kwargs.pop("fields", {}))}'
        if 'timeout' not in kwargs:
            kwargs['timeout'] = None
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        if 'retries' not in kwargs:
            kwargs['retries'] = None
        if self.acl_token:
            kwargs['headers']['X-Consul-Token'] = self.acl_token
        if 'base_url' in kwargs and kwargs['base_url']:
            base_url = kwargs.pop('base_url')
        else:
            base_url = f'{self.schema}://{self.host}:{self.port}'
        if url.startswith(('http', 'https')):
            endpoint = url
        else:
            endpoint = f'{base_url}{url}'
        rsp = self.http.request(method, endpoint, **kwargs)
        if (
                HTTPStatus.OK.value
                <= rsp.status <
                HTTPStatus.MULTIPLE_CHOICES.value
        ):
            return rsp
        data = rsp.data.decode('utf-8')
        raise ConsulError(data, original=endpoint)


class BaseConsulAPI(object):
    """ Consul接口基类 """

    def __init__(self, client: t.Optional[BaseConsulClient] = None) -> None:
        """ 初始化实例

        @param client: 客户端
        """
        self.client = client

    def __new__(cls, *args: t.Any, **kwargs: t.Any) -> BaseConsulAPI:
        """ 创建接口实例

        @param args  : 位置参数
        @param kwargs: 接口参数
        """
        instance = super(BaseConsulAPI, cls).__new__(cls)
        current_consul_api_instance = instance
        # 获取当前类中为BaseConsulAPI实例的类属性
        all_apis = getmembers(cls, predicate=is_consul_api)
        for name, api in all_apis:
            # 向子API实例传递客户端CLIENT实例
            api.client = instance.client
            setattr(instance, name, api)
        return current_consul_api_instance

    def _get(self, url: t.Text, **kwargs: t.Any) -> t.Any:
        """ 请求方法 - get

        @param url: 请求地址
        @param kwargs: 请求参数
        @return: t.Any
        """
        hasattr(self, 'base_url') and kwargs.update({'base_url': self.base_url})
        return self.client.get(url, **kwargs)

    def _post(self, url, **kwargs) -> t.Any:
        """ 请求方法 - post

        @param url: 请求地址
        @param kwargs: 请求参数
        @return: t.Any
        """
        hasattr(self, 'base_url') and kwargs.update({'base_url': self.base_url})
        return self.client.post(url, **kwargs)

    def _put(self, url, **kwargs) -> t.Any:
        """ 请求方法 - put

        @param url: 请求地址
        @param kwargs: 请求参数
        @return: t.Any
        """
        hasattr(self, 'base_url') and kwargs.update({'base_url': self.base_url})
        return self.client.put(url, **kwargs)

    def _patch(self, url, **kwargs) -> t.Any:
        """ 请求方法 - patch

        @param url: 请求地址
        @param kwargs: 请求参数
        @return: t.Any
        """
        hasattr(self, 'base_url') and kwargs.update({'base_url': self.base_url})
        return self.client.patch(url, **kwargs)

    def _delete(self, url, **kwargs) -> t.Any:
        """ DELETE请求方法

        :param url: 请求地址
        :param kwargs: 命名参数
        :return: t.Any
        """
        hasattr(self, 'base_url') and kwargs.update({'base_url': self.base_url})
        return self.client.delete(url, **kwargs)
