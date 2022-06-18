import hashlib
# 使用setting.py里面生成的字符串作为盐
from django_day01.settings import SECRET_KEY


def md5(strs):
    '''
    传入字符串会经过md5编码，转成加密的字符串
    :param strs:
    :return:
    '''
    obj=hashlib.md5(SECRET_KEY.encode('utf8'))
    obj.update(strs.encode('utf8'))
    return obj.hexdigest()