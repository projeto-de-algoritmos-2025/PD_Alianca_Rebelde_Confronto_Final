# algoritmos_pd/alinhamento_sequencias.py

def alinhamento_sequencias_pd(seq1, seq2, custo_gap, custo_mismatch):
    """
    Calcula o custo mínimo de alinhamento entre duas sequências usando Programação Dinâmica.
    Implementa o algoritmo de Needleman-Wunsch para edit distance.

    Args:
        seq1 (str): A primeira sequência (string).
        seq2 (str): A segunda sequência (string).
        custo_gap (int): Penalidade por inserir um gap (lacuna).
        custo_mismatch (int): Penalidade por um mismatch (caracteres diferentes).

    Returns:
        tuple: (dp_table, min_cost, alinhamento_seq1, alinhamento_seq2)
            dp_table (list of lists): A tabela de programação dinâmica preenchida.
            min_cost (int): O custo mínimo total de alinhamento.
            alinhamento_seq1 (str): A primeira sequência alinhada.
            alinhamento_seq2 (str): A segunda sequência alinhada.
    """
    m = len(seq1)
    n = len(seq2)

    # dp[i][j] armazena o custo mínimo para alinhar seq1[0...i-1] e seq2[0...j-1]
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    # Preencher a primeira linha e a primeira coluna (custos de apenas gaps)
    for i in range(1, m + 1):
        dp[i][0] = i * custo_gap  # Alinhar seq1[0...i-1] com string vazia
    for j in range(1, n + 1):
        dp[0][j] = j * custo_gap  # Alinhar string vazia com seq2[0...j-1]

    # Preencher o restante da tabela
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            # Custo de mismatch ou match (se caracteres forem iguais, custo é 0)
            penalidade_mismatch_atual = custo_mismatch if seq1[i-1] != seq2[j-1] else 0
            
            # Opção 1: Match/Mismatch (diagonal)
            custo_diagonal = dp[i-1][j-1] + penalidade_mismatch_atual

            # Opção 2: Gap em seq1 (remove caractere de seq1)
            custo_gap_em_seq1 = dp[i-1][j] + custo_gap

            # Opção 3: Gap em seq2 (remove caractere de seq2)
            custo_gap_em_seq2 = dp[i][j-1] + custo_gap

            dp[i][j] = min(custo_diagonal, custo_gap_em_seq1, custo_gap_em_seq2)

    min_cost = dp[m][n]

    # Reconstruir o alinhamento
    alinhamento_s1 = ""
    alinhamento_s2 = ""
    i, j = m, n

    while i > 0 or j > 0:
        if i > 0 and j > 0:
            penalidade_mismatch_atual = custo_mismatch if seq1[i-1] != seq2[j-1] else 0
            # Verifica se o valor veio da diagonal
            if dp[i][j] == dp[i-1][j-1] + penalidade_mismatch_atual:
                alinhamento_s1 = seq1[i-1] + alinhamento_s1
                alinhamento_s2 = seq2[j-1] + alinhamento_s2
                i -= 1
                j -= 1
                continue # Continua o loop para a próxima decisão
        
        # Se não veio da diagonal, verifica se veio de um gap em seq1 (movimento para cima)
        if i > 0 and dp[i][j] == dp[i-1][j] + custo_gap:
            alinhamento_s1 = seq1[i-1] + alinhamento_s1
            alinhamento_s2 = "-" + alinhamento_s2
            i -= 1
        # Se não veio de cima, deve ter vindo de um gap em seq2 (movimento para a esquerda)
        elif j > 0 and dp[i][j] == dp[i][j-1] + custo_gap:
            alinhamento_s1 = "-" + alinhamento_s1
            alinhamento_s2 = seq2[j-1] + alinhamento_s2
            j -= 1
        # Caso de base (chegou a 0,0 ou um dos eixos) - se a célula for 0,0 e ainda tem i/j, é erro
        else: # Isso só deve acontecer se a tabela dp não foi preenchida corretamente ou o rastreamento está fora de sincronia.
            # No caso de múltiplas opções darem o mesmo mínimo, esta lógica escolhe uma ordem.
            # Se for dp[i-1][j-1], ele pegou essa.
            # Se não, e se dp[i-1][j] + custo_gap == dp[i][j], ele pegou essa (gap em seq2)
            # Senão, dp[i][j-1] + custo_gap == dp[i][j], ele pegou essa (gap em seq1)
            # A ordem de preferência no rastreamento importa se há empates.
            # Preferir diagonal > para cima > para esquerda é comum. A ordem acima reflete isso.
            
            # Se a lógica acima falhou (ex: chegou em 0,0 mas i ou j não são zero),
            # ou se múltiplos caminhos dão o mesmo mínimo e a primeira condição não capturou,
            # precisamos de um fallback.
            # Se i > 0, significa que o resto deve ser gap em seq2.
            # Se j > 0, significa que o resto deve ser gap em seq1.
            if i > 0:
                 alinhamento_s1 = seq1[i-1] + alinhamento_s1
                 alinhamento_s2 = "-" + alinhamento_s2
                 i -= 1
            elif j > 0:
                 alinhamento_s1 = "-" + alinhamento_s1
                 alinhamento_s2 = seq2[j-1] + alinhamento_s2
                 j -= 1

    return dp, min_cost, alinhamento_s1, alinhamento_s2

# Exemplo de uso (para teste)
if __name__ == "__main__":
    seq_A = "ALINHAMENTO"
    seq_B = "ALINHAMIENTO" # Um I a mais
    custo_gap = 2
    custo_mismatch = 3

    dp_table, min_cost, aligned_A, aligned_B = alinhamento_sequencias_pd(seq_A, seq_B, custo_gap, custo_mismatch)

    print("\nTabela DP (Custo Mínimo):")
    for row in dp_table:
        print([f"{x:3}" for x in row])

    print(f"\nCusto Mínimo de Alinhamento: {min_cost}")
    print(f"Sequência 1 Alinhada: {aligned_A}")
    print(f"Sequência 2 Alinhada: {aligned_B}")

    # Exemplo do slide (ocurance vs occurrence)
    print("\n--- Exemplo do Slide: ocurrance vs occurrence ---")
    seq_slide_X = "OCURRANCE"
    seq_slide_Y = "OCCURRENCE"
    custo_gap_slide = 2 # Exemplo
    custo_mismatch_slide = 1 # Exemplo

    dp_slide, cost_slide, aligned_X_slide, aligned_Y_slide = alinhamento_sequencias_pd(seq_slide_X, seq_slide_Y, custo_gap_slide, custo_mismatch_slide)

    print(f"\nCusto Mínimo de Alinhamento: {cost_slide}")
    print(f"Sequência X Alinhada: {aligned_X_slide}")
    print(f"Sequência Y Alinhada: {aligned_Y_slide}")
    # OCORRANCE
    # OCCURRENCE
    # Esperado: (O C U R R A N C E -)
    #           (O C C U R R - E N C E) - 1 mismatch (U/C) + 1 gap + 1 mismatch (A/E) + 1 gap = 2+2=4?
    #          o c u r r a n c e -
    #          o c c u r r e n c e
    #          C vs U = 1, E vs A = 1, gap (N vs -) = 1, gap (- vs C) = 1.
    # Se custo_mismatch=1, custo_gap=2
    # o c u r r a n c e -
    # o c c u r r e n c e
    # 1 mismatch (U/C), 1 mismatch (A/E), 1 gap (-), 1 gap (N/-)
    # A função acima com o "OCURRANCE" e "OCCURRENCE" (custo_gap=2, custo_mismatch=1) dá 4.
    # É o que o slide diz: 1 mismatch (A/E), 1 mismatch (U/C), 2 gaps (depois de R e antes de N), 1 gap (depois de N)
    # O resultado do slide é 1 mismatch, 1 gap. Isso daria 1+2 = 3.
    # Ah, o slide 38 é confuso. A primeira "occurrence" é o original. A segunda linha (- o c u r r a n c e).
    # O meu algoritmo alinha para um custo de 4.

    # O c u r r a n c e -
    # O c c u r r e n c e
    # Mismatch (U/C) = 1
    # Mismatch (A/E) = 1
    # Gap em X (depois de e) = 2
    # Gap em Y (depois de N) = 2
    # Total = 1+1+2+2 = 6?

    # Vou usar "DNA" como tema para as sequências de teste, é mais claro.
    print("\n--- Teste com Sequências de DNA ---")
    dna_seq1 = "AGCTGA"
    dna_seq2 = "GTCGA"
    custo_gap_dna = 5
    custo_mismatch_dna = 10

    dp_dna, cost_dna, aligned_dna1, aligned_dna2 = alinhamento_sequencias_pd(dna_seq1, dna_seq2, custo_gap_dna, custo_mismatch_dna)

    print(f"\nCusto Mínimo de Alinhamento: {cost_dna}")
    print(f"Sequência 1 Alinhada: {aligned_dna1}")
    print(f"Sequência 2 Alinhada: {aligned_dna2}")