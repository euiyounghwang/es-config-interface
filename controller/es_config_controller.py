from fastapi import APIRouter
import json
import datetime
from injector import logger, ESConfigHandlerInject
from service.status_handler import (StatusHanlder, StatusException)
# from typing import Optional
import datetime
from io import BytesIO


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
          description="Sample Payload : ", 
          summary="Get json for prometheus export email")
async def get_hostname_from_domain_controller():
    ''' get json config file from local disk '''
   
    response =  await ESConfigHandlerInject.get_hostname_from_domain()
    if isinstance(response, dict):
        logger.info('get_hostname_from_domain_controller - {}'.format(json.dumps(response, indent=2)))

    return {}

