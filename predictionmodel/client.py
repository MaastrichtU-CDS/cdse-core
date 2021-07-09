import json
import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry


class Client:
    PREFIX = "http://"
    HOST = "http://localhost:1312/"

    def post_model_input(self):
        payload = {
            "clinical_T": "cT1",
            "clinical_N": "cN0",
        }

        try:
            session = requests.session()
            retry = Retry(total=5, backoff_factor=0.2, status_forcelist=[500])
            session.mount(self.PREFIX, HTTPAdapter(max_retries=retry))
            session.post(self.HOST, data=json.dumps(payload))
        except ConnectionError as connection_error:
            print(connection_error)

    def get_model_result(self):
        try:
            resp = requests.get(self.HOST)
            print(resp)
        except ConnectionError as connection_error:
            print(connection_error)
