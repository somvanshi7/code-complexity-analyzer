from analyzer.rules import infer_time_complexity

def analyze(parser):
    complexity = infer_time_complexity(
        parser.loops,
        parser.nested_loops,
        parser.recursive_calls
    )

    return {
        "loops": parser.loops,
        "max_nesting": parser.nested_loops,
        "recursion": parser.recursive_calls,
        "time_complexity": complexity
    }
