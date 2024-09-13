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
        
    def to_json(self):
        return {
            'env' : str(self.env).lower(),
            'alert' : str(self.alert).lower()
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
    

