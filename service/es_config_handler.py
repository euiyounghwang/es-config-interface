
import requests
from service.status_handler import StatusException

class ESConfigHandler(object):
    
    def __init__(self, logger, hosts):
        ''' Get the number of hosts from the file to generate a excel file included active spark jobs'''
        self.logger = logger
        self.hosts = hosts

    async def get_hostname_from_domain(self):
        ''' get_hostname_from_domain '''
        try:

            # self.logger.info(f"get_hostname_from_domain : {spark_url}")
            #  # -- make a call to master node to get the information of activeapps
            # resp = requests.get(url=spark_url, timeout=5)
            
            # if not (resp.status_code == 200):
            #     return None
            
            # # logging.info(f"activeapps - {resp}, {resp.json()}")
            # resp_working_job = resp.json().get("activeapps", "")
            # # response_activeapps = []
            # if resp_working_job:
            #     self.logger.info(f"activeapps - {resp_working_job}")
            #     return resp_working_job
            # return None
            return {}
        
        except Exception as e:
           return StatusException.raise_exception(str(e))
