from datetime import datetime
from fastapi import HTTPException
from re import (
    match,
    sub
)


def validate_cpf_cnpj(string:str) -> dict[str, str]:
    """
    Valida um CPF ou CNPJ
    
    - Args:
        - string:: str: String que será validada para ser, CPF ou CNPJ
        
    - Return:
        - dict[str, str]: Dicionário com a informação sobre o tipo de identidade (CPF ou CNPJ) e o número da identidade
            - chaves: 
                - identity, 
                - number
        - HTTPException: Caso o tamanho da string seja inválido para ser um CPF ou CNPJ
    
    """
    # TODO: Implementar validação do CPF
    identity = "".join([number for number in string if number.isnumeric()])
    print(identity)
    print("Tamanho: ",len(identity))
    
    if len(identity) == 11: #Caso seja um CPF
        return {"identity": "CPF", "number": identity}
    
    elif len(identity) == 14:
        return {"identity": "CNPJ", "number": identity}
    
    raise HTTPException(400,"CPF/CNPJ inválido")

def validate_email(email:str) -> None:
    """
    Valida um email
    
    - Args:
        - email:: str: Email que será validado
        
    - Return:
        - None
    
    - Raises:    
        - HTTPException: 400 - E-mail invalido
    
    """
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not match(email_regex, email):
        raise HTTPException(400, "Email inválido")

def validate_date(date:str) -> str:
    """
    Valida uma data no formato YYYY-MM-DD
    
    - Args:
        - date:: str: Data que será validada
        
    - Return:
        - str: Data formatada
    
    - Raises:    
        - HTTPException: 400 - Data invalida
    
    """
    
    if type(date) != str:
        raise HTTPException(400, "Tipo de data inválida")

    # Definindo o formato esperado de data (YYYY-MM-DD)
    date_format = r'\d{4}-\d{2}-\d{2}'
    
    # Verificando se a data fornecida corresponde ao formato esperado
    if match(date_format, date):
        # Convertendo a data para um objeto datetime
        parsed_date = datetime.strptime(date, '%Y-%m-%d')
        # Verificando se a data de nascimento é no passado
        if parsed_date >= datetime.now():
            raise HTTPException(400,'A data de nascimento não pode estar no futuro')
        if datetime.now().year - parsed_date.year < 18:
            raise HTTPException(400,'O usuário deve ser maior de idade')
    else:
        raise HTTPException(400,'Formato de data inválido. Use o formato YYYY-MM-DD')
    
def validate_phone_number(phone_number: str) -> str:
    """
    Remove todos os caracteres especiais de um número de telefone e valida o formato.
    
    - Args:
        - phone_number: str: Número de telefone que será limpo e validado
        
    - Return:
        - str: Número de telefone contendo apenas dígitos e no formato correto
    
    - Raises:    
        - HTTPException: 400 - Número de telefone inválido
    """
    
    # Removendo todos os caracteres que não são dígitos
    cleaned_number = sub(r'\D', '', phone_number)
    
    # Definindo o formato esperado de número de telefone brasileiro com DDD e dígito 9
    phone_regex = r'^\d{2}9\d{8}$'
    
    # Verificando se o número de telefone limpo corresponde ao formato esperado
    if not match(phone_regex, cleaned_number):
        raise HTTPException(400, 'Número de telefone inválido. Deve conter 11 dígitos no formato correto (XX9XXXXXXXX)')
    
    return cleaned_number

def validate_house_number(house_number: str) -> str:
    """
    Valida o número da casa levando em conta as seguintes possíbilidades
    - Números Inteiros: Exemplo: 123
    - Números com Letras: Exemplo: 123A, 123B
    - Números com Barras: Exemplo: 123/1, 123/2
    - Números com Hífen: Exemplo: 123-1, 123-2
    - Casos Especiais: Como "S/N" (sem número)
    
    - Args:
        - house_number: str: Número da casa que será validado
        
    - Return:
        - str: Número da casa validado
    
    - Raises:    
        - HTTPException: 400 - Número da casa inválido
    """
    
    # Definindo o formato esperado de número de casa
    house_number_regex = r'^\d+[A-Za-z]?(/?\d+)?(-?\d+)?$|^S/N$'
    
    # Verificando se o número da casa fornecido corresponde ao formato esperado
    if not match(house_number_regex, house_number):
        raise HTTPException(400, 'Número da casa inválido. Deve ser um número válido ou (S/N)')
    
    return house_number
