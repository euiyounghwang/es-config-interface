import os
import requests
from dotenv import load_dotenv
import logging
import argparse
from dotenv import load_dotenv
import os
from datetime import datetime
from threading import Thread
import json
import warnings
from io import BytesIO
import pandas as pd
import datetime
import jaydebeapi, jpype
import logging
import sys
from dotenv import load_dotenv

load_dotenv()



class database:

    def __init__(self, logging, user, db_url):
        self.logger = logging
        self.user = user
        self.db_url = db_url
        self.db_conn = None
        # pass

    def set_init_JVM(self):
        '''
        Init JPYPE StartJVM
        '''

        if jpype.isJVMStarted():
            return
            
        jar = r'./h2-2.3.232.jar'
        args = '-Djava.class.path=%s' % jar

        self.logger.info('Python Version : ', sys.version)
        # print('JAVA_HOME : ', os.environ["JAVA_HOME"])
        self.logger.info('Jpype Default JVM Path : ', jpype.getDefaultJVMPath())

        # jpype.startJVM("-Djava.class.path={}".format(JDBC_Driver))
        jpype.startJVM(jpype.getDefaultJVMPath(), args, '-Xrs')
        

    def set_init_JVM_shutdown(self):
        jpype.shutdownJVM() 
   

    def set_db_connection(self):
        ''' DB Connect '''

        StartTime = datetime.datetime.now()

        # -- Init JVM
        self.set_init_JVM()
        # --

        user_account = str(self.user).split(",")
            
        # - DB Connection
        self.db_conn = jaydebeapi.connect(
            "org.h2.Driver",
            self.db_url,
            user_account,
            # "./h2-2.3.232.jar"
        )
        # --
        EndTime = datetime.datetime.now()
        Delay_Time = str((EndTime - StartTime).seconds) + '.' + str((EndTime - StartTime).microseconds).zfill(6)[:2]
        print("# DB Connection Running Time - {}".format(str(Delay_Time)))
        

    
    def set_db_disconnection(self):
        ''' DB Disconnect '''
        if self.db_conn:
            self.db_conn.close()
            # self.set_init_JVM_shutdown()
            self.logger.info("Disconnected to Oracle database successfully!") 

    
    def get_db_connection(self):
        return self.db_conn
    

    ''' export list with dict based on str type'''
    def select_oracle_query(self, sql):
        '''
        DB Oracle : Excute Query
        '''
        self.logger.info(f"excute_oracle_query : {sql}")
        # Creating a cursor object
        cursor = self.get_db_connection().cursor()

        # Executing a query
        cursor.execute(sql)
            
        # Fetching the results
        results = cursor.fetchall()
        cols = list(zip(*cursor.description))[0]
        # print(type(results), cols)

        json_rows_list = []
        for row in results:
            # print(type(row), row)
            json_rows_dict = {}
            for i, row in enumerate(list(row)):
                json_rows_dict.update({str(cols[i]) : str(row)})
            json_rows_list.append(json_rows_dict)

        cursor.close()

        # self.logger.info(json_rows_list)
        # print(json.dumps(json.loads(json_rows_list), indent=2))
            
        return json_rows_list
    
    ''' not select'''
    def excute_oracle_query(self, sql):
        '''
        DB Oracle : Excute Query
        '''
        self.logger.info(f"excute_oracle_query : {sql}")
        # Creating a cursor object
        cursor = self.get_db_connection().cursor()

        # Executing a query
        cursor.execute(sql)
        