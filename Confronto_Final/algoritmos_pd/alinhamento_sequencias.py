

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

    
    dp = [[0 for _ in range(n + 1)] for _ in range(m + 1)]

    
    for i in range(1, m + 1):
        dp[i][0] = i * custo_gap  
    for j in range(1, n + 1):
        dp[0][j] = j * custo_gap  

    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            
            penalidade_mismatch_atual = custo_mismatch if seq1[i-1] != seq2[j-1] else 0
            
            
            custo_diagonal = dp[i-1][j-1] + penalidade_mismatch_atual

            
            custo_gap_em_seq1 = dp[i-1][j] + custo_gap

            
            custo_gap_em_seq2 = dp[i][j-1] + custo_gap

            dp[i][j] = min(custo_diagonal, custo_gap_em_seq1, custo_gap_em_seq2)

    min_cost = dp[m][n]

    
    alinhamento_s1 = ""
    alinhamento_s2 = ""
    i, j = m, n

    while i > 0 or j > 0:
        if i > 0 and j > 0:
            penalidade_mismatch_atual = custo_mismatch if seq1[i-1] != seq2[j-1] else 0
            
            if dp[i][j] == dp[i-1][j-1] + penalidade_mismatch_atual:
                alinhamento_s1 = seq1[i-1] + alinhamento_s1
                alinhamento_s2 = seq2[j-1] + alinhamento_s2
                i -= 1
                j -= 1
                continue 
        
        # 
        if i > 0 and dp[i][j] == dp[i-1][j] + custo_gap:
            alinhamento_s1 = seq1[i-1] + alinhamento_s1
            alinhamento_s2 = "-" + alinhamento_s2
            i -= 1
        
        elif j > 0 and dp[i][j] == dp[i][j-1] + custo_gap:
            alinhamento_s1 = "-" + alinhamento_s1
            alinhamento_s2 = seq2[j-1] + alinhamento_s2
            j -= 1
        
        else: 
            if i > 0:
                 alinhamento_s1 = seq1[i-1] + alinhamento_s1
                 alinhamento_s2 = "-" + alinhamento_s2
                 i -= 1
            elif j > 0:
                 alinhamento_s1 = "-" + alinhamento_s1
                 alinhamento_s2 = seq2[j-1] + alinhamento_s2
                 j -= 1

    return dp, min_cost, alinhamento_s1, alinhamento_s2


if __name__ == "__main__":
    seq_A = "ALINHAMENTO"
    seq_B = "ALINHAMIENTO" 
    custo_gap = 2
    custo_mismatch = 3

    dp_table, min_cost, aligned_A, aligned_B = alinhamento_sequencias_pd(seq_A, seq_B, custo_gap, custo_mismatch)

    print("\nTabela DP (Custo Mínimo):")
    for row in dp_table:
        print([f"{x:3}" for x in row])

    print(f"\nCusto Mínimo de Alinhamento: {min_cost}")
    print(f"Sequência 1 Alinhada: {aligned_A}")
    print(f"Sequência 2 Alinhada: {aligned_B}")

    
    print("\n--- Exemplo do Slide: ocurrance vs occurrence ---")
    seq_slide_X = "OCURRANCE"
    seq_slide_Y = "OCCURRENCE"
    custo_gap_slide = 2 
    custo_mismatch_slide = 1 

    dp_slide, cost_slide, aligned_X_slide, aligned_Y_slide = alinhamento_sequencias_pd(seq_slide_X, seq_slide_Y, custo_gap_slide, custo_mismatch_slide)

    print(f"\nCusto Mínimo de Alinhamento: {cost_slide}")
    print(f"Sequência X Alinhada: {aligned_X_slide}")
    print(f"Sequência Y Alinhada: {aligned_Y_slide}")
    
    print("\n--- Teste com Sequências de DNA ---")
    dna_seq1 = "AGCTGA"
    dna_seq2 = "GTCGA"
    custo_gap_dna = 5
    custo_mismatch_dna = 10

    dp_dna, cost_dna, aligned_dna1, aligned_dna2 = alinhamento_sequencias_pd(dna_seq1, dna_seq2, custo_gap_dna, custo_mismatch_dna)

    print(f"\nCusto Mínimo de Alinhamento: {cost_dna}")
    print(f"Sequência 1 Alinhada: {aligned_dna1}")
    print(f"Sequência 2 Alinhada: {aligned_dna2}")