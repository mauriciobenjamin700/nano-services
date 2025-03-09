import matplotlib.colors as mcolors

# Definindo as cores fornecidas
"""colors = [
    "#2F4F4F",  # Cinza escuro
    "#696969",  # Cinza médio escuro
    "#808080",  # Cinza médio
    "#A9A9A9",  # Cinza médio claro
    "#D3D3D3"   # Cinza claro
]"""

EXAMPLE_COLORS = [
    "#caa165",  
    "#ddc4a0",    
    "#ffe2a8",  
    "#fff1b5",  
    "#fffac8"   
]

def generate_color_palette(n, ascending=False, colors: list[str] = EXAMPLE_COLORS) -> list[str]:
    """
    Gera uma lista de N cores seguindo a paleta fornecida, onde cada item mais à esquerda
    da lista tem a intensidade mais forte e cada item à direita tem menos intensidade.
    
    - Args:
        - n:: int : Número de cores a serem geradas.
        - ascending:: bool : Se True, a lista de cores será invertida.
        
        
    
    - Returns:
        - list: Lista de N cores em formato hexadecimal.
    """
    # Interpolando as cores
    cmap = mcolors.LinearSegmentedColormap.from_list("custom_palette", colors)
    palette = [mcolors.rgb2hex(cmap(i / (n - 1))) for i in range(n)]
    
    if ascending:
        palette = list(reversed(palette))
    
    return palette