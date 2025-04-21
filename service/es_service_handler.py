
import requests
from service.status_handler import StatusException
import json
import os
import socket
from datetime import datetime
import OpenSSL
import ssl


class ESServiceHandler(object):
    
    def __init__(self, logger):
        ''' Get the number of hosts from the file to generate a excel file included active spark jobs'''
        self.logger = logger
        

    async def get_es_service_ssl_api(self, es_host):
        response_dict = {}
        try:
            self.logger.info(f"es_host : {es_host}")

            es_host = es_host.replace("http://","").replace("https://","")
            source_es_hostname = str(es_host.split(':')[0])
            source_es_port = str(es_host.split(':')[1])

            cert=ssl.get_server_certificate((source_es_hostname, source_es_port))
            x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
            bytes=x509.get_notAfter()
            # print(bytes)
            timestamp = bytes.decode('utf-8')
            # print (datetime.strptime(timestamp, '%Y%m%d%H%M%S%z').date().isoformat())
            # print(datetime.strptime(timestamp, '%Y%m%d%H%M%S%z'))
            ssl_expire_date = datetime.strptime(timestamp, '%Y%m%d%H%M%S%z')
            ssl_expire_date = "{}-{}-{}".format(str(ssl_expire_date.year).zfill(2), str(ssl_expire_date.month).zfill(2), str(ssl_expire_date.day).zfill(2))
        
            response_dict.update({"ssl_certs_expire_date" : ssl_expire_date})
            response_dict.update({"ssl_certs_expire_yyyymmdd" : int(ssl_expire_date.replace("-",""))})
        
        except Exception as e:
           response_dict.update({"ssl_certs_expire_date" : 'no_ssl_certs'})
           response_dict.update({"ssl_certs_expire_yyyymmdd" : 0})
           return StatusException.raise_exception(str(e))

        finally:
            return response_dict
