#! /usr/bin/env python
# coding=utf8

import grpc
import protofile.user_pb2 as grpc_message
import protofile.user_pb2_grpc as grpc_service

class ReceivegRPC(object):
    def __init__(self, func):
        self.func = func
    def __call__(self, *args, **kwargs):
        response = self.func(self, *args, **kwargs)
        if response.data.error:
            print('error: ' + response.data.error)
        else:
            pass
        return response

class User:
    def __init__(self, url):
        self.conn = grpc.insecure_channel(url)
        self.stub = grpc_service.UserStub(channel=self.conn)

    @ReceivegRPC
    def send(self, func, request):
        response = func(request)
        # print(response)
        return response

    def login(self, user, pwd):
        params = grpc_message.LoginPayloads(user=user, pwd=pwd)
        payload = grpc_message.UserPayloads(login=params)
        request = grpc_message.UserRequest(payload=payload)
        # response = self.stub.Login(request)
        response = self.send(self.stub.Login, request)
        self.token = response.data.login.token

    def ping(self, ping):
        params = grpc_message.PingPayloads(text=ping)
        payload = grpc_message.UserPayloads(ping=params)
        request = grpc_message.UserRequest(auth=self.token, payload=payload)
        # request = grpc_message.UserRequest(auth='self.token', payload=payload)
        # response = self.stub.Ping(request)
        response = self.send(self.stub.Ping, request)
        pong = response.data.ping.text
        print('Ping ' + pong)





if __name__ == '__main__':
    url = 'localhost:50052'
    client = User(url)
    client.login('user', 'pwd')
    client.ping('hello')

