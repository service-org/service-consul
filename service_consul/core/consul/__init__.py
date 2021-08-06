#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from .apis.kv import KvAPI
from .base import BaseConsulClient


class ConsulClient(BaseConsulClient):
    """ Consul客户端类 """

    # https://www.consul.io/api-docs/kv
    kv = KvAPI()
