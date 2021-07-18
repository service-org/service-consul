#! -*- coding: utf-8 -*-
#
# author: forcemain@163.com


from service_core.exception import RemoteError


class ConsulApiError(RemoteError):
    """ 接口异常 """
    pass


class ConsulDnsError(RemoteError):
    """ DNS异常 """
    pass


class ConsulGrpcError(RemoteError):
    """ Grpc异常 """
    pass
