#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from service_consul.core.consul import ConsulClient
from service_consul.constants import CONSUL_CONFIG_KEY
from service_core.core.service.dependency import Dependency


class Consul(Dependency):
    """ Consul依赖类 """

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
        config.update(self.kwargs)
        self.client = ConsulClient(**config)
