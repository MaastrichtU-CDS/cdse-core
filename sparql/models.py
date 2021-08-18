class ModelData:
    def __init__(
        self,
        fhir_code,
        fhir_code_system,
        parameter,
        description,
        children,
        matched_child,
    ):
        self.fhir_code = fhir_code
        self.fhir_code_system = fhir_code_system
        self.parameter = parameter
        self.description = description
        self.children = children
        self.matched_child = matched_child

    def get_child_by_code(self, child_code):
        for child in self.children:
            if child.fhir_code == child_code:
                return child
