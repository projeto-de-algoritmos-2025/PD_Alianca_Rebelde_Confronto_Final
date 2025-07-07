def lis_recursive(arr):
    n = len(arr)
    memo = {}

    def helper(index, prev_index):
        if index == n:
            return []

        key = (index, prev_index)
        if key in memo:
            return memo[key]

        taken = []
        if prev_index == -1 or arr[index] > arr[prev_index]:
            taken = [arr[index]] + helper(index + 1, index)

        not_taken = helper(index + 1, prev_index)

        result = taken if len(taken) > len(not_taken) else not_taken
        memo[key] = result
        return result

    subseq = helper(0, -1)
    return subseq, len(subseq)