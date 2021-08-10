#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from service_consul.core.consul import ConsulClient
from service_consul.constants import CONSUL_CONFIG_KEY
from service_core.core.service.dependency import Dependency


class Consul(Dependency):
    """ Consul依赖类

    1. 基于它的注册发现子类常对外暴露client和cache所以无需重写get_instance方法
    2. 此扩展无需在每次请求时都注入一次get_instance实例,请设置skip_inject=True
    """

    def __init__(self, alias: t.Text, **kwargs: t.Text) -> None:
        """ 初始化实例

        @param alias: 配置别名
        @param skip_inject: 跳过注入
        @param skip_loaded: 跳过加载
        """
        self.alias = alias
        self.client = None
        self.center = kwargs.pop('data_center', '')
        skip_inject = kwargs.pop('skip_inject', False)
        skip_loaded = kwargs.pop('skip_loaded', False)
        self.kwargs = kwargs
        super(Consul, self).__init__(skip_inject=skip_inject, skip_loaded=skip_loaded)

    def setup(self) -> None:
        """ 生命周期 - 载入阶段

        @return: None
        """
        config = self.container.config.get(f'{CONSUL_CONFIG_KEY}.{self.alias}', default={})
        # 防止YAML中声明值为None
        config = config or {}
        config.update(self.kwargs)
        self.client = ConsulClient(**config)
