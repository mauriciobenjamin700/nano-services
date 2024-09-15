from datetime import datetime
from matplotlib.figure import Figure
import matplotlib.pyplot as plt


def custom_bar_chart(
    items_name: list, 
    items_quantity: list, 
    title: str,
    legend: list[str], 
    y_label: str, 
    color_bar: list
) -> plt.Figure:
    """
    Cria um gráfico de barras usando dados processados
    
    - Args:
        - items_name:: list[Strings]: Lista contendo o rotúto de cada item (ex: ["Pão", "Ovo", "Bolo"]), será usada no eixo x do gráfico
        - items_quantity:: list[Numbers]: Lista contendo a quantidade de cada item (ex: [15, 50, 12, 2.5])
        - title:: str: Título do Gráfico 
        - legend:: str: Legenda do Gráfico
        - y_label:: str: Legenda do eixo y do gráfico
        - color_bar:: list[Strings]: Lista contendo a cor de cada item na - - legenda (ex: ["red", "blue", "orange"])
        
    - Return:
        - fig: Figure: Gráfico de barras criado com os dados passados
    """
    
    fig, ax = plt.subplots()
    
    
    bars = ax.bar(items_name, items_quantity, label=items_name,color=color_bar)
    ax.set_ylabel(y_label)
    if len(title) > 0:
        ax.set_title(title)
    ax.legend(legend)

    ax.set_xticklabels([])
    
    # Definindo os intervalos de 1 em 1 no eixo y
    #ax.set_yticks(range(0, int(max(items_quantity)) + 2, 1))
    #ax.set_ylim(0, max(items_quantity) + 1)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2, 
            height, 
            f'{height}', 
            ha='center', 
            va='bottom'
        )
    
    #plt.show()
    return fig

def custom_pie_chart(
    items_name: list, 
    items_quantity: list, 
    title: str,
    legend: list[str], 
    color_pie: list
) -> plt.Figure:
    """
    Cria um gráfico de pizza usando dados processados
    
    - Args:
        - items_name:: list[Strings]: Lista contendo o rótulo de cada item - (ex: ["Pão", "Ovo", "Bolo"])
        - items_quantity:: list[Numbers]: Lista contendo a quantidade de cada item (ex: [15, 50, 12])
        - title:: str: Título do Gráfico 
        - legend:: list[str]: Legenda do Gráfico
        - color_pie:: list[Strings]: Lista contendo a cor de cada item na - legenda (ex: ["red", "blue", "orange"])
        
    - Return:
        - fig: Figure: Gráfico de pizza criado com os dados passados
    """
    for idx in range(0,len(items_name)):
        if items_quantity[idx] < 0:
            del items_name[idx]
            del items_quantity[idx]
    fig, ax = plt.subplots()
    
    wedges, texts, autotexts = ax.pie(
        items_quantity, 
        labels=items_name, 
        colors=color_pie, 
        autopct='%1.1f%%', 
        startangle=90
    )
    if len(title) > 0:
        ax.set_title(title)

    ax.legend(wedges, legend, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    # Ajusta o texto dos percentuais
    for text in autotexts:
        text.set_color('black')
    
    #plt.show()
    return fig

def custom_donut_chart(
    items_name: list, 
    items_quantity: list, 
    title: str,
    legend: list[str], 
    color_donut: list
) -> plt.Figure:
    """
    Cria um gráfico de rosca usando dados processados
    
    - Args:
        - items_name:: list[str]: Lista contendo o rótulo de cada item (ex: ["Pão", "Ovo", "Bolo"])
        - items_quantity:: list[Numbers]: Lista contendo a quantidade de cada item (ex: [15, 50, 12, 2.5])
        - title:: str: Título do Gráfico 
        - legend:: list[str]: Legenda do Gráfico
        - color_donut:: list[str]: Lista contendo a cor de cada item na - legenda (ex: ["red", "blue", "orange", #ffff])
        
    - Return:
        - fig: Figure: Gráfico de rosca criado com os dados passados
    """
    for idx in range(0,len(items_name)):
        if items_quantity[idx] < 0:
            del items_name[idx]
            del items_quantity[idx]

    fig, ax = plt.subplots()
    
    wedges, texts, autotexts = ax.pie(
        items_quantity, 
        labels=items_name, 
        colors=color_donut, 
        autopct='%1.1f%%', 
        startangle=90,
        wedgeprops=dict(width=0.3)  # Define a largura das fatias para criar o efeito de rosca
    )
    
    if len(title) > 0:
        ax.set_title(title)
    ax.legend(wedges, legend, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))
    
    # Ajusta o texto dos percentuais
    for text in autotexts:
        text.set_color('black')
    
    #plt.show()
    return fig
    
def custom_line_chart(
    date:list[datetime],
    sales: list[float],
    title: str = "Desempenho de Vendas",
    x_label: str = "Data",
    y_label: str = "Número de Vendas",
    color_line: str = 'b',
    marker: str = 'o',
    linestyle: str = '-'
) -> plt.Figure:
    """
    Cria um gráfico de linha usando dados processados
    
    - Args:
        - date:: list[datetime]: Lista contendo as datas (ex: [datetime(2022, 1, 1), datetime(2022, 1, 2), datetime(2022, 1, 3)])
        - sales:: list[float]: Lista contendo as vendas correspondentes as datas (ex: [1000, 1500, 2000])
        - title:: str: Título do Gráfico
        - x_label:: str: Legenda do eixo x do gráfico
        - y_label:: str: Legenda do eixo y do gráfico
        - color_line:: str: Cor da linha do gráfico (ex: 'b' para azul)
        - marker:: str: Simbolo usado para representar os pontos no gráfico (ex: 'o' para círculo)
        - linestyle:: str: Estilo da linha do gráfico (ex: '-' para uma linha contínua)
        
    - Return:
        - fig: Figure: Gráfico de linha criado com os dados passados
    """
    
    fig = plt.figure(figsize=(10, 5))
    plt.plot(date, sales, marker=marker, linestyle=linestyle, color=color_line)

    # Adicionar título e rótulos aos eixos
    if len(title) > 0:
        plt.title(title)
    if len(x_label) > 0:
        plt.xlabel(x_label)
    if len(y_label) > 0:
        plt.ylabel(y_label)

    # Mostrar o gráfico
    plt.grid(True)
    #plt.show()
    
    return fig

def plot_fig(fig:Figure):
    """
    Plota uma Figura na Tela
    
    - Args:
        - fig:: Figure: Figura do Matplotlib que será plotada
    
    - Returns:
        - None
    """
    plt.figure(fig)
    plt.show()