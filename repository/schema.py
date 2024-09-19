from pydantic import BaseModel
from datetime import datetime
from pytz import timezone as tz
from enum import Enum
from typing import List, Union
import uuid
import sys


class Sort_Order(str, Enum):
    desc = 'DESC'
    asc = 'ASC'
    


class Alert(BaseModel):
    env: str = "prod1"
    alert: str = "false"
    message: str = 'Security Patching'
        
    def to_json(self):
        return {
            'env' : str(self.env).lower(),
            'alert' : str(self.alert).lower(),
            'message' : str(self.message)
        }
            
    '''
    def to_json(self): 
        return  {
            "localhost": {
                "mail_list": "test@x.com",
                "env" : "Dev",
                "is_mailing": True
            },
            "dev": {
                "mail_list": "test@y.com",
                "env": "Localhost",
                "is_mailing": True
            }
        }
    '''
    

class Log(BaseModel):
    env: str = "prod1"
    host_name: str = "localhost"
    status: str = "ES_RESTARTED"
    message: str = 'TEST MESSAGE'
        
    def to_json(self):
        return {
            'env' : str(self.env).lower(),
            'host_name' : str(self.host_name).lower(),
            'status' : str(self.status).upper(),
            'message' : str(self.message)
        }