from datetime import datetime
from pandas import(
    Categorical,
    DataFrame,
    Timestamp,
    merge,
    to_datetime   
)


def filter_rows_by_date(
    df: DataFrame, 
    column_date: str,
    date: str | list[str] | datetime | list[datetime]
) -> DataFrame:
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

def top_selling_product(
    df: DataFrame, 
    product_col: str, 
    quantity_col: str, 
    limit: int = 5, 
    ascending: bool = False
) -> tuple[list, list]:
    """
    Dado um DataFrame de vendas, analisa quais são os produtos mais vendidos e retorna os mais vendidos e suas respectivas quantidades de venda.
    
    - Args:
        - df: DataFrame contendo os dados de vendas
        - product_col: Nome da coluna que contém os nomes dos produtos
        - quantity_col: Nome da coluna que contém as quantidades vendidas
        - limit: Quantidade de produtos mais vendidos a serem retornados (default: 5)
        - ascending: True se for em ordem crescente e False em ordem decrescente
        
    - Returns:
        - tuple:
            - products: Lista com os nomes dos produtos mais vendidos
            - quantities: Lista com as respectivas quantidades de venda dos produtos mais vendidos
    """
    if limit < 0:
        raise ValueError("Limite deve ser um valor inteiro positivo")
    
    most_sold_products = df.groupby(product_col)[quantity_col].sum().reset_index()
    most_sold_products = most_sold_products.sort_values(by=quantity_col, ascending=ascending).head(limit)
    
    products = most_sold_products[product_col]
    quantities = most_sold_products[quantity_col]
    
    return (products.to_list(), quantities.to_list())

def top_profitable_product(
    products_df: DataFrame, 
    sales_df: DataFrame, 
    product_col: str, 
    price_sale_col: str, 
    price_cost_col: str, 
    quantity_col: str, 
    limit: int = 5, 
    ascending: bool = False
) -> tuple[list, list]:
    """
    Retorna os produtos mais lucrativos e seu lucro gerado.
    
    - Args:
        - products_df: DataFrame contendo os dados dos produtos
        - sales_df: DataFrame contendo os dados das vendas
        - product_col: Nome da coluna que contém os nomes dos produtos
        - price_sale_col: Nome da coluna que contém os preços de venda
        - price_cost_col: Nome da coluna que contém os preços de custo
        - quantity_col: Nome da coluna que contém as quantidades vendidas
        - limit: Quantidade de produtos mais lucrativos a serem retornados (default: 5)
        - ascending: True se for em ordem crescente e False em ordem decrescente
        
    - Returns:
        - tuple:
            - product: Lista com o nome dos produtos mais lucrativos
            - profit: Lista com o lucro gerado pelos produtos mais lucrativos
    """
    if limit < 0:
        raise ValueError("Limite deve ser um valor inteiro positivo")
    
    products_df["profit_per_unit"] = products_df[price_sale_col] - products_df[price_cost_col]
    
    product_sales = sales_df.groupby(product_col)[quantity_col].sum().reset_index()
    
    merged_df = merge(product_sales, products_df, left_on=product_col, right_on=product_col)
    
    merged_df["total_profit"] = merged_df["profit_per_unit"] * merged_df[quantity_col]
    
    merged_df = merged_df[[product_col, "total_profit"]].sort_values(by="total_profit", ascending=ascending).head(limit)
    
    product = merged_df[product_col].to_list()
    profit = merged_df["total_profit"].apply(lambda x: round(x, 2)).tolist()
    
    return (product, profit)

def expenditure(
    df: DataFrame, 
    value_col: str, 
    quantity_col: str, 
    date_col: str, 
    date: datetime | list[datetime] | None = None
) -> float:
    """
    Calcula todas as despesas feitas ao adquirir novos ingredientes ao estoque
    
    - Args:
      - df: DataFrame contendo os dados de compras
      - value_col: Nome da coluna que contém os valores dos ingredientes
      - quantity_col: Nome da coluna que contém as quantidades dos ingredientes
      - date_col: Nome da coluna que contém as datas de registro
      - date: Data Específica ou intervalo Fechado de tempo para análisar as vendas
        
    - Returns:
      - float: valor gasto em despesas geradas ao obter ingredientes 
    """
    df['total_value'] = df[value_col] * df[quantity_col]
    
    if date is None:
        value = df["total_value"].sum()
    else:
        filtered_df = filter_rows_by_date(df, date_col, date)
        value = filtered_df["total_value"].sum()
        
    return round(float(value), 2)

def total_revenue(
    df: DataFrame, 
    total_value_col: str, 
    date_col: str, 
    date: datetime | list[datetime] | None = None
) -> float:
    """
    Calcula a receita total que entrou no caixa

    - Args:
      - df: DataFrame contendo os dados de vendas
      - total_value_col: Nome da coluna que contém os valores totais das vendas
      - date_col: Nome da coluna que contém as datas de venda
      - date: Data Específica ou intervalo Fechado de tempo para análisar as vendas
        
    - Returns:
      - float: Valor total que entrou em caixa, desconsiderando gastos com obtenção de ingredientes
    """
    if date is None:
        value = df[total_value_col].sum()
    else:
        filtered_df = filter_rows_by_date(df, date_col, date)
        value = filtered_df[total_value_col].sum()
        
    return round(float(value), 2)

def profit(
    sales_df: DataFrame, 
    purchases_df, 
    sales_total_value_col: str, 
    purchases_value_col: str, 
    purchases_quantity_col: str, 
    sales_date_col: str, 
    purchases_date_col: str, 
    date: datetime | list[datetime] | None = None
) -> float:
    """
    Calcula o lucro obtido da venda de produtos
    
    - Args:
      - sales_df: DataFrame contendo os dados de vendas
      - purchases_df: DataFrame contendo os dados de compras
      - sales_total_value_col: Nome da coluna que contém os valores totais das vendas
      - purchases_value_col: Nome da coluna que contém os valores dos ingredientes
      - purchases_quantity_col: Nome da coluna que contém as quantidades dos ingredientes
      - sales_date_col: Nome da coluna que contém as datas de venda
      - purchases_date_col: Nome da coluna que contém as datas de registro
      - date: Data Específica ou intervalo Fechado de tempo para análisar as vendas
        
    - Returns:
      - float: Lucro obtido da venda
    """
    return round(
        total_revenue(
            sales_df, 
            sales_total_value_col, 
            sales_date_col, date
            ) 
        - expenditure(
            purchases_df, 
            purchases_value_col, 
            purchases_quantity_col, 
            purchases_date_col, 
            date),
        2)


def sales_per_day(df, total_value_col: str, date_col: str, id_col: str, date: datetime | list[datetime] | None = None) -> tuple[list[str], list[float], list[int]]:
    """
    Calcula a quantidade de vendas por dia, dado um intervalo de tempo
    
    - Args:
      - df: DataFrame contendo os dados de vendas
      - total_value_col: Nome da coluna que contém os valores totais das vendas
      - date_col: Nome da coluna que contém as datas de venda
      - id_col: Nome da coluna que contém os IDs das vendas
      - date: Data Específica ou intervalo Fechado de tempo para análisar as vendas
        
    - Returns:
      - tuple: 
        - dates: list[date]: Datas que ocorreram vendas
        - total_values: list[float]: Valor total das Vendas
        - total_sales: list[int]: Total de Vendas
    """
    df_filtered = filter_rows_by_date(df, date_col, date)
    
    df_filtered['sale_date'] = df_filtered[date_col].dt.date
    
    grouped_df = df_filtered.groupby('sale_date').agg({total_value_col: 'sum', id_col: 'count'}).reset_index()
    
    dates = grouped_df['sale_date'].tolist()
    
    total_values = grouped_df[total_value_col].tolist()
    
    total_sales = grouped_df[id_col].apply(lambda x: int(x)).tolist()
    
    return dates, total_values, total_sales

def sales_per_hour(df, total_value_col: str, date_col: str, id_col: str, date: datetime | list[datetime] | None = None) -> tuple[list[str], list[float], list[int]]:
    """
    Calcula a quantidade de vendas por hora, dado um intervalo de tempo
    
    - Args:
      - df::Dataframe: DataFrame contendo os dados de vendas
      - total_value_col::str: Nome da coluna que contém os valores totais das vendas
      - date_col::str: Nome da coluna que contém as datas de venda
      - id_col::str: Nome da coluna que contém os IDs das vendas
      - date::str: Data Específica ou intervalo Fechado de tempo para análisar as vendas
        
    - Returns:
      - tuple: 
        - hours: list[str]: Horas que ocorreram vendas
        - total_values: list[float]: Valor total das Vendas
        - total_sales: list[int]: Total de Vendas
    """
    df_filtered = filter_rows_by_date(df, date_col, date)
    df_filtered['sale_hour'] = df_filtered[date_col].dt.hour
    grouped_df = df_filtered.groupby('sale_hour').agg({total_value_col: 'sum', id_col: 'count'}).reset_index()
    hours = grouped_df['sale_hour'].apply(lambda x: f"{x:02d}:00").tolist()
    total_values = grouped_df[total_value_col].tolist()
    total_sales = grouped_df[id_col].apply(lambda x: int(x)).tolist()
    return hours, total_values, total_sales

def sales_per_weekday(
    df: DataFrame, 
    total_value_col: str,
    date_col: str, 
    id_col: str, 
    date: datetime | list[datetime] | None = None
) -> tuple[
    list[str], 
    list[float], 
    list[int]
    ]:
    """
    Calcula a quantidade de vendas por dia da semana, dado um intervalo de tempo
    
    - Args:
      - df::Dataframe: DataFrame contendo os dados de vendas
      - total_value_col::str: Nome da coluna que contém os valores totais das vendas
      - date_col::str: Nome da coluna que contém as datas de venda
      - id_col::str: Nome da coluna que contém os IDs das vendas
      - date: Data Específica ou intervalo Fechado de tempo para análisar as vendas
        
    - Returns:
      - tuple: 
        - weekdays: list[str]: Dias da semana que ocorreram vendas
        - total_values: list[float]: Valor total das Vendas
        - total_sales: list[int]: Total de Vendas
    """
    df_filtered = filter_rows_by_date(df, date_col, date)
    
    df_filtered['sale_weekday'] = df_filtered[date_col].dt.day_name()
    
    grouped_df = df_filtered.groupby('sale_weekday').agg({total_value_col: 'sum', id_col: 'count'}).reset_index()
    
    weekdays_order = [
        'Monday', 
        'Tuesday', 
        'Wednesday', 
        'Thursday', 
        'Friday', 
        'Saturday', 
        'Sunday'
    ]
    
    grouped_df['sale_weekday'] = Categorical(grouped_df['sale_weekday'], categories=weekdays_order, ordered=True)
    
    grouped_df = grouped_df.sort_values('sale_weekday')
    
    weekdays = grouped_df['sale_weekday'].tolist()
    
    total_values = grouped_df[total_value_col].tolist()
    
    total_sales = grouped_df[id_col].apply(lambda x: int(x)).tolist()
    
    return weekdays, total_values, total_sales

def sales_per_month(
    df: DataFrame, 
    total_value_col: str, 
    date_col: str, 
    id_col: str, 
    date: datetime | list[datetime] | None = None
) -> tuple[
    list[str], 
    list[float], 
    list[int]
    ]:
    """
    Calcula a quantidade de vendas por mês, dado um intervalo de tempo
    
    - Args:
      - df::DataFrame: DataFrame contendo os dados de vendas
      - total_value_col::str: Nome da coluna que contém os valores totais das vendas
      - date_col::str: Nome da coluna que contém as datas de venda
      - id_col::str: Nome da coluna que contém os IDs das vendas
      - date: Data Específica ou intervalo Fechado de tempo para análisar as vendas
        
    - Returns:
      - tuple: 
        - months: list[str]: Meses que ocorreram vendas
        - total_values: list[float]: Valor total das Vendas
        - total_sales: list[int]: Total de Vendas
    """
    df_filtered = filter_rows_by_date(df, date_col, date)
    df_filtered['sale_month'] = df_filtered[date_col].dt.month #.to_period('M')
    grouped_df = df_filtered.groupby('sale_month').agg({total_value_col: 'sum', id_col: 'count'}).reset_index()
    
    months = grouped_df['sale_month'].astype(str).tolist()
    
    total_values = grouped_df[total_value_col].tolist()
    
    total_sales = grouped_df[id_col].apply(lambda x: int(x)).tolist()
    
    return (months, total_values, total_sales)

def sales_per_year(
    df: DataFrame, 
    total_value_col: str, 
    date_col: str, 
    id_col: str, 
    date: datetime | list[datetime] | None = None
) -> tuple[
    list[str], 
    list[float], 
    list[int]
    ]:
    """
    Calcula a quantidade de vendas por ano, dado um intervalo de tempo
    
    - Args:
      - df::DataFrame: DataFrame contendo os dados de vendas
      - total_value_col::str: Nome da coluna que contém os valores totais das vendas
      - date_col::str: Nome da coluna que contém as datas de venda
      - id_col::str: Nome da coluna que contém os IDs das vendas
      - date:: Data Específica ou intervalo Fechado de tempo para análisar as vendas
        
    - Returns:
      - tuple: 
        - years: list[str]: Anos que ocorreram vendas
        - total_values: list[float]: Valor total das Vendas
        - total_sales: list[int]: Total de Vendas
    """
    df_filtered = filter_rows_by_date(df, date_col, date)
    
    df_filtered['sale_year'] = df_filtered[date_col].dt.year
    
    grouped_df = df_filtered.groupby('sale_year').agg({total_value_col: 'sum', id_col: 'count'}).reset_index()
    
    years = grouped_df['sale_year'].astype(str).tolist()
    
    total_values = grouped_df[total_value_col].tolist()
    
    total_sales = grouped_df[id_col].apply(lambda x: int(x)).tolist()
    
    return (years, total_values, total_sales)