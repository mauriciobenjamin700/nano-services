from pydantic import Field

def base_field(title: str, description: str, example: str) -> Field:
    
    return Field(
        None,
        title=title,
        description=description,
        examples=[example],
        validate_default=True
    )