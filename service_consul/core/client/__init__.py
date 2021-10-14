#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from service_client.core.client import BaseClient

from .apis.kv import KvAPI


class ConsulClient(BaseClient):
    """ Consul客户端类 """

    # https://www.consul.io/api-docs/kv
    kv = KvAPI()

    def __init__(
            self,
            base_url: t.Optional[t.Text] = None,
            debug: t.Optional[bool] = None,
            acl_token: t.Optional[t.Text] = None,
            data_center: t.Optional[t.Text] = None,
            pool_options: t.Optional[t.Dict[t.Text, t.Any]] = None
    ) -> None:
        """ 初始化实例

        @param base_url: 基础路径
        @param debug: 开启调试 ?
        @param acl_token: Acl令牌
        @param data_center: 数据中心
        @param pool_options: 池配置
        """
        super(ConsulClient, self).__init__(
            base_url=base_url, debug=debug,
            pool_options=pool_options
        )
        self.acl_token = acl_token
        self.registered_services = {}
        self.data_center = data_center or ''

    def request(self, method: t.Text, url: t.Text, **kwargs: t.Any) -> t.Any:
        """ 请求处理方法

        :param method: 请求方法
        :param url: 请求地址
        :param kwargs: 请求参数
        :return: t.Any
        """
        if 'timeout' not in kwargs:
            kwargs['timeout'] = 2.0
        if 'headers' not in kwargs:
            kwargs['headers'] = {}
        if 'retries' not in kwargs:
            kwargs['retries'] = 2
        if self.acl_token:
            kwargs['headers']['X-Consul-Token'] = self.acl_token
        return super(ConsulClient, self).request(method, url, **kwargs)
