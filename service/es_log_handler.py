
import requests
from service.status_handler import StatusException
from util.es_util import json_read_config
import json
import os
import socket
from dotenv import load_dotenv
from service.db import database

load_dotenv()

class ESLogConfigHandler(object):
    
    def __init__(self, logger):
        ''' Get the number of hosts from the file to generate a excel file included active spark jobs'''
        self.logger = logger
        self.user = os.getenv('LOG_DB_USER')
        self.db_url = os.getenv('LOG_DB_URL')
        self.log_alert_sql = os.getenv('LOG_ALERT_SQL')
        self.log_monitoring_sql = os.getenv('LOG_MONITORING_SQL')
        self.insert_monitoring_log_sql = os.getenv('INSERT_MONITORING_LOG_SQL')
        
    
    async def get_service_alert_log(self):
        ''' get_service_alert_log '''
        db_obj = database(self.logger, self.user, self.db_url)
        try:
            db_obj.set_db_connection()
            result_dict = db_obj.select_oracle_query(self.log_alert_sql)
            '''  <class 'list'> <- result_dict '''
            self.logger.info(json.dumps(result_dict, indent=2))

            return result_dict

        except Exception as e:
           return StatusException.raise_exception(str(e))
        
        finally:
            db_obj.set_db_disconnection()

    
    async def get_service_monitoring_log(self):
        ''' get_service_monitoring_log '''
        db_obj = database(self.logger, self.user, self.db_url)
        try:
            db_obj.set_db_connection()
            result_dict = db_obj.select_oracle_query(self.log_monitoring_sql)
            '''  <class 'list'> <- result_dict '''
            self.logger.info(json.dumps(result_dict, indent=2))

            return result_dict

        except Exception as e:
           return StatusException.raise_exception(str(e))
        
        finally:
            db_obj.set_db_disconnection()
        
    
    async def set_service_monitoring_log(self, client_ip, request_json):
        ''' Update log to H2 database'''
        try:
            self.logger.info(f"request_json : {request_json}")

            ''' Save this log to H2 database'''
            db_obj = database(self.logger, self.user, self.db_url)
            db_obj.set_db_connection()
            ''' MONITORING_LOG (ENV_NAME, HOST_NAME, STATUS, LOG) VALUES('DEV', 'host', 'ES_RESTARTED', 'TEST MESSAGE');'''
            self.logger.info("{},{},{},{},{}".format(str(request_json.get("env")).upper(), str(request_json.get("host_name")),  str(request_json.get("status")), str(client_ip), str(request_json.get("message",""))))
            result_dict = db_obj.excute_oracle_query(self.insert_monitoring_log_sql.format(str(request_json.get("env")).upper(), str(request_json.get("host_name")),  str(request_json.get("status")), str(client_ip), str(request_json.get("message",""))))
            self.logger.info("result_dict for logs - {}".format(result_dict))

            db_obj.set_db_disconnection()

            return {"message": "Inserted log successfully."}
          
            ''' --------------- '''
        except Exception as e:
           self.logger.error(e)
           return StatusException.raise_exception(str(e))
