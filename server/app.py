#! /usr/bin/env python
# coding=utf8

import time
from concurrent import futures
import grpc
import protofile.user_pb2 as grpc_message
import protofile.user_pb2_grpc as grpc_service
import server

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
SECRET_KEY = 'SECRET_KEY'

class SendgRPC(object):
    def __init__(self, func):
        self.func = func

    def __call__(self, request, context):
        try:
            if self.func.__name__ == "Login":
                pass
            else:
                server.auth(request.auth)
            response = self.func(self, request, context)
            return grpc_message.UserResponse(data=response)
        except Exception as e:
            error = grpc_message.UserResults(error=str(e))
            return grpc_message.UserResponse(data=error)

class UserService(grpc_service.UserServicer):
    def __init__(self):
        pass

    @SendgRPC
    def Login(self, request, context):
        """
        user: user account
        pwd: user password
        """
        payload = request.payload.login
        user = payload.user
        pwd = payload.pwd
        print(user)
        token = server.login(user, pwd)
        print(token)
        params = grpc_message.LoginResponse(token=token)
        response = grpc_message.UserResults(login=params)
        return response

    @SendgRPC
    def Ping(self, request, context):
        """
        ping: string
        """
        payload = request.payload.ping.text
        params = grpc_message.PingResponse(text=payload)
        response = grpc_message.UserResults(ping=params)
        return response


def run():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    grpc_service.add_UserServicer_to_server(UserService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("start service...")
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    run()


