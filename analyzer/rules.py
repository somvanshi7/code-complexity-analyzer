def infer_time_complexity(depth, recursion, divide_and_conquer=False, log_loops=0):
    # --- Recursion cases ---
    if recursion > 0:
        if divide_and_conquer:
            return "O(n log n)"
        if recursion == 1:
            return "O(n)"
        return "O(2^n)"

    # --- Logarithmic loops ---
    if log_loops > 0:
        if depth == 1:
            return "O(log n)"
        if depth == 2:
            return "O(n log n)"
        return "O(log^2 n)"

    # --- Loop-based cases ---
    if depth == 0:
        return "O(1)"
    if depth == 1:
        return "O(n)"
    if depth == 2:
        return "O(n^2)"
    return f"O(n^{depth})"
