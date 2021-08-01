def query_model_input_data(model_uri):
    return (
        """
PREFIX fml: <https://fairmodels.org/ontology.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
SELECT DISTINCT ?input_type_parent ?input_type_child ?code_parent ?code_child ?model_input_parameter ?parent_input_parameter
WHERE {
    BIND (<%s> AS ?model).
    ?model fml:contains_algorithm ?algo.
	?algo fml:has_input_parameter ?input_parameters.
  	?input_parameters fml:has_translation ?translated_input.
  	?translated_input fml:target_value ?model_input_parameter.
  	?translated_input fml:source_object ?source_obj.
  	?source_obj fml:thesaurus_code ?code_child.
  	?source_obj fml:thesaurus_type ?input_type_child.
    ?input_parameters fml:model_parameter_name ?parent_input_parameter.
  	?input_parameters fml:based_on_information_element ?parent_node.
  	?parent_node fml:thesaurus_code ?code_parent.
    ?parent_node fml:thesaurus_type ?input_type_parent.
}
"""
        % model_uri
    )
