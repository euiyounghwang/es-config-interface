from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware
from controller import (es_config_controller, es_download_controller, es_log_controller, es_service_controller)
from config.log_config import create_log
from threading import Thread
import time

logger = create_log()
app = FastAPI(
    title="ES Configuration API Service",
    description="ES Configuration API Service",
    version="0.0.1",
    # terms_of_service="http://example.com/terms/",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def custom_openapi():
    if not app.openapi_schema:
        app.openapi_schema = get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            description=app.description,
            terms_of_service=app.terms_of_service,
            contact=app.contact,
            license_info=app.license_info,
            routes=app.routes,
            tags=app.openapi_tags,
            servers=app.servers,
        )
        for _, method_item in app.openapi_schema.get('paths').items():
            for _, param in method_item.items():
                responses = param.get('responses')
                # remove 422 response, also can remove other status code
                if '422' in responses:
                    del responses['422']
    return app.openapi_schema

app.openapi = custom_openapi


def start_worker():
    while True:
        print('[main]: starting worker...')
        time.sleep(10)
        
        
    
''' http://localhost:8100/docs '''

@app.get("/", tags=['API'],  
         status_code=200,
         description="Default GET API", 
         summary="Return Json")
async def root():
    return {"message": "Hello World"}


'''
@app.get("/test", tags=['API'],  
         status_code=200,
         description="Default GET Param API", 
         summary="Return GET Param Json")
async def root_with_arg(id):
    logger.info('root_with_arg - {}'.format(id))
    return {"message": "Hello World [{}]".format(id)}


@app.get("/test/{id}", tags=['API'],  
         status_code=200,
         description="Default GET with Body API", 
         summary="Return GET with Body Json")
async def root_with_param(id):
    logger.info('root_with_arg - {}'.format(id))
    return {"message": "Hello World [{}]".format(id)}
'''

# router
''' Enter the host name of the master node in the spark cluster to collect the list of running spark jobs. '''
app.include_router(es_config_controller.app, tags=["Prometheus Configuration API"], )
app.include_router(es_download_controller.app, tags=["Prometheus Download API"], )
app.include_router(es_service_controller.app, tags=["Prometheus Service API"], )
app.include_router(es_log_controller.app, tags=["Log API"], )

# _worker_thread = Thread(target=start_worker, daemon=False)
# _worker_thread.start()

