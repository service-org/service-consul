#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from service_consul.core.consul import ConsulClient
from service_core.core.context import WorkerContext
from service_consul.constants import CONSUL_CONFIG_KEY
from service_core.core.service.dependency import Dependency


class Consul(Dependency):
    """ Consul依赖类

    1. 基于它的注册发现子类常对外暴露client和cache所以无需重写get_instance方法
    2. 此扩展无需在每次请求时都注入一次get_instance实例,请设置skip_inject=True
    """

    def __init__(
            self,
            alias: t.Text,
            connect_options: t.Optional[t.Dict[t.Text, t.Any]] = None,
            **kwargs: t.Text
    ) -> None:
        """ 初始化实例

        @param alias: 配置别名
        @param connect_options: 连接配置
        @param kwargs: 其它配置
        """
        self.alias = alias
        self.client = None
        self.connect_options = connect_options or {}
        super(Consul, self).__init__(**kwargs)

    def setup(self) -> None:
        """ 生命周期 - 载入阶段

        @return: None
        """
        connect_options = self.container.config.get(f'{CONSUL_CONFIG_KEY}.{self.alias}.connect_options', default={})
        # 防止YAML中声明值为None
        connect_options = (connect_options or {}) | self.connect_options
        self.client = ConsulClient(**connect_options)

    def get_instance(self, context: WorkerContext) -> t.Any:
        """ 获取注入对象

        @param context: 上下文对象
        @return: t.Any
        """
        return self.client
