#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from service_consul.core.consul import Consul
from service_core.core.configure import Configure
from service_consul.constants import CONSUL_CONFIG_KEY


class ConsulProxy(object):
    """ Consul代理类 """

    def __init__(self, config: Configure, **option: t.Text) -> None:
        """ 初始化实例

        @param config: 配置对象
        @param option: 其它选项
        """
        self.config = config
        self.option = option

    def __call__(self, alias: t.Text, **option: t.Text) -> Consul:
        """ 代理可调用

        @param alias: 配置别名
        @param option: 其它选项
        @return: Consul
        """
        cur_option = self.option
        # 调用时传递的参数配置优先级最高
        cur_option.update(option)
        config = self.config.get(f'{CONSUL_CONFIG_KEY}.{alias}', default={})
        # 调用时传递的参数配置优先级最高
        config.update(cur_option)
        return Consul(**config)
