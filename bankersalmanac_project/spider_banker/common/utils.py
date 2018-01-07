# -*- coding: utf-8 -*-

import hashlib


def get_md5(argument):
    '''
    将字符串转换为MD5
    :param url:
    :return:
    '''
    if isinstance(argument, str):
        argument = argument.encode("utf-8")
    m = hashlib.md5()
    m.update(argument)
    return m.hexdigest()