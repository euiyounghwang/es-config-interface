from fastapi import APIRouter
import json
import datetime
from injector import logger, ESConfigHandlerInject
from service.status_handler import (StatusHanlder, StatusException)
# from typing import Optional
import datetime
from repository.schema import Search


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
        #   responses={
        #     200: {"description" : "OK"},
        #     404 :{"description" : "URl not found"}
        #   },
          description="Sample Payload : http://localhost:8004/config/get_mail_config, Please change the json file if you want to change to '/home/biadmin/es_config_interface/repository/config.json", 
          summary="Get prometheus export mail configuration")
async def get_mail_config():
    ''' get json config file from local disk '''
   
    response =  await ESConfigHandlerInject.get_service_mail_config()
    if isinstance(response, dict):
        logger.info('get_mail_config - {}'.format(json.dumps(response, indent=2)))

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