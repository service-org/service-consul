#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from service_consul.core.consul.base import ConsulAPI


class KvAPI(ConsulAPI):
    """ Agent接口类

    doc: https://www.consul.io/api-docs/kv
    """

    def get_kv(self, key: t.Text, **kwargs: t.Text) -> t.Text:
        """ 读取键值

        doc: https://www.consul.io/api-docs/kv#read-key

        @param key: 指定键名
        @param kwargs: 请求参数
        @return: t.Text
        """
        return self._get(f'/v1/kv/{key}', **kwargs)

    def put_kv(self, key: t.Text, **kwargs: t.Text) -> t.Text:
        """ 创建键值

        doc: https://www.consul.io/api-docs/kv#create-update-key

        @param key: 指定键名
        @param kwargs: 请求参数
        @return: t.Text
        """
        return self._put(f'/v1/kv/{key}', **kwargs)

    def delete_kv(self, key: t.Text, **kwargs: t.Text) -> t.Text:
        """ 删除键值

        doc: https://www.consul.io/api-docs/kv#delete-key

        @param key: 指定键名
        @param kwargs: 请求参数
        @return: t.Text
        """
        return self._delete(f'/v1/kv/{key}', **kwargs)
