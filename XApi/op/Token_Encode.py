import jwt
import time

#生成token
def token_encode(data):
    # print(data.account)
    # print(data.password)
    # 生成一个字典，包含我们的具体信息
    d = {
        # 公共声明
        'exp': time.time()+3000,  # (Expiration Time) 此token的过期时间的时间戳
        'iat': time.time(),  # (Issued At) 指明此创建时间的时间戳
        'iss': 'Bbback',  # (Issuer) 指明此token的签发者

        # 私有声明
        'data': {
            'account': data.account,
            'password': data.password,
            'timestamp': time.time()
        }
    }
    jwt_encode = jwt.encode(d, '123456', algorithm='HS256')
    # print(jwt_encode)
    return jwt_encode