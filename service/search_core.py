import os
import requests
import json
from datetime import datetime


class Search_Core:
    
    def __init__(self, logger, index_name):
        self.index_name = index_name
        self.logger = logger

    def push_data_search_engine(self, data_json):
        try:
            url = 'http://{}:4080/es/_bulk'.format(os.getenv('GRAFANA_LOKI_HOST'))
            headers = {
                    'Content-type': 'application/json',
                    'Authorization' : 'Basic {}'.format(os.getenv("BASIC_AUTH_ZINC_SEARCH")),
                    'Connection': 'close'
            }

            payload = [data_json]
            bulk_payload_lines = []
            for doc in payload:
                # Action line for indexing
                # action_line = {"index": {"_index": "alert", "_id": doc["id"]}}
                action_line = {"index": {"_index": self.index_name}}
                # bulk_payload_lines.append(json.dumps(action_line))
                bulk_payload_lines.append(json.dumps(action_line))
                doc.update({"created_date" : datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                # Source document line
                bulk_payload_lines.append(json.dumps(doc))

            self.logger.info(f"bulk_payload_lines : {json.dumps(bulk_payload_lines, indent=2)}")

            bulk_payload = "\n".join(bulk_payload_lines) + "\n"  # Add a final newline

            self.logger.info(f"bulk_payload : {json.dumps(bulk_payload, indent=2)}")
            self.logger.info(f"Uploading the alert log into local search engine : {url}")
            response = requests.post(url, data=bulk_payload, headers=headers, verify=False)
            print(response.status_code)

        except Exception as e:
            self.logger.error(e)
            pass  