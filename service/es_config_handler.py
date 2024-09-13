
import requests
from service.status_handler import StatusException
from util.es_util import json_read_config
import json
from service.redis_service import Redis_Client
import os
from dotenv import load_dotenv

load_dotenv()

class ESConfigHandler(object):
    
    def __init__(self, logger):
        ''' Get the number of hosts from the file to generate a excel file included active spark jobs'''
        self.logger = logger
        # self.hosts = hosts
        self.ALERT_VALIDATE = ["true", "false"]

    async def write_repository_file(self, data):
        try:
            with open("./repository/mail_config.json", 'w') as f:
                # json.dump(data, f)
                f.write(json.dumps(data, indent=2))
        
        except Exception as e:
           return StatusException.raise_exception(str(e))
        
    async def get_mapping_host_config(self):
        ''' get_hostname_from_domain '''
        try:
            ''' get all hots '''
            mapping_hosts = json_read_config("./repository/env_host_mapping.json")
            # self.logger.info(f"get_mapping_host_config : {hosts}")
            # print(f"get_mapping_host_config : {mapping_hosts}")
                        
            ''' get ./repositoy/mail_config.json '''
            return mapping_hosts
        
        except Exception as e:
           return StatusException.raise_exception(str(e))
    
    async def get_service_mail_config(self):
        ''' get_hostname_from_domain '''
        try:
            ''' get all hots '''
            hosts = json_read_config("./repository/mail_config.json")
            # self.logger.info(f"get_service_mail_config : {hosts}")
            # print(f"get_service_mail_config : {hosts}")
                        
            ''' get ./repositoy/mail_config.json '''
            return hosts
        
        except Exception as e:
           return StatusException.raise_exception(str(e))
        

    async def get_service_global_config(self):
        ''' get_hostname_from_domain '''
        try:
            merge_config_hosts = {}
            ''' get all hots '''
            hosts = json_read_config("./repository/config.json")
            # self.logger.info(f"get_service_global_config : {hosts}")

            merge_config_hosts = hosts.copy()
            merge_config_hosts.update(await self.get_service_host_info())
            
            ''' get ./repositoy/config.json '''
            # return hosts
            return merge_config_hosts
        
        except Exception as e:
           return StatusException.raise_exception(str(e))
        
    
    async def get_service_host_info(self):
        ''' get_hostname_from_domain '''
        try:
            ''' get all hots '''
            hosts = json_read_config("./repository/env_hosts.json")
            # self.logger.info(f"get_service_host_info : {hosts}")
            
            ''' get ./repositoy/env_hosts.json '''
            return hosts
        
        except Exception as e:
           return StatusException.raise_exception(str(e))
        

    async def set_service_mail_config(self, request_json):
        ''' Update alert value and save configuration json file direcly'''
        try:
            print(f"request_json : {request_json}")
            
            env_name = str(request_json.get("env")).lower()
            alert_bool_option = str(request_json.get("alert")).lower()
            
            print(f"env_name : {env_name}, alert_bool_option : {alert_bool_option}")

            ''' --------------- '''
            ''' Validate true/false value from the parameter'''
            ''' --------------- '''
            if alert_bool_option not in self.ALERT_VALIDATE:
                return StatusException.raise_exception(f"Please check bolean value with 'true' or 'false'")
            
            ''' --------------- '''
            ''' get host name matched env name to read their json configuraion'''
            ''' --------------- '''
            mapping_host_dict = await self.get_mapping_host_config()
            if env_name not in mapping_host_dict.keys():
                return StatusException.raise_exception(f"Please check env name")
            
            ''' --------------- '''
            ''' Update alert value on the specific env'''
            real_host_name = mapping_host_dict.get(env_name)
            ''' lookup env_name from es_configuration mail_config.json'''
            config_env = await self.get_service_mail_config()
            if real_host_name in config_env.keys():
                print("# Exists env name..")
                alert_value = True if str(alert_bool_option).lower() == "true" else False
                config_env[real_host_name]["is_mailing"] = alert_value
                ''' only update sms for Prod env's'''
                if "prod" in env_name or "dev" in env_name:
                    config_env[real_host_name]["is_sms"] = alert_value

                ''' write file with config json'''
                await self.write_repository_file(config_env)

                ''' validate if alert has changed'''
                config_env = await self.get_service_mail_config()
                ''' prod env, update all alert'''
                if "prod" in env_name or "dev" in env_name:
                    if config_env[real_host_name]["is_mailing"]  == alert_value and config_env[real_host_name]["is_sms"] == alert_value:
                        return {"message": "Updated the alert [{}] successfully.".format(str(alert_bool_option).lower())}
                    else:
                        return StatusException.raise_exception(f"{request_json.get('env')} env doesn't updated successfully.")
                else:
                    if config_env[real_host_name]["is_mailing"]  == alert_bool_option:
                        return {"message": "Updated the alert [{}] successfully.".format(str(alert_bool_option).lower())}
                    else:
                        return StatusException.raise_exception(f"{request_json.get('env')} env doesn't updated successfully.")
            else:
                return StatusException.raise_exception(f"{request_json.get('env')} env doesn't exist in configuration")
            
            ''' --------------- '''
        
        except Exception as e:
           return StatusException.raise_exception(str(e))
        


    async def set_service_alert_config(self, request_json):
        ''' Update alert value and save json file via jobs with Cache'''
        redis_client = None
        try:
            print(f"request_json : {request_json}")
            
            env_name = str(request_json.get("env")).lower()
            alert_bool_option = str(request_json.get("alert")).lower()
            
            print(f"env_name : {env_name}, alert_bool_option : {alert_bool_option}")

            ''' --------------- '''
            ''' Validate true/false value from the parameter'''
            ''' --------------- '''
            if alert_bool_option not in self.ALERT_VALIDATE:
                return StatusException.raise_exception(f"Please check bolean value with 'true' or 'false'")
            
            ''' --------------- '''
            ''' get host name matched env name to read their json configuraion'''
            ''' --------------- '''
            mapping_host_dict = await self.get_mapping_host_config()
            if env_name not in mapping_host_dict.keys():
                return StatusException.raise_exception(f"Please check env name")
            
            ''' --------------- '''
            ''' Update alert value on the specific env'''
            redis_client = Redis_Client(os.getenv('REDIS_SERVER_HOST'), self.logger)
            redis_client.Set_Connect()
            ''' update key,.value paris to Cache'''
            security_patching_json = {
                "alert" : alert_bool_option
            }
            # security_patching_json = json.dumps(payload, ensure_ascii=False).encode('utf-8')
            ''' set key value'''
            redis_client.Set_Memory_dict(env_name, security_patching_json)

            ''' check'''
            if redis_client.Get_Memory_dict(env_name):
                return {"message": "Updated the alert [{}] successfully.".format(str(alert_bool_option).lower())}
            else:
                return StatusException.raise_exception(f"{request_json.get('env')} env doesn't exist in configuration")
            ''' --------------- '''
        except Exception as e:
           self.logger.error(e)
           return StatusException.raise_exception(str(e))
        
        finally:
            if redis_client:
                redis_client.Set_Close()
        