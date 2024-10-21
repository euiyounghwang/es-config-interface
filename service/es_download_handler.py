
import json
from service.status_handler import (StatusHanlder, StatusException)
import requests
from fastapi import Response
import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")


class JobHandler(object):
    
    def __init__(self, logger):
        self.logger = logger


    async def generate_excel(self, data, _type):
        ''' service layer '''
        ''' get_download_sparkjobs '''
        try:

            self.logger.info(f"generate_excel")

            results = []

            ''' Extract Disk Usage from Prometheus Export app (9115 port)'''
            if _type == 'get_download_prometheus_disk_usage':
                for index, each_json in enumerate(data):
                    for row in each_json.values():
                        for v in row:
                            results.append([v.get("category"), v.get("host"), v.get("disktotal"),v.get("diskavail"),v.get("diskused"),v.get("diskusedpercent"),v.get("env_name"),v.get("ip"),v.get("name")])
            
                # print(results)
                ''' response df with sparkjob position that's status is N'''
                df = pd.DataFrame(
                        # [['Dev#1', "Dev spark job Dev spark job Dev spark job", "localhost", "localhost", "test_job", "Y"], ["Dev#2", "Dev spark job", "localhost", "localhost", "test_job", "N"]], 
                        results,
                        columns=["Category", "Server Name", "Disk_Total", "Disk_Avaiable", "Disk_Used", "Disk_Used_Percentage", "ENV_NAME", "IP Address", "Description"]
                    )
                
                return df

            
        except Exception as e:
           return StatusException.raise_exception(str(e)), None
        

    async def transform_prometheus_txt_to_Json(self, host, env_name, response, lookup):
            ''' transform_prometheus_txt_to_Json '''
            body_list = [body for body in response.text.split("\n") if not "#" in body and len(body)>0]
            
            prometheus_json = {}
            prometheus_json_list = []
            loop = 0
            for x in body_list:
                json_key_pairs = x.split("} ")
                key = json_key_pairs[0]
                
                ''' extract node_disk_space_metric from prometheus export app'''
                if lookup in key and lookup == 'node_disk_space_metric':
                    
                    json_key_pairs[0] = json_key_pairs[0].replace(lookup,'')
                    extract_keys = json_key_pairs[0].replace("{","").replace("}","").replace("\"","").split(",")
                    json_keys_list = {each_key.split("=")[0] : each_key.split("=")[1] for each_key in extract_keys}
                    
                    prometheus_json_list.append({
                            'category' : json_keys_list.get('category'),
                            # 'host' : host,
                            'host' : json_keys_list.get('host'),
                            'disktotal' : json_keys_list.get('disktotal'),
                            'diskavail' : json_keys_list.get('diskavail'),
                            'diskused' : json_keys_list.get('diskused'),
                            'diskusedpercent' : json_keys_list.get('diskusedpercent'),
                            'ip' : json_keys_list.get('ip'),
                            'name' : json_keys_list.get('name'),
                            'env_name' : env_name
                        }
                    )
                    loop += 1
                    
            # print(json.dumps(prometheus_json, indent=2))
            """
            {
                "0-node_disk_space_metric{category=\"Elastic": "Node\",diskavail=\"1.7gb\",disktotal=\"1.8gb\",diskused=\"1.1gb\",diskusedpercent=\"1.08%\",ip=\"0.0.0.0\",name=\"test-node-1\",server_job=\"localhost\"}",
            }
            """
            prometheus_json_list = sorted(prometheus_json_list, key=lambda k: k['name'], reverse=False)
            prometheus_json.update({host : prometheus_json_list})

            return prometheus_json
        

    async def get_download_prometheus_disk_usage(self):
        ''' get metrics from prometheus app''' 

        try:
            disk_usage_host_list = []
            host_list = str(os.getenv('PROMETHEUS_HOST')).split(",")
            # self.logger.info(f"host_list : {host_list}")
            for each_host in host_list:
                host = each_host.split(":")[1]
                env_name = each_host.split(":")[0]

                try:
                    resp = requests.get(url="http://{}:9115/metrics".format(host), timeout=5)
                                
                    if not (resp.status_code == 200):
                        ''' save failure node with a reason into saved_failure_dict'''
                        self.logger.error(f"get_metrics_from_expoter_app port do not reachable")
                        
                    self.logger.info(f"resp : {resp}")

                    ''' extract content'''
                    prometheus_json = await self.transform_prometheus_txt_to_Json(host, env_name, resp, 'node_disk_space_metric')
                    disk_usage_host_list.append(prometheus_json)
                
                except Exception as e:
                    self.logger.error(e)
                    pass

            # self.logger.info(f"disk_usage_host_list : {json.dumps(disk_usage_host_list, indent=2)}")  

            ''' get hostname from prometheus export directly after deployed Prometheus Export that has additional request(get_host_info) for this'''
            return  await self.generate_excel(disk_usage_host_list, 'get_download_prometheus_disk_usage')
        
        except Exception as e:
            self.logger.error(e)
            