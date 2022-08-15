from jose import jwt
from jose.exceptions import ExpiredSignatureError, JWTError

SECRET_KEY = "123456"
def token_decode(token):
    try:
        payload = jwt.decode(token, SECRET_KEY)
        return payload
    # 否则，则捕获异常，进行提示
    except ExpiredSignatureError as e:
        print('token过期了！')
        return None
    except JWTError as e:
        print('token验证失败！')
        return None