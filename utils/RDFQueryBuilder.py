import os

from SPARQLWrapper import SPARQLWrapper, JSON

HOST = os.environ.get(
    "PREDICTION_MODEL_SERVICE", "http://localhost:7200/repositories/data"
)


def query_form_string(query_string):
    sparql = SPARQLWrapper(HOST)
    sparql.setQuery(query_string)
    sparql.setReturnFormat(JSON)
    result = sparql.query().convert()
    return result["results"]["bindings"]
