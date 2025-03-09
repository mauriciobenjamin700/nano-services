from datetime import datetime, date
from typing import Union

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

def br_date_to_american_date(date: str) -> str:
    """
    Converte uma data em Formato PT-BR (ex: 15/04/2030) para o Formato que o Banco de Dados aceita (ex: 2030-04-15).
    
    Caso A string seja invalida, retornará uma string vazia ("")
    
    Args:
        date:: str: Data PT-BR que será convertida para o Banco de Dados
        
    Return
        bd_date:: str: Data Formatada para o Portgrees poder Salvar
    """
    
    bd_date = ""
    
    if(len(date.strip())) == 10:
        bd_date = datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')

    return bd_date

def american_date_to_br_date(date_input: Union[str, datetime, date], with_time: bool = False) -> str:
    """
    Converte uma data no formato do banco de dados (YYYY-MM-DD) para o formato PT-BR (DD/MM/YYYY).
    
    Args:
        date_input (Union[str, datetime, date]): Data que será convertida.
        
    Returns:
        str: Data convertida para o formato PT-BR. Retorna uma string vazia se a conversão falhar.
    """
    
    br_date = ""
    
    try:
        if not with_time:
            
            if isinstance(date_input, str):
                
                if len(date_input.strip()) == 10:
                    br_date = datetime.strptime(date_input, '%Y-%m-%d').strftime('%d/%m/%Y')

            elif isinstance(date_input, datetime):
                br_date = date_input.strftime('%d/%m/%Y')

            elif isinstance(date_input, date):
                br_date = date_input.strftime('%d/%m/%Y')
                
            return br_date
        
        if with_time:
            
            if isinstance(date_input, str):
                
                if len(date_input.strip()) == 19:
                    br_date = datetime.strptime(date_input, '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M')

            elif isinstance(date_input, datetime):
                br_date = date_input.strftime('%d/%m/%Y %H:%M')

            elif isinstance(date_input, date):
                br_date = date_input.strftime('%d/%m/%Y %H:%M')
                
            return br_date
        
    except TypeError:
        raise TypeError("Argumento inválido. Deve ser uma data no formato YYYY-MM-DD ou datetime.")
            
            
    except ValueError as e:
        raise ValueError(f"Erro na conversão: {e}")
        
    except Exception as e:
        raise Exception(f"Erro inesperado: {e}")

    

def date_list_to_format_date_list(date_list: list[str] | list[datetime]) -> list[str]:
    """
    Converte uma lista de datas em um novo formato, como por exemplo, YYYY-MM-DD, para uma lista de datas no formato DD/MM/YYYY.
    
    Args:
        date_list (list[str] | list[datetime]): Lista de datas que será convertida.
        
    Returns:
        list[str]: Lista de datas convertidas para o formato DD/MM/YYYY.
    """
    
    return [american_date_to_br_date(date) for date in date_list]


def map_weekday_to_pt(weekday: str) -> str:
    """
    Converte um dia da semana em inglês para português.
    
    - Args:
        - weekday:: str: Dia da semana em inglês (
            'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
        )
        
    - Returns:
        - str: Dia da semana em português (
            - 'Monday' -> 'Segunda',
            - 'Tuesday' -> 'Terça',
            - 'Wednesday' -> 'Quarta',
            - 'Thursday' -> 'Quinta',
            - 'Friday' -> 'Sexta',
            - 'Saturday' -> 'Sábado',
            - 'Sunday' -> 'Domingo'
        )
    """
    mapping = {
        'Monday': 'Segunda',
        'Tuesday': 'Terça',
        'Wednesday': 'Quarta',
        'Thursday': 'Quinta',
        'Friday': 'Sexta',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }
    return mapping.get(weekday, weekday)

def map_month_to_pt(month: str) -> str:
    """
    Mapeia um mês no formato númerico para o nome do mês em português.
    
    - Args:
        - month:: str: Mês no formato númerico ('01', '02', '03', ..., '12')
        
    - Returns:
        - str: Mês em português ('Janeiro', 'Fevereiro',..., 'Dezembro')
    """
    mapping = {
        '01': 'Janeiro',
        '02': 'Fevereiro',
        '03': 'Março',
        '04': 'Abril',
        '05': 'Maio',
        '06': 'Junho',
        '07': 'Julho',
        '08': 'Agosto',
        '09': 'Setembro',
        '10': 'Outubro',
        '11': 'Novembro',
        '12': 'Dezembro'
    }
    #year, month_num = month.split('-')
    #return f"{mapping.get(month_num, month_num)} de {year}"
    return mapping.get(month, month)

def calc_days(
    start_date: datetime, 
    end_date: datetime
) -> int:
    """
    Dado duas datas, calcula o tempo em dias com base no intervalo de tempo
    
    - Args:
        - start_date:: datetime : Data inicial (Mais Recente)
        - end_date:: datetime : Data final (Menos Recente)
    
    - Returns:
        - int: Dias entre as duas datas
    """
    
    result = start_date - end_date
    return result.days

def calc_mean(
    value: float,
    date: datetime | list[datetime]):
    """
    Calcula o valor médio em dias de um montante, dado o intervalo de tempo passado
    
    - Args:
      - value:: float : Montante a ser dividido
      - date:: datetime | list[datetime] : Data Específica | Data mais recente e Data menos recente |  intervalo Fechado de tempo para análisar as vendas
    """
    if isinstance(date, list):
    
        if len(date) == 2:
            
            value =  value / calc_days(date[0], date[1])
        
        elif len(date) > 2:
            value =  value / len(date)
            
    return value