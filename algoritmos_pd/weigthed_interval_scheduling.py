from bisect import bisect_right

class Intervalo:
    def __init__(self, inicio, fim, valor):
        self.inicio = inicio
        self.fim = fim
        self.valor = valor

def weighted_interval_scheduling(intervalos):
    # Ordenar os intervalos por tempo de término
    intervalos.sort(key=lambda x: x.fim)
    n = len(intervalos)
    
    # p(j): índice do último intervalo que não conflita com o j
    p = [0] * n
    starts = [i.inicio for i in intervalos]
    ends = [i.fim for i in intervalos]

    for j in range(n):
        i = bisect_right(ends, intervalos[j].inicio) - 1
        p[j] = i

    # Memoization
    M = [-1] * (n + 1)

    def compute_opt(j):
        if j == -1:
            return 0
        if M[j] != -1:
            return M[j]
        incluir = intervalos[j].valor + compute_opt(p[j])
        excluir = compute_opt(j - 1)
        M[j] = max(incluir, excluir)
        return M[j]

    def find_solution(j):
        if j == -1:
            return []
        if intervalos[j].valor + M[p[j]] > M[j - 1]:
            return find_solution(p[j]) + [j]
        else:
            return find_solution(j - 1)

    # Executa
    max_valor = compute_opt(n - 1)
    solucao = find_solution(n - 1)

    # Mostrar solução como índices ou intervalos
    solucao_intervalos = [intervalos[i] for i in solucao]
    return max_valor, solucao_intervalos
