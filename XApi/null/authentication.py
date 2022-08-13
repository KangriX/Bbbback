from jose import jwt
SECRET_KEY = "123456"
# 导入token校验的两种异常，一种是token超时异常，一种是token错误异常
from jose.exceptions import ExpiredSignatureError, JWTError
def token_is_true(token):
    # 尝试解密，解密成功后，秘钥，payload，有效时长校验通过，则会返回payload
    try:
        payload = jwt.decode(token,SECRET_KEY)
        print(payload)
        return True
    # 否则，则捕获异常，进行提示
    except ExpiredSignatureError as e:
        print('token过期了！')
        return False
    except JWTError as e:
        print('token验证失败！')
        return False