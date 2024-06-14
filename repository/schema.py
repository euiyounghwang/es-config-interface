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
    

class Config_Detail(BaseModel):
    mail_list: str = "test"
    is_mailing: bool = True
    env: str

    def to_json(self):
        return {
            'mail_list' : self.mail_list,
            'is_mailing' : self.is_mailing
        }


class Search(BaseModel):
    # localhost: List[Config_Detail]
    dev: Config_Detail
    localhost: Config_Detail
            
    def to_json(self):
        return {
            'dev' : self.tsgvm00875,
            'localhost' : self.tsgvm02738
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
    

