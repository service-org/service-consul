#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from service_consul.core.consul.base import BaseConsulAPI

class AgentAPI(BaseConsulAPI):
    """ Agent接口类 """

    def agent_members(self):
        return self._get('/v1/agent/members')
