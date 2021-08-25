#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import os
import json
import pprint
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

    def __init__(self, alias: t.Text, key_format: t.Text = '', val_format: t.Text = '', **kwargs: t.Text) -> None:
        """ 初始化实例

        @param alias: 配置别名
        @param key_prefix: 键格式串
        @param val_format: 值格式串
        @param skip_inject: 跳过注入
        @param skip_loaded: 跳过加载
        """
        super(BaseConsulKvRegist, self).__init__(alias, **kwargs)
        self.cache = {}
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
        self.client.kv.put_kv(self.ident, body=self.value)
        super(BaseConsulKvRegist, self).start()

    def stop(self) -> None:
        """ 生命周期 - 关闭阶段

        @return: None
        """
        self.client.kv.delete_kv(self.ident)
        super(BaseConsulKvRegist, self).stop()

    def watch(self) -> None:
        """ 用阻塞查询监控键变化

        doc: https://www.consul.io/api/features/blocking

        @return:None
        """
        prefix, exception_occurred = self.ident.split('/')[0], False
        index, wait, sleep_seconds_when_exception = '0', '5m', 1
        while not self.stopped:
            try:
                # 通过传递index和wait参数来进行阻塞查询接口数据是否变更
                fields = {'keys': True, 'index': index, 'wait': wait,
                          'dc': self.data_center, 'recurse': True}
                # 如果之前发生了未知异常(如连接异常)则尝试重新注册此服务
                exception_occurred and self.client.kv.put_kv(
                    self.ident, body=self.value, retries=False
                )
                resp = self.client.kv.get_kv(prefix, fields=fields, retries=False)
                exception_occurred = False
                data, cache = json.loads(resp.data.decode('utf-8')), {}
                for key in data:
                    if not key.startswith(prefix):
                        warn = (f'got invalid key {key} '
                                f'that not startswith {prefix}, ignore')
                        logger.warning(warn)
                        continue
                    if key.count('/') != 2:
                        warn = (f'got invalid key {key} '
                                f'that not {key}/name/host:port, ignore')
                        logger.warning(warn)
                        continue
                    all_parts = key.rsplit('/')
                    name, addr = all_parts[-2], all_parts[-1]
                    connection = Connection(*addr.split(':', 1))
                    cache.setdefault(name, set())
                    cache[name].add(connection)
                self.cache = cache
                all_service_str = os.linesep + pprint.pformat(self.cache)
                logger.debug(f'registered services {all_service_str} updated')
                index = resp.headers.get('X-Consul-Index', index)
                # 优雅处理如ctrl + c, sys.exit, kill thread时的异常
            except (KeyboardInterrupt, SystemExit, GreenletExit):
                break
            except:
                exception_occurred = True
                # 应该避免其它未知异常中断当前触发器导致检测任务无法被调度
                logger.error(f'unexpected error while watch key', exc_info=True)
                eventlet.sleep(sleep_seconds_when_exception)
