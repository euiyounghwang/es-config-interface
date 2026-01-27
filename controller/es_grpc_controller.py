from fastapi import APIRouter, Request
import json
import datetime
from injector import logger, ESGrpcServiceHandlerInject
from service.status_handler import (StatusHanlder, StatusException)
# from typing import Optional
import datetime
from repository.schema import gRPC

app = APIRouter(
    prefix="/gRPC",
)


'''
@app.get("/query", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="Sample Payload : http://localhost:8001/cluster/health?es_url=http://localhost:9200", 
          summary="DB Query")
async def get_db_query(es_url="http://localhost:9200"):
    # logger.info(es_url)
    # response =  SearchAPIHandlerInject.get_es_health(es_url)
    # if isinstance(response, dict):
    #     logger.info('SearchOmniHandler:get_es_info - {}'.format(json.dumps(response, indent=2)))

    return {}
'''


@app.post("/get_service_status", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            500 :{"description" : "Unexpected error"}
          },
          description="Sample Payload : POST http://localhost:8004/gRPC/get_service_status", 
          summary="Get the status of ES services using gRPC")
async def get_service_status(request_ip: Request, request: gRPC):
    ''' 
    test curl
    curl -X 'POST'   'http://localhost:8004/gRPC/get_service_status' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{
      "grpc_server_hostname": "localhost",
      "env": "dev"
    }'

    '''
    request_json = request.to_json()
    logger.info(f"request_ip.client.host : {request_ip.client.host}, request_json : {request_json}")
    response =  await ESGrpcServiceHandlerInject.get_service_status(request_ip.client.host, request_json)
    # if isinstance(response, dict):
    #     # logger.info('set_alert_config [response] - {}'.format(json.dumps(response, indent=2)))
    #     logger.info('set_alert_config [response] - {}'.format(response))

    return response
