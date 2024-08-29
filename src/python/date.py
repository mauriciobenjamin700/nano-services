from datetime import datetime

def str_to_date(date_str: str) -> datetime:
    """
    Converte uma string no formato 'YYYY-MM-DD' para um objeto datetime.
    
    Args:
    date_str (str): A data em formato de string.
    
    Returns:
    datetime: O objeto datetime correspondente.
    """
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as e:
        raise ValueError(f"Formato de data inválido: {date_str}. Use o formato 'YYYY-MM-DD'.") from e
