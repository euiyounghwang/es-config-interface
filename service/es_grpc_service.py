
import requests
from service.status_handler import StatusException
from util.es_util import json_read_config
import json
from service.redis_service import Redis_Client
import os
import socket
from service.db import database
from dotenv import load_dotenv
from service.search_core import Search_Core

''' gRPC '''
''' pip install grpcio grpcio-tools'''
import grpc
import service.service_pb2
import service.service_pb2_grpc
from google.protobuf.json_format import MessageToJson, Parse

load_dotenv()
# load_dotenv() # will search for .env file in local folder and load variables
# Reload the variables from your .env file, overriding existing ones
# load_dotenv(".env_server", override=True)


class ESGrpcServiceHandler(object):
    
    def __init__(self, logger):
        self.logger = logger

    async def get_service_status(self, request_ip, request_json):
        ''' return {"127.0.0.1" : "localhost"}'''
        try:
            ''' load a config file'''
            gRPC_config_json = json_read_config("./repository/gRPC_config.json")
            with grpc.insecure_channel("{}:{}".format(request_json.get("grpc_server_hostname"), gRPC_config_json.get(request_json.get("env").lower()))) as channel:
                # with grpc.insecure_channel("{}:50002".format(gRPC_server_host)) as channel:
                stub = service.service_pb2_grpc.GreeterStub(channel)

                '''
                response = stub.SayHello(service_pb2.HelloRequest(name='azamman'))
                print("Greeter client received: " + response.message)

                # 함수 2 호출
                response2 = stub.GetServerStatus(service_pb2.StatusRequest(id='123'))
                print("서버 상태:", "활성" if response2.active else "비활성")
                '''

                '''
                # 1. Convert a Python dictionary (JSON) to a Protobuf message before sending
                json_input = {"name": "Test User", "id": 123}
                request_message = Parse(json.dumps(json_input), pb2.YourRequestMessage())
                response = stub.YourMethod(request_message)
                '''
                
                response_dict = stub.GetMetricsStatus(service.service_pb2.MetricsStatusRequest(env=request_json.get("env").lower()))
                # print(f"response_dict : {response_dict}, type {type(response_dict)}")

                ''' MessageToJson(message): Serializes a Protobuf message object to a JSON formatted string.'''
                Jsons = MessageToJson(response_dict)
                Jsons_dict = json.loads(Jsons).get('metrics')
                # print(f"MessageToJson : {Jsons}, type : {type(Jsons_dict)}, key : {Jsons_dict.get('token')}")
                self.logger.info(json.dumps(Jsons_dict, indent=2))

                return Jsons_dict
        
        except Exception as e:
           return StatusException.raise_exception(str(e))