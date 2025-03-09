from pydantic import Field


from src.pydantic_helper.fields.base import base_field


def email_field(title: str = "E-mail", description: str = "E-mail", example: str = "email@gmail.com") -> Field:
    
    return base_field(title, description, example)

def message_field(title: str = "Mensagem", description: str = "Mensagem", example: str = "Mensagem") -> Field:
    
    return base_field(title, description, example)

def name_field(title: str = "Nome", description: str = "Nome", example: str = "Jose") -> Field:
    
    return base_field(title, description, example)

def password_field(title: str = "Senha", description: str = "Senha", example: str = "password1234") -> Field:
    
    return base_field(title, description, example)

def phone_field(title: str = "Telefone", description: str = "Telefone", example: str = "(11) 99999-9999") -> Field:
    
    return base_field(title, description, example)

def value_field(title: str = "Valor", description: str = "Valor", example: float = 100.00) -> Field:
    
    return base_field(title, description, example)

    