#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from service_consul.core.dependencies.consul import ConsulDependency


class ConsulRegistDependency(ConsulDependency):
    """ Consul注册基类 """

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        """ 初始化实例

        @param   args: 位置参数
        @param kwargs: 命名参数
        """
        super(ConsulRegistDependency, self).__init__(*args, **kwargs)

    def start(self) -> None:
        """ 生命周期 - 启动阶段

        @return: None
        """
        func = self.watch
        args, kwargs, tid = (), {}, f'{self}.self_watch'
        self.container.spawn_splits_thread(func, args, kwargs, tid=tid)

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
