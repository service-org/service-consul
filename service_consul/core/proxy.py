#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from service_core.core.configure import Configure
from service_consul.core.client import ConsulClient
from service_consul.constants import CONSUL_CONFIG_KEY


class ConsulProxy(object):
    """ Consul代理类 """

    def __init__(self, config: Configure, **options: t.Text) -> None:
        """ 初始化实例

        @param config: 配置对象
        @param options: 其它选项
        """
        self.config = config
        self.options = options

    def __call__(self, alias: t.Text, **options: t.Text) -> ConsulClient:
        """ 代理可调用

        @param alias: 配置别名
        @param options: 其它选项
        @return: ConsulClient
        """
        cur_options = self.options
        # 调用时传递的参数配置优先级最高
        cur_options.update(options)
        config = self.config.get(f'{CONSUL_CONFIG_KEY}.{alias}.connect_options', default={})
        # 调用时传递的参数配置优先级最高
        config.update(cur_options)
        return ConsulClient(**config)
