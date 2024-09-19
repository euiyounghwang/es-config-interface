from fastapi import APIRouter, Request
import json
import datetime
from injector import logger, ESLogHandlerInject
from service.status_handler import (StatusHanlder, StatusException)
# from typing import Optional
import datetime
from repository.schema import Log


app = APIRouter(
    prefix="/log",
)


@app.get("/get_alert_log", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            500 :{"description" : "Unexpected error"}
          },
          description="Sample Payload : GET http://localhost:8004/log/get_alert_log", 
          summary="Get Alert log")
async def get_alert_log(request: Request):
    ''' get json config file from local disk '''
   
    response =  await ESLogHandlerInject.get_service_alert_log()
    if isinstance(response, dict):
        logger.info('get_alert_log: {}]'.format(response))
        
    return response


@app.get("/get_monitoring_log", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            500 :{"description" : "Unexpected error"}
          },
          description="Sample Payload : GET http://localhost:8004/log/get_monitoring_log", 
          summary="Get All services log")
async def get_monitoring_log(request: Request):
    ''' get json config file from local disk '''
   
    response =  await ESLogHandlerInject.get_service_monitoring_log()
    if isinstance(response, dict):
        logger.info('get_monitoring_log: {}]'.format(response))
        
    return response


@app.post("/create_log", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            500 :{"description" : "Unexpected error"}
          },
          description="Sample Payload : POST http://localhost:8004/log/create_log", 
          summary="Create_log")
async def set_monitoring_log(request_ip:  Request, request_log: Log):
    ''' 
    test curl
    curl -X 'POST'   'http://localhost:8004/log/set_log' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{
      "env": "dev",
      "alert": "false"
    }'

    '''
    logger.info("request.client.host - : {}".format(request_ip.client.host))
    request_json = request_log.to_json()
    response =  await ESLogHandlerInject.set_service_monitoring_log(request_ip.client.host, request_json)
    if isinstance(response, dict):
        logger.info('set_log [response] - {}'.format(response))

    return response

