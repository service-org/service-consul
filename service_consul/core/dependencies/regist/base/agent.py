#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from . import BaseConsulRegist


class BaseConsulAgentRegist(BaseConsulRegist):
    """ Consul代理注册类 """

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:
        """ 初始化实例

        @param   args: 位置参数
        @param kwargs: 命名参数
        """
        super(BaseConsulAgentRegist, self).__init__(*args, **kwargs)

    def watch(self) -> None:
        """ 用阻塞查询监控键变化

        @return: None
        """
        raise NotImplementedError
