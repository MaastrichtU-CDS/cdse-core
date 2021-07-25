def query_model_output_data(model_uri):
    return (
        """
PREFIX fml: <https://fairmodels.org/ontology.owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?objective_description ?objective_parameter ?output_parameter_name ?output_parameter_description ?output_code
WHERE {
    BIND (<%s> AS ?model).
	?model fml:has_objective ?model_objective.

  	?model_objective rdfs:label ?objective_description.
    ?model_objective fml:model_parameter_name ?objective_parameter.

  	?model_objective fml:based_on_parameter ?objective_based_on.
    ?objective_based_on rdfs:label ?output_parameter_description.
  	?objective_based_on fml:model_parameter_name ?output_parameter_name.
  	?objective_based_on fml:probability_of ?prob.

  	?prob fml:out_code ?output_code.
}
"""
        % model_uri
    )
