# 运行环境

|system |python | 
|:------|:------|      
|cross platform |3.9.16|

# 组件安装

```shell
pip install -U service-consul 
```

# 服务配置

> config.yaml

```yaml
CONSUL:
  test:
    host: 127.0.0.1
    port: 8500
CONTEXT:
  - service_consul.cli.subctxs.consul:Consul
```

# 基础用法

> facade.py

```python
#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from logging import getLogger
from service_croniter.core.entrypoints import croniter
from service_core.core.service import Service as BaseService
from service_consul.core.dependencies import ApiSixConsulKvRegist

logger = getLogger(__name__)


class Service(BaseService):
    """ 微服务类 """

    # 微服务名称
    name = 'demo'
    # 微服务简介
    desc = 'demo'

    # 作为依赖项
    apisix = ApiSixConsulKvRegist(alias='test')

    @croniter.cron('* * * * * */1')
    def test_croniter_every_second_with_exec_atonce(self) -> None:
        """ 测试每秒且立即执行

        More expr_format: https://github.com/kiorky/croniter
        """
        logger.debug('yeah~ yeah~ yeah~, i am called ~')
```

> facade.py

```python
#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

from project import Service

app = Service()
```

# 运行服务

> core start facade --debug

# 接口调试

> core shell --shell `shell`

```shell
C:\Program Files\Python39\lib\site-packages\service_core-0.0.1-py3.9.egg\service_core\cli\main.py:39: UserWarning:
* eventlet 0.31.1
    - platform: macOS 10.15.7
      error  : changelist must be an iterable of select.kevent objects
      issue  : https://github.com/eventlet/eventlet/issues/670#issuecomment-735488189
    - platform: macOS 10.15.7
      error  : monkey_patch causes issues with dns .local #694
      issue  : https://github.com/eventlet/eventlet/issues/694#issuecomment-806100692

2021-08-04 11:22:02,236 - 13808 - DEBUG - load subcmd service_core.cli.subcmds.debug:Debug succ
2021-08-04 11:22:02,237 - 13808 - DEBUG - load subcmd service_core.cli.subcmds.shell:Shell succ
2021-08-04 11:22:02,237 - 13808 - DEBUG - load subcmd service_core.cli.subcmds.start:Start succ
2021-08-04 11:22:02,238 - 13808 - DEBUG - load subcmd service_core.cli.subcmds.config:Config succ
2021-08-04 11:22:02,332 - 13808 - DEBUG - load subctx service_core.cli.subctxs.config:Config succ
2021-08-04 11:22:02,332 - 13808 - DEBUG - load subctx service_consul.cli.subctxs.consul:Consul succ
PtPython - 3.9.6 (tags/v3.9.6:db3ff76, Jun 28 2021, 15:26:21) [MSC v.1929 64 bit (AMD64)]
>>> import json
>>> resp = s.consul.proxy(alias='test').kv.get_kv('apisix-service-upstreams', fields={'keys': True})
>>> json.loads(resp.data.decode('utf-8'))
['apisix-service-upstreams/demo/10.219.255.176:49234']
```

# 运行调试

> core debug --port `port`
