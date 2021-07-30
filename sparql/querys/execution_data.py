def query_model_execution_data(model_uri):
    return (
        """
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX fml: <https://fairmodels.org/ontology.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?model_label ?exec_type ?image_name ?image_id ?host_env ?fhir_version
WHERE {
    BIND (<%s> AS ?model).
	?model rdfs:label ?model_label.
  	?model fml:contains_algorithm ?algo.

  	?algo fml:fhir_version ?fhir_version.

  	?algo fml:has_execution_type ?exec.
  	?exec rdf:type ?exec_type.

  	?exec fml:docker_image_name ?image_name.
  	?exec fml:docker_image_id ?image_id.
  	?exec fml:docker_host_env ?host_env.
}
"""
        % model_uri
    )
