#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from .base import BaseConsulKvRegistDependency

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
        pass
