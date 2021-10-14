#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com

from __future__ import annotations

import typing as t

from service_client.core.client import BaseClientAPI


class KvAPI(BaseClientAPI):
    """ Kv接口类

    doc: https://www.consul.io/api-docs/kv
    """

    def read(self, key: t.Text, **kwargs: t.Any) -> t.Text:
        """ 读取键值

        doc: https://www.consul.io/api-docs/kv#read-key

        @param key: 指定键名
        @param kwargs: 请求参数
        @return: t.Text
        """
        return self._get(f'/v1/kv/{key}', **kwargs)

    def upsert(self, key: t.Text, **kwargs: t.Any) -> t.Text:
        """ 创建键值

        doc: https://www.consul.io/api-docs/kv#create-update-key

        @param key: 指定键名
        @param kwargs: 请求参数
        @return: t.Text
        """
        return self._put(f'/v1/kv/{key}', **kwargs)

    def delete(self, key: t.Text, **kwargs: t.Any) -> t.Text:
        """ 删除键值

        doc: https://www.consul.io/api-docs/kv#delete-key

        @param key: 指定键名
        @param kwargs: 请求参数
        @return: t.Text
        """
        return self._delete(f'/v1/kv/{key}', **kwargs)
