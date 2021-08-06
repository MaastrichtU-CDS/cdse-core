import os

from SPARQLWrapper import SPARQLWrapper, JSON

from sparql.exceptions import SparqlQueryFailedException

HOST = os.environ.get(
    "PREDICTION_MODEL_SERVICE", "http://localhost:7200/repositories/model_cache"
)


def query_from_string(query_string):
    try:
        sparql = SPARQLWrapper(HOST)
        sparql.setQuery(query_string)
        sparql.setReturnFormat(JSON)
        result = sparql.query().convert()
        return result["results"]["bindings"]
    except Exception:
        raise SparqlQueryFailedException()
