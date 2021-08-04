#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from service_core.cli.subctxs import Context
from service_core.core.configure import Configure
from service_consul.core.proxy import ConsulProxy


class Consul(Context):
    """ 用于调试Consul接口 """

    name: t.Text = 'consul'

    def __init__(self, config: Configure) -> None:
        """ 初始化实例

        @param config: 配置对象
        """
        super(Consul, self).__init__(config)
        self.proxy = ConsulProxy(config=config)
