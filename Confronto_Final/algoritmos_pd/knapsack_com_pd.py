# algoritmos_pd/knapsack_com_pd.py

def knapsack_01_pd(valores, pesos, capacidade):
    """
    Resolve o problema da Mochila (Knapsack 0/1) usando Programação Dinâmica.
    
    Args:
        valores (list): Uma lista de valores dos itens.
        pesos (list): Uma lista de pesos dos itens.
        capacidade (int): A capacidade máxima da mochila.
        
    Returns:
        tuple: (valor_maximo, itens_selecionados)
            valor_maximo (int): O valor máximo que pode ser colocado na mochila.
            itens_selecionados (list): Uma lista de índices dos itens selecionados.
    """
    n = len(valores)
    
    dp = [[0 for _ in range(capacidade + 1)] for _ in range(n + 1)]

  
    for i in range(1, n + 1):  
        for w in range(1, capacidade + 1):  
            peso_atual = pesos[i-1]   
            valor_atual = valores[i-1] 

            if peso_atual > w:
                dp[i][w] = dp[i-1][w]

            else:

                dp[i][w] = max(dp[i-1][w], valor_atual + dp[i-1][w - peso_atual])

    valor_maximo = dp[n][capacidade]
    

    itens_selecionados = []
    w = capacidade
    for i in range(n, 0, -1):
        if valor_maximo <= 0: 
            break

        if dp[i][w] != dp[i-1][w]:
            itens_selecionados.append(i - 1)  
            valor_maximo -= valores[i-1]     
            w -= pesos[i-1]                 

    itens_selecionados.reverse() 
    
    return dp, valor_maximo, itens_selecionados



if __name__ == "__main__":
    valores = [18, 22, 28, 29, 7]  
    pesos = [5, 6, 7, 8, 2]     
    capacidade = 11


    valores = [18, 22, 28, 29, 7]
    pesos   = [5, 6, 7, 8, 2]
    capacidade = 11


   
    valores_slide = [18, 22, 28, 29, 7]
    pesos_slide   = [5, 6, 6, 2, 7] 
    capacidade_slide = 11

    dp_table, max_val, selected_items = knapsack_01_pd(valores_slide, pesos_slide, capacidade_slide)

    print("\nTabela DP (apenas para depuração):")
    for row in dp_table:
        print([f"{x:2}" for x in row]) 

    print(f"\nValor Máximo Obtido: {max_val}")
    print(f"Itens Selecionados (índices): {selected_items}")
    

    valores_aula = [18, 22, 28, 29, 7]
    pesos_aula   = [5, 6, 7, 8, 2] 

    print("\n--- Teste com dados da AULA (slide 32 e 34 texto) ---")
    dp_table_aula, max_val_aula, selected_items_aula = knapsack_01_pd(valores_aula, pesos_aula, capacidade_slide)
    print("\nTabela DP (apenas para depuração - dados da aula):")
    for row in dp_table_aula:
        print([f"{x:2}" for x in row])

    print(f"\nValor Máximo Obtido (dados da aula): {max_val_aula}")
    print(f"Itens Selecionados (índices - dados da aula): {selected_items_aula}")
   