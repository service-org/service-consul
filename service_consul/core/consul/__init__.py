#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

if t.TYPE_CHECKING:
    from .base import BaseConsulAPI

    # 接口类型
    ConsulAPI = t.TypeVar('ConsulAPI', bound=BaseConsulAPI)

from .apis.kv import KvAPI
from .base import BaseConsulClient


class ConsulClient(BaseConsulClient):
    """ Consul客户端类 """

    # https://www.consul.io/api-docs/kv
    kv = KvAPI()
