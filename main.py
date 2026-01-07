import ast

from analyzer.cpp_parser import CPPParser
from analyzer.java_parser import JavaParser
from analyzer.parser import CodeParser

from analyzer.rules import infer_time_complexity
from analyzer.space_rules import infer_space_complexity
from analyzer.reasoning import (
    generate_reasoning,
    generate_space_reasoning,
)

# =================================================
# CONFIG
# =================================================
lang = "cpp"  # python | cpp | java
code = open("input.txt").read()

# =================================================
# DEFAULTS (important)
# =================================================
depth = 0
recursion = 0
dac = False
log_loops = 0

aux_space = False
rec_depth = None

# =================================================
# PYTHON ANALYSIS
# =================================================
if lang == "python":
    tree = ast.parse(code)
    parser = CodeParser()
    parser.visit(tree)

    depth = parser.nested_loops
    recursion = parser.recursive_calls

    aux_space = False
    rec_depth = "n" if recursion > 0 else None

# =================================================
# JAVA ANALYSIS
# =================================================
elif lang == "java":
    parser = JavaParser(code)
    parser.analyze()

    depth = parser.max_depth
    recursion = parser.recursion
    dac = parser.divide_and_conquer
    log_loops = parser.log_loops

    aux_space = parser.aux_space
    rec_depth = parser.recursion_depth

# =================================================
# C++ ANALYSIS
# =================================================
elif lang == "cpp":
    parser = CPPParser(code)
    parser.analyze()

    depth = parser.max_depth
    recursion = parser.recursion
    dac = parser.divide_and_conquer
    log_loops = parser.log_loops

    aux_space = parser.aux_space
    rec_depth = parser.recursion_depth

    # -------------------------------------------------
    # 🔥 IMPORTANT CONVENTION FIX 🔥
    # Ignore OUTPUT-ONLY containers (algorithmic rule)
    # -------------------------------------------------
    if (
        recursion == 0
        and not dac
        and "vector<" in code
        and "return" in code
    ):
        aux_space = False

else:
    raise ValueError("Unsupported language")

# =================================================
# FINAL RESULTS
# =================================================
time_complexity = infer_time_complexity(
    depth,
    recursion,
    dac,
    log_loops,
)

space_complexity = infer_space_complexity(
    aux_space,
    recursion,
    rec_depth,
)

time_reason = generate_reasoning(
    depth,
    recursion,
    dac,
    log_loops,
)

space_reason = generate_space_reasoning(
    aux_space,
    recursion,
    rec_depth,
)

# =================================================
# OUTPUT
# =================================================
print("\n===== ANALYSIS RESULT =====\n")

print("Language:", lang)
print("Max Nesting:", depth)
print("Recursion:", recursion)
print("Log Loops:", log_loops)

print("\nTime Complexity:", time_complexity)
print("Space Complexity:", space_complexity)

print("\nTime Reason:")
for r in time_reason:
    print("-", r)

print("\nSpace Reason:")
for r in space_reason:
    print("-", r)
