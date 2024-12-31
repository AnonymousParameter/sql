import jwt
import datetime
import time
#from jwt.exceptions import ExpiredSignatureError

# 全局密钥
secret = '123456'  #自定义密钥


# 生成token
def encode_func(user):
    # user = {'id': 1, 'password':12121}
    dic = {
        'exp': datetime.datetime.now() + datetime.timedelta(days=1),  # 过期时间
        'iat': datetime.datetime.now() - datetime.timedelta(days=1),  # 开始时间
        'iss': 'liuchsh',
        'data': user
    }
    encoded = jwt.encode(dic, secret, algorithm='HS256')
    return encoded


# 解析token
def decode_func(token):
    decode = jwt.decode(token, secret, issuer='liuchsh', algorithms=['HS256'])
    # 返回解码出来的data
    return decode['data']

