def check_fields_formated(obj, required_fields: list, possible_error_messages: dict):
    """
    Checa todos os atributos de um objeto e caso encontre valores nulos ou strings vazia, levanta um raise
    
    Args:
        - obj (object): Objeto que se deseja checar
        - required_fields (list): Lista com os nomes dos atributos que se deseja checar
        - possible_error_messages (dict): Dicionário com os possíveis erros que podem ocorrer. Cada chave do dicionário deve ser um atributo do objeto que será checado e caso valor da chave deve ser a respectiva mensagem de erro
        
    Example:
    
        - required_fields = ["name", "email", "phone", "password"]
        - possible_error_messages = {
                                        "name": "Nome Invalido",
                                        "email": "Email Invalido",
                                        "phone": "Telefone Invalido",
                                        "password": "Senha Invalida"
                                        }
    
    Returns:
        None
    """
    for field in required_fields:
        if not hasattr(obj, field):
            raise Exception(possible_error_messages[field])
        field_value = getattr(obj, field)
        if field_value is None or (isinstance(field_value, str) and field_value.strip() == ""):
            raise Exception(possible_error_messages[field])