
import requests
from service.status_handler import StatusException
import json
import os
import socket
import OpenSSL
import ssl

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pytz
import datetime


class ESServiceHandler(object):
    
    def __init__(self, logger):
        ''' Get the number of hosts from the file to generate a excel file included active spark jobs'''
        self.logger = logger
        self.gloabal_default_timezone = pytz.timezone('US/Eastern')
        

    async def get_es_service_ssl_api(self, es_host):
        response_dict = {}
        try:
            # self.logger.info(f"es_host : {es_host}")

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
            ssl_expire_date = datetime.datetime.strptime(timestamp, '%Y%m%d%H%M%S%z')
            ssl_expire_date = "{}-{}-{}".format(str(ssl_expire_date.year).zfill(2), str(ssl_expire_date.month).zfill(2), str(ssl_expire_date.day).zfill(2))
        
            response_dict.update({"ssl_certs_expire_date" : ssl_expire_date})
            response_dict.update({"ssl_certs_expire_yyyymmdd" : int(ssl_expire_date.replace("-",""))})
        
        except Exception as e:
        #    self.logger.error(e)
           response_dict.update({"ssl_certs_expire_date" : 'no_ssl_certs'})
           response_dict.update({"ssl_certs_expire_yyyymmdd" : 0})
           return StatusException.raise_exception(str(e))

        finally:
            return response_dict


    async def get_push_alert_act(self, request_json):
        ''' Push alert via email using this endpoint service'''
        def cleanText(readData):
            text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\[\]\(\)\<\>`\'…》]', '', readData)
            return text
    
        def html_color(status):
            ''' https://www.figma.com/colors/chili-red/ '''
            if status == "" or status is None:
                _color = '#008000'
            if status.lower() == 'yellow':
                _color = 'orange'
            elif status.lower() == 'red':
                _color = 'red'
            else:
                _color = '#008000'
            return "<font color='{}'>{}</font>".format(_color, status) 
        

        def mail_attached(env, subject, to, cc, message, _type):
            user_list = to.split(",")
            self.logger.info(f"user_list : {user_list}")
            
            ''' using smtp'''
            me = os.environ["MAIL_SENDER"]
            you = user_list

            msg = MIMEMultipart('alternative')
            msg['Subject'] = '[{}] {}'.format(str(env).upper(), subject)
            msg['From'] = me
            msg['To'] = ','.join(you)
            msg['Cc'] = cc
            
            alert_date = datetime.datetime.now(tz=self.gloabal_default_timezone).strftime('%Y-%m-%d %H:%M:%S')

            if _type == "mail":
                body = """
                    - Alert Date : %s <BR/> \
                    - Enviroment: <b>%s</b><BR/>\
                    - <b>Alert Message : </b><BR/>%s \
                    """ % ( alert_date, 
                            str(env).upper(),
                            message
                          )
            
            elif _type == "sms":
                self.logger("sms")

            html = """
                <h4>Monitoring [ES Team Dashboard on export application]</h4>
                <HTML><head>
                <body>
                %s
                </body></HTML>
                """ % (body)

            part2 = MIMEText(html, 'html')
            msg.attach(part2)

            # print msg
            s = smtplib.SMTP(os.getenv("SMTP_HOST"), os.getenv("SMTP_PORT"))

            if not you:
                you = []

            if not cc:
                cc = []
            else:
                cc = [cc]
            
            recipients_list = you + cc
            s.sendmail(me, recipients_list, msg.as_string())
            s.quit()

        response_dict = {}

        try:
            self.logger.info(f"[service] get_push_alert_act - request_json : {request_json}")
            self.logger.info(f"html_color : {html_color('green')}")
            self.logger.info(f"os.getenv : {os.getenv('SMTP_HOST')}")
            self.logger.info(f"os.getenv : {os.getenv('SMTP_PORT')}")

            ''' send alert '''
            mail_attached(request_json.get("env"), request_json.get("subject"), request_json.get("to_user"), request_json.get("cc_user"), request_json.get("message"), _type="mail")

            ''' response '''
            response_dict = {
                 "status" : 200,
                 "message" : "Sent an email alert successfully.."
             }
            
        except Exception as e:
           self.logger.error(e)
           return StatusException.raise_exception(str(e))

        finally:
            return response_dict
