from fastapi import APIRouter, Request
import json
import datetime
from injector import logger, ESConfigHandlerInject
from service.status_handler import (StatusHanlder, StatusException)
# from typing import Optional
import datetime
from repository.schema import Alert



''' Enter the host name of the master node in the spark cluster to collect the list of running spark jobs. '''
app = APIRouter(
    prefix="/config",
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


@app.get("/get_mail_config", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            500 :{"description" : "Unexpected error"}
          },
          description="Sample Payload : GET http://localhost:8004/config/get_mail_config, Please change the json file if you want to change to '/home/biadmin/es_config_interface/repository/mail_config.json", 
          summary="Get prometheus export mail configuration")
async def get_mail_config(request: Request):
    ''' get json config file from local disk '''
   
    response =  await ESConfigHandlerInject.get_service_mail_config(request.client.host)
    # ip_by_host = await ESConfigHandlerInject.get_host_by_ipaddress(response)
    if isinstance(response, dict):
        # logger.info('ip_by_host [{}]'.format(ip_by_host))
        logger.info('Remote IP Address = {}, get_mail_config - Alert configuratiohn [alert_exclude_time : {}]'.format(request.client.host, response.get("alert_exclude_time")))
        
    return response


@app.get("/get_gloabl_config", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            500 :{"description" : "Unexpected error"}
          },
          description="Sample Payload : GET http://localhost:8004/config/get_gloabl_config, Please change the json file if you want to change to '/home/biadmin/es_config_interface/repository/config.json", 
          summary="Get prometheus export global configuration")
async def get_global_config():
    ''' get json config file from local disk '''
   
    response =  await ESConfigHandlerInject.get_service_global_config()
    if isinstance(response, dict):
        # logger.info('get_global_config - {}'.format(json.dumps(response, indent=2)))
        logger.info('get_mail_config - response global config with host info[{}]'.format(len(response)))

    return response


"""
@app.get("/get_host_info", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            500 :{"description" : "Unexpected error"}
          },
          description="Sample Payload : GET http://localhost:8004/config/get_host_info, Please change the json file if you want to change to '/home/biadmin/es_config_interface/repository/env_hosts.json", 
          summary="Get prometheus export global configuration")
async def get_host_info():
    ''' get json config file from local disk '''
   
    response =  await ESConfigHandlerInject.get_service_host_info()
    if isinstance(response, dict):
        # logger.info('get_global_config - {}'.format(json.dumps(response, indent=2)))
        logger.info('get_mail_config - response host info[{}]'.format(len(response)))

    return response
"""

@app.post("/update_mail_config", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            500 :{"description" : "Unexpected error"}
          },
          description="Sample Payload : POST http://localhost:8004/config/update_mail_config", 
          summary="Return POST alert results for writing json file internally")
async def set_mail_config(request: Alert):
    ''' 
    test curl
    curl -X 'POST'   'http://localhost:8004/config/update_mail_config' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{
      "env": "dev",
      "alert": "false"
    }'

    '''
    request_json = request.to_json()
    # logger.info("set_mail_config [request] : {}".format(json.dumps(request_json, indent=2)))

    # response =  await ESConfigHandlerInject.set_service_global_config()
    response =  await ESConfigHandlerInject.set_service_mail_config(request_json)
    if isinstance(response, dict):
        # logger.info('set_mail_config [response] - {}'.format(json.dumps(response, indent=2)))
        logger.info('set_mail_config [response] - {}'.format(response))

    return response
    

@app.post("/update_alert_config", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            500 :{"description" : "Unexpected error"}
          },
          description="Sample Payload : POST http://localhost:8004/config/update_alert_config", 
          summary="Return POST alert results for writing json file via jobs with Cache")
async def set_alert_config(request: Alert):
    ''' 
    test curl
    curl -X 'POST'   'http://localhost:8004/config/update_alert_config' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{
      "env": "dev",
      "alert": "false"
    }'

    '''
    request_json = request.to_json()
    response =  await ESConfigHandlerInject.set_service_alert_config(request_json)
    if isinstance(response, dict):
        # logger.info('set_alert_config [response] - {}'.format(json.dumps(response, indent=2)))
        logger.info('set_alert_config [response] - {}'.format(response))

    return response

"""
@app.post("/set_mail_config", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            404 :{"description" : "URl not found"}
          },
          description="Return Search results", 
          summary="Set prometheus export mail configuration")
async def set_mail_config(request: Search):
    ''' Search to Elasticsearch '''
    try:
        # logger.info("api_controller doc: {}".format(json.dumps(doc, indent=2)))
        # request_json = {k : v for k, v in request}
        request_json = request.to_json()
        # print(request, type(request), request.size, request_json, request_json['query_string'])
        logger.info("set_mail_config : {}".format(json.dumps(request_json, indent=2)))
    
        # return await SearchOmniHandlerInject.search(QueryBuilderInject, oas_query=request_json)
        return {}
       
    except Exception as e:
        logger.error(e)
"""