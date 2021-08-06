def query_model_input_data(model_uri):
    return (
        """
PREFIX fml: <https://fairmodels.org/ontology.owl#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX ncit: <http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?fhir_code_system_parent ?fhir_code_system_child ?fhir_code_parent ?fhir_code_child ?child_parameter ?parent_parameter
WHERE {
    BIND (<%s> AS ?model).
?model fml:contains_algorithm ?algo.
?algo fml:has_input_parameter ?input_parameters.
?input_parameters fml:has_translation ?translated_input.
?translated_input fml:target_value ?child_parameter.
?translated_input fml:source_object ?source_obj.

?input_parameters fml:model_parameter_name ?parent_parameter.
?input_parameters fml:based_on_information_element ?parent_node.

?parent_node rdf:type ?parent_node_type.
FILTER(?parent_node_type != fml:InformationElement).
OPTIONAL{?parent_node_type rdfs:label ?o}.
BIND( REPLACE(STR(?parent_node_type), "#.*$", "") AS ?fhir_code_system_parent).
BIND( REPLACE(STR(?parent_node_type), "^.*#", "") AS ?fhir_code_parent).

    
?source_obj rdf:type ?child_node_type.
FILTER(?child_node_type != fml:InformationElement).
OPTIONAL{?child_node_type rdfs:label ?o}.
BIND( REPLACE(STR(?child_node_type), "#.*$", "") AS ?fhir_code_system_child).
BIND( REPLACE(STR(?child_node_type), "^.*#", "") AS ?fhir_code_child).
}
"""
        % model_uri
    )
