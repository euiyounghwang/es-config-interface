
import requests
from service.status_handler import StatusException
from util.es_util import json_read_config


class ESConfigHandler(object):
    
    def __init__(self, logger):
        ''' Get the number of hosts from the file to generate a excel file included active spark jobs'''
        self.logger = logger
        # self.hosts = hosts

    
    async def get_service_mail_config(self):
        ''' get_hostname_from_domain '''
        try:
            ''' get all hots '''
            hosts = json_read_config("./repository/mail_config.json")
            self.logger.info(f"get_service_mail_config : {hosts}")
            
            ''' get ./repositoy/mail_config.json '''
            return hosts
        
        except Exception as e:
           return StatusException.raise_exception(str(e))
        

    async def get_service_global_config(self):
        ''' get_hostname_from_domain '''
        try:
            ''' get all hots '''
            hosts = json_read_config("./repository/config.json")
            self.logger.info(f"get_service_global_config : {hosts}")
            
            ''' get ./repositoy/config.json '''
            return hosts
        
        except Exception as e:
           return StatusException.raise_exception(str(e))

