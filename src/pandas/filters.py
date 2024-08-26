from datetime import datetime

from pandas import (
    DataFrame,
    Timestamp,
    to_datetime
)

def filter_rows_by_date(df: DataFrame, column_date: str ,date: str | list[str] | datetime | list[datetime]) -> DataFrame:
    """
    Filtra todas as linhas de um DataFrame com base em uma data específica ou com base em uma lista de dadas, contendo início e fim ou todas as datas passadas na lista
    
    - Args:
        - df:: DataFrame: DataFrame pandas para aplicar a filtragem de registros
        - column_date:: str: Nome da coluna que contém as datas
        - date:: str | list[str] | datetime | list[datetime]: Data ou lista de datas para filtrar
        
    - Returns:
        - DataFrame: DataFrame com as linhas filtradas
    """
    
    if isinstance(date, str):
        
        df[column_date] = to_datetime(df[column_date])
        filtered_df = df[df[column_date].dt.date == to_datetime(date).date()]
        return filtered_df
    
    if isinstance(date, datetime):
        
        date_filter = Timestamp(date)
        filtered_df = df[df[column_date].dt.date == date_filter.date()]
        return filtered_df
    
    if isinstance(date, list):
        
        if len(date) == 2:
            date_filter_start = Timestamp(date[0])
            date_filter_end = Timestamp(date[1])
            filtered_df = df[(df[column_date].dt.date >= date_filter_start.date()) & (df[column_date].dt.date <= date_filter_end.date())]
            return filtered_df
        
        if len(date) > 2:
            date_filters = [Timestamp(d) for d in date]
            filtered_df = df[df[column_date].dt.date.isin([df_date.date() for df_date in date_filters])]
            return filtered_df
        
    return df