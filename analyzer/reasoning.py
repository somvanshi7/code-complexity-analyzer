def generate_reasoning(depth, recursion, divide_and_conquer, log_loops):
    reasons = []

    # -----------------------------
    # Recursion explanations
    # -----------------------------
    if recursion > 0:
        if divide_and_conquer:
            reasons.append(
                "Divide-and-conquer recursion detected (problem size halves each call)"
            )
            reasons.append(
                "Recursive calls form a tree of height log n"
            )
            reasons.append(
                "Work done at each level is linear"
            )
            return reasons

        if recursion == 1:
            reasons.append(
                "Single recursive call detected"
            )
            reasons.append(
                "Problem size reduces by a constant amount each call"
            )
            return reasons

        reasons.append(
            "Multiple recursive self-calls detected"
        )
        reasons.append(
            "Number of calls grows exponentially"
        )
        return reasons

    # -----------------------------
    # Logarithmic loop explanations
    # -----------------------------
    if log_loops > 0:
        reasons.append(
            "Loop variable changes multiplicatively (e.g., *= 2 or /= 2)"
        )
        reasons.append(
            "Number of iterations reduces logarithmically"
        )

        if depth > 1:
            reasons.append(
                "Logarithmic loop combined with linear loop"
            )
        return reasons

    # -----------------------------
    # Loop-based explanations
    # -----------------------------
    if depth == 0:
        reasons.append(
            "No loops or recursion detected"
        )
        reasons.append(
            "Constant number of operations"
        )

    elif depth == 1:
        reasons.append(
            "Single loop detected"
        )
        reasons.append(
            "Loop runs proportional to input size n"
        )

    else:
        reasons.append(
            f"{depth} nested loops detected"
        )
        reasons.append(
            "Each inner loop runs fully for each outer iteration"
        )
        reasons.append(
            f"Total operations grow as n^{depth}"
        )

    return reasons

def generate_space_reasoning(aux_space, recursion, recursion_depth):
    reasons = []

    if recursion > 0:
        if recursion_depth == "log n":
            reasons.append(
                "Recursive calls consume stack space proportional to log n"
            )
        else:
            reasons.append(
                "Recursive calls consume stack space proportional to n"
            )
        return reasons

    if aux_space:
        reasons.append(
            "Additional data structures allocated during execution"
        )
        return reasons

    reasons.append(
        "No significant auxiliary memory used"
    )
    return reasons
