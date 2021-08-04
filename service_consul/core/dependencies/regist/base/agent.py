#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from . import ConsulRegistDependency


class ConsulAgentRegistDependency(ConsulRegistDependency):
    """ Consul代理注册类 """

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        """ 初始化实例

        @param   args: 位置参数
        @param kwargs: 命名参数
        """
        super(ConsulAgentRegistDependency, self).__init__(*args, **kwargs)

    def stop(self) -> None:
        """ 生命周期 - 停止阶段

        @return: None
        """
        raise NotImplementedError

    def watch(self) -> None:
        """ 用阻塞查询监控键变化

        @return: None
        """
        raise NotImplementedError
