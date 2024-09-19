from config.log_config import create_log
from dotenv import load_dotenv
# import yaml
import json
import os
from service.es_config_handler import ESConfigHandler
from service.es_download_handler import JobHandler
from service.es_log_handler import ESLogConfigHandler

load_dotenv()
    
# Initialize & Inject with only one instance
logger = create_log()


# read host file to make an dict in memory
def read_config_json(path):
    with open(path, "r") as read_file:
        data = json.load(read_file)
        return data

"""
''' get all hots '''
hosts = read_config_json("./repository/config.json")
''' hosts = ['localhost', 'dev',...] '''
logger.info(list(hosts))
# es_hosts_enum_list =list(hosts.keys())
"""

ESConfigHandlerInject = ESConfigHandler(logger)
JobHandlerInject = JobHandler(logger)
ESLogHandlerInject = ESLogConfigHandler(logger)