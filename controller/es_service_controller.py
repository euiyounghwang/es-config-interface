from fastapi import APIRouter, Request
import json
import datetime
from injector import logger, ESServiceHandlerInject
from service.status_handler import (StatusHanlder, StatusException)
# from typing import Optional
import datetime
from repository.schema import Alert



app = APIRouter(
    prefix="/service",
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


@app.get("/get_es_service_ssl_api", 
          status_code=StatusHanlder.HTTP_STATUS_200,
          responses={
            200: {"description" : "OK"},
            500 :{"description" : "Unexpected error"}
          },
          description="Sample Payload : GET http://localhost:8004/service/get_es_service_ssl_api", 
          summary="Get the ssl certs from the ES host")
async def get_es_service_api(request: Request, es_host="http://localhost:9200"):
    ''' get json config file from local disk '''
   
    """request.client.host"""
    response =  await ESServiceHandlerInject.get_es_service_ssl_api(es_host)
    if isinstance(response, dict):
        logger.info('Remote IP Address = {}, get_es_service_api: {}]'.format(request.client.host, response))

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