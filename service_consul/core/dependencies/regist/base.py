#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from string import Template
from service_consul.core.dependencies.consul import ConsulDependency


class BaseConsulRegistDependency(ConsulDependency):
    """ Consul注册类 """

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        """ 初始化实例

        @param   args: 位置参数
        @param kwargs: 命名参数
        """
        super(BaseConsulRegistDependency, self).__init__(*args, **kwargs)

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


class BaseConsulAgentRegistDependency(BaseConsulRegistDependency):
    """ Consul代理注册类 """

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        """ 初始化实例

        @param   args: 位置参数
        @param kwargs: 命名参数
        """
        super(BaseConsulRegistDependency, self).__init__(*args, **kwargs)

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


class BaseConsulKvRegistDependency(BaseConsulRegistDependency):
    """ Consul键值注册类 """

    def __init__(self, alias: t.Text, key_format: t.Text = '', val_format: t.Text = '', **kwargs: t.Text) -> None:
        """ 初始化实例

        @param alias: 配置别名
        @param key_prefix: 键格式串
        @param val_format: 值格式串
        @param skip_inject: 跳过注入
        @param skip_loaded: 跳过加载
        """
        self.cache = {}
        self.ident = None
        self.value = None
        self.key_format = key_format
        self.val_format = val_format
        super(BaseConsulRegistDependency, self).__init__(alias, **kwargs)

    def setup(self) -> None:
        """ 生命周期 - 载入阶段

        @return: None
        """
        super(BaseConsulRegistDependency, self).setup()
        context = {
            'name': self.container.service.name,
            'host': self.container.service.host,
            'port': self.container.service.port,
        }
        self.ident = Template(self.key_format).safe_substitute(context)
        self.value = Template(self.val_format).safe_substitute(context)

    def start(self) -> None:
        """ 生命周期 - 启动阶段

        @return: None
        """
        self.client.kv.put_kv(self.ident)
        super(BaseConsulKvRegistDependency, self).start()

    def stop(self) -> None:
        """ 生命周期 - 关闭阶段

        @return: None
        """
        self.client.kv.delete_kv(self.ident)

    def watch(self) -> None:
        """ 用阻塞查询监控键变化

        @return: None
        """
        raise NotImplementedError
