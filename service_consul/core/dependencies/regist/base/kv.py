#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import eventlet
import typing as t

from string import Template
from logging import getLogger
from greenlet import GreenletExit
from collections import namedtuple

from . import BaseConsulRegist

logger = getLogger(__name__)
Connection = namedtuple('Connection', ['host', 'port'])


class BaseConsulKvRegist(BaseConsulRegist):
    """ Consul KV注册类 """

    def __init__(self, alias: t.Text, key_format: t.Text = '', val_format: t.Text = '', **kwargs: t.Any) -> None:
        """ 初始化实例

        @param alias: 配置别名
        @param key_prefix: 键格式串
        @param val_format: 值格式串
        @param skip_inject: 跳过注入
        @param skip_loaded: 跳过加载
        """
        super(BaseConsulKvRegist, self).__init__(alias, **kwargs)
        self.ident = None
        self.value = None
        self.key_format = key_format  # DEFAULT_APISIX_CONSUL_KEY_FORMAT
        self.val_format = val_format  # DEFAULT_APISIX_CONSUL_VAL_FORMAT

    def setup(self) -> None:
        """ 生命周期 - 载入阶段

        @return: None
        """
        super(BaseConsulKvRegist, self).setup()
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
        self.client.kv.upsert(self.ident, body=self.value)
        super(BaseConsulKvRegist, self).start()

    def stop(self) -> None:
        """ 生命周期 - 关闭阶段

        @return: None
        """
        self.client.kv.delete(self.ident)
        super(BaseConsulKvRegist, self).stop()

    def watch(self) -> None:
        """ 用阻塞查询监控键变化

        doc: https://www.consul.io/api/features/blocking

        @return:None
        """
        prefix = self.ident.split('/')[0]
        index, wait, sleep = '0', '10m', 1
        while not self.stopped:
            try:
                # 通过传递index和wait参数来进行阻塞查询接口数据是否变更
                fields = {'keys': True, 'index': index, 'wait': wait,
                          'dc': self.client.data_center, 'recurse': True}
                self.client.kv.upsert(self.ident, body=self.value, retries=False)
                resp = self.client.kv.read(prefix, fields=fields, retries=False)
                index = resp.headers.get('X-Consul-Index', index)
                # 优雅处理如ctrl + c, sys.exit, kill thread时的异常
            except (KeyboardInterrupt, SystemExit, GreenletExit):
                break
            except:
                # 应该避免其它未知异常中断当前触发器导致检测任务无法被调度
                logger.error(f'unexpected error while watch key', exc_info=True)
                eventlet.sleep(sleep)
