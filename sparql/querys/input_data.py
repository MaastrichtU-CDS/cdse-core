def query_model_input_data(model_uri):
    return (
        """
PREFIX fml: <https://fairmodels.org/ontology.owl#>
SELECT DISTINCT ?ncit_parent ?ncit_child ?model_input_parameter ?parent_input_parameter
WHERE {
    BIND (<%s> AS ?model).
	?model fml:has_input_parameter ?input_parameters.
  	?input_parameters fml:has_translation ?translated_input.
  	?translated_input fml:target_value ?model_input_parameter.
  	?translated_input fml:source_object ?source_obj.
  	?source_obj fml:ncit_code ?ncit_child.

  	?input_parameters fml:model_parameter_name ?parent_input_parameter.

  	?input_parameters fml:based_on_information_element ?parent_node.
  	?parent_node fml:ncit_code ?ncit_parent.
}
"""
        % model_uri
    )
