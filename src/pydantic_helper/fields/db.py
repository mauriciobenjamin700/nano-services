from pydantic import Field

from src.pydantic_helper.fields.base import base_field


def id_field(title: str = "ID", description: str = "ID", example: str = "1234567890") -> Field:
    
    return base_field(title, description, example)