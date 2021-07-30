def query_all_models():
    return """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX fml: <https://fairmodels.org/ontology.owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?model ?label
        WHERE {
	        ?model rdf:type fml:Model.
            ?model rdfs:label ?label.
}
"""
