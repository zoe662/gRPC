# gRPC
* 客戶端可以遠程調用伺服器方法的協議

  
* protocol buffers
    - IDL(Interface Definition Language) 介面描述語言
    - message interchange format 資料交換格式
    
# 官方文件
[gRPC](https://grpc.io/docs/what-is-grpc/) <br>
[proto3](https://developers.google.com/protocol-buffers/docs/proto3)


# requirements

* Python 3.5 以上
* pip version 9.0.1 以上

```commandline
pip install grpcio
pip install grpcio-tools  
pip install protobuf
```

# working with protocol buffers
* 建立.proto: 定義資料架構
* 建立 proto .py檔
```commandline
python -m grpc_tools.protoc -I ./ --python_out=./ --grpc_python_out=. .protofile/user.proto
```