class ValidationError(Exception):
    """
    A class that represents the validation error on a schema.
    
    - Args:
        - field: str: The field that has the error.
        - detail: str: The error message.
    """
    def __init__(self, field: str, detail: str):
    
        self.field = field
        self.detail = detail
        super().__init__(f"{field}: {detail}")