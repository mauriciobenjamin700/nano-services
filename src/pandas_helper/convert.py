from pandas import DataFrame

def models_to_df(data: list[object]) -> DataFrame:
    """
    Recebe uma lista de objetos e retorna um DataFrame com os dados de cada objeto.
    
    - Args:
        - data:: list: Lista de objetos, onde os atributos dos objetos serão as colunas do dataframe. (Todos os Objetos devem ser da mesma classe)
        
    - Returns:
        - DataFrame: Um DataFrame com os dados dos objetos.
    """
    df =  DataFrame([model.__dict__ for model in data])
    
    try:
        df.drop(columns=["_sa_instance_state"],inplace=True)
    except KeyError:
        pass  # Se a coluna _sa_instance_state não existir, não há problema.
    
    return df