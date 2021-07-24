import os

import requests

HOST = os.environ.get("PREDICTION_MODEL_SERVICE", "http://localhost:3000/")


class PredictionModelClient:
    @staticmethod
    def get_model_list():
        resp = requests.get(HOST)
        return resp.json()


