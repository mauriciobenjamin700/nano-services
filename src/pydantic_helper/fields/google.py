
from pydantic import Field

from src.pydantic_helper.fields.base import base_field


def google_id_field(title: str = "Google ID", description: str = "Google ID", example: str = "google_id") -> Field:
    
    return base_field(title, description, example)