#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations


import typing as t


from .apis.agent import AgentAPI
from .base import BaseConsulClient


class ConsulClient(BaseConsulClient):
    """ Consul客户端类 """

    agent = AgentAPI()
