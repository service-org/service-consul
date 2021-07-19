#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import os
import json
import pprint
import eventlet
import typing as t

from logging import getLogger
from collections import namedtuple

from .base import BaseConsulKvRegistDependency

logger = getLogger(__name__)
Connection = namedtuple('Connection', ['host', 'port'])
DEFAULT_APISIX_CONSUL_KEY_FORMAT = 'apisix-service-upstreams/$name/$host:$port'
DEFAULT_APISIX_CONSUL_VAL_FORMAT = '{"weight": 1, "max_fails": 2, "fail_timeout": 1}'


class ApisixConsulRegistDependency(BaseConsulKvRegistDependency):
    """ Apisix注册类 """

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        """ 初始化实例

        @param   args: 位置参数
        @param kwargs: 命名参数
        """
        kwargs.setdefault('key_format', DEFAULT_APISIX_CONSUL_KEY_FORMAT)
        kwargs.setdefault('val_format', DEFAULT_APISIX_CONSUL_VAL_FORMAT)
        super(ApisixConsulRegistDependency, self).__init__(*args, **kwargs)

    def watch(self) -> None:
        """ 用阻塞查询监控键变化

        doc: https://www.consul.io/api/features/blocking

        @return:None
        """
        prefix = self.ident.split('/')[0]
        index, wait, sleep_seconds_when_exception = '0', '5m', 1
        while True:
            try:
                fields = {'keys': True, 'index': index, 'wait': wait}
                resp = self.client.kv.get_kv(prefix, fields=fields)
                data, curr = json.loads(resp.data.decode('utf-8')), {}
                for key in data:
                    all_parts = key.rsplit('/')
                    name, addr = all_parts[-2], all_parts[-1]
                    connection = Connection(*addr.split(':', 1))
                    curr.setdefault(name, set())
                    curr[name].add(connection)
                for name in curr:
                    self.cache.setdefault(name, set())
                    self.cache[name] = curr[name]
                index = resp.headers.get('X-Consul-Index', index)
            except BaseException:
                logger.error(f'unexpected error while watch key', exc_info=True)
                eventlet.sleep(sleep_seconds_when_exception)
                continue
            all_service_str = os.linesep + pprint.pformat(self.cache)
            logger.debug(f'registered services {all_service_str} changed')
