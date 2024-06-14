from config.log_config import create_log
from dotenv import load_dotenv
# import yaml
import json
import os
from service.es_config_handler import ESConfigHandler

load_dotenv()
    
# Initialize & Inject with only one instance
logger = create_log()


# read host file to make an dict in memory
def read_host_domain(server_file):
    sparkjob_list = []
    with open(server_file) as data_file:
        for line in data_file:
            if '#' in line:
                continue
            line = line.strip().split("|")
            # print(f"{line}")
            sparkjob_list.append(line)
    return sparkjob_list


''' get all hots '''
hosts = read_host_domain("./repository/hosts")
''' hosts = ['localhost', 'dev',...] '''
logger.info(list(hosts))
# es_hosts_enum_list =list(hosts.keys())

ESConfigHandlerInject = ESConfigHandler(logger, hosts)