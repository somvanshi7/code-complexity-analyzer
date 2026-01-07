def infer_space_complexity(aux_space, recursion, recursion_depth):
    # Auxiliary space dominates recursion stack
    if aux_space:
        return "O(n)"

    if recursion > 0:
        return f"O({recursion_depth})"

    return "O(1)"
