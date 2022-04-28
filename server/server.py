#! /usr/bin/env python
# coding=utf8
import jwt
import time
SECRET_KEY = "your-256-bit-secret"

def ifuser(user, pwd):
    db = {'user': 'pwd'}
    if (user in db.keys()) and (db[user] == pwd):
        return True
    else:
        return False

def login(user, pwd):
    if ifuser(user, pwd):
        headers = {"alg":"HS256","typ":"JWT"}
        payload = {"user": user, "exp": int(time.time()) + 60 * 60 * 24 * 7}
        # payload = '{"sub": "1234567890","name": "John Doe","iat": 1516239022}'

        token = jwt.encode(payload, SECRET_KEY, headers=headers, algorithm="HS256")
        return token
    else:
        raise Exception("wrong user or pwd")

def auth(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms="HS256")

    if payload['exp'] < int(time.time()):
        raise Exception("token expired")
    return payload

if __name__ == "__main__":
    token = login("1","1")
    decode = auth(token)
    print(decode)