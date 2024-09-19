from fastapi import APIRouter
import json
import datetime
from injector import logger, JobHandlerInject
from service.status_handler import (StatusHanlder, StatusException)
# from typing import Optional
import datetime
from repository.schema import Alert
from fastapi.responses import StreamingResponse
import datetime
from io import BytesIO
import xlsxwriter
import pandas as pd


app = APIRouter(
    prefix="/download",
)



@app.get("/generate_excel_disk_usage", description="Sample Payload : http://localhost:8003/download/generate_excel_disk_usage", summary="download_excel_disk_usage")
async def generate_excel_prometheus_disk_usage():
    ''' Search to sparkjob in all envs '''
    StartTime, EndTime, Delay_Time = 0, 0, 0
    
    try:
        StartTime = datetime.datetime.now()
        
        logger.info("generate_excel_prometheus_disk_usage")

        ''' response df with sparkjob position that's status is N'''
        df = await JobHandlerInject.get_download_prometheus_disk_usage()
        
        '''
        return df from service layer 
        df = pd.DataFrame(
                [["Canada", 10], ["USA", 20]], 
                columns=["team", "points"]
        )
        '''

        '''
        # -- csv
        https://xlsxwriter.readthedocs.io/working_with_pandas.html
        return StreamingResponse(
                iter([df.to_csv(index=False)]),
                media_type="text/csv",
                headers={"Content-Disposition": f"attachment; filename=ES_SPARK_JOBS_{datetime.datetime.now().strftime('%Y%m%d')}.csv"}
                # headers={"Content-Disposition": f"attachment; filename=data.csv"}
        )
        '''
        # - getnerate excel file
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            sheet_name = str(datetime.datetime.today().strftime('%Y-%m-%d'))
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            workbook  = writer.book
            worksheet = writer.sheets[sheet_name]

            # df.to_excel(writer, sheet_name='Sheet1', index=False)
            # workbook  = writer.book
            # worksheet = writer.sheets['Sheet1']


            header_format = workbook.add_format( # !!! here workable, no error
                {
                    'bold': True,
                    'text_wrap': True,
                    'valign': 'top',
                    'valign': 'center',
                    # 'fg_color': '#D7E4BC',
                    # 'bg_color': '#edbd93',
                    'bg_color': 'yellow',
                    'border': 1
                }
            )

            # column_settings = [{'header': column} for column in df.columns]
            (max_row, max_col) = df.shape

            # worksheet.add_table(0, 0, max_row, max_col - 1, {'columns': column_settings})
            frm2 = workbook.add_format({'bold': True,'bg_color': 'yellow',})

            # Write the column headers with the defined format.
            for col_num, value in enumerate(df.columns.values):
                # print(col_num, value)
                worksheet.write(0, col_num, value, header_format)
                worksheet.set_column(0, col_num, 15)
                worksheet.autofilter(0, 0, max_row, max_col - 1)
                worksheet.autofit()
                col_num += 1
                # worksheet.set_column('A:A',None,frm2)  

        
            EndTime = datetime.datetime.now()
            Delay_Time = str((EndTime - StartTime).seconds) + '.' + str((EndTime - StartTime).microseconds).zfill(6)[:2]

            logger.info('Metrics : {}'.format(Delay_Time))
      
        return StreamingResponse(
            BytesIO(buffer.getvalue()),
            media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            headers={"Content-Disposition": f"attachment; filename=DISK-USAGE-PROD-{datetime.datetime.now().strftime('%Y%m%d')}.xlsx"}
        )
        
    except Exception as e:
        logger.error(e)
        return StatusException.raise_exception(e)
    
