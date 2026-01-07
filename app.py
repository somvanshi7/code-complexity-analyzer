import streamlit as st
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
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Code Complexity Analyzer",
    layout="wide",
)

st.title("🧠 Code Complexity Analyzer")
st.caption("Time & Space Complexity with Reasoning")

# =================================================
# INPUT
# =================================================
lang = st.selectbox(
    "Select Language",
    ["cpp", "java", "python"],
)

code = st.text_area(
    "Paste your code here",
    height=350,
)

function_name = None
if lang == "python":
    function_name = st.text_input(
        "Function to analyze (Python only)",
        value=""
    )

analyze = st.button("Analyze")

# =================================================
# ANALYSIS
# =================================================
if analyze:
    if not code.strip():
        st.warning("Please paste some code.")
        st.stop()

    depth = 0
    recursion = 0
    dac = False
    log_loops = 0
    aux_space = False
    rec_depth = None

    # ---------------- PYTHON ----------------
    if lang == "python":
        tree = ast.parse(code)
        parser = CodeParser(target_function=function_name)
        parser.visit(tree)
        parser.finalize()

        depth = parser.max_depth
        recursion = parser.recursive_calls
        dac = parser.divide_and_conquer
        aux_space = parser.aux_space
        rec_depth = parser.recursion_depth


        # 🔥 IMPORTANT CONVENTION 🔥
        # Ignore output-only space in Python
        if (
            recursion == 0
            and "return" in code
            and "[" in code
        ):
            aux_space = False

    # ---------------- JAVA ----------------
    elif lang == "java":
        parser = JavaParser(code)
        parser.analyze()

        depth = parser.max_depth
        recursion = parser.recursion
        dac = parser.divide_and_conquer
        log_loops = parser.log_loops
        aux_space = parser.aux_space
        rec_depth = parser.recursion_depth

    # ---------------- C++ ----------------
    elif lang == "cpp":
        parser = CPPParser(code)
        parser.analyze()

        depth = parser.max_depth
        recursion = parser.recursion
        dac = parser.divide_and_conquer
        log_loops = parser.log_loops
        aux_space = parser.aux_space
        rec_depth = parser.recursion_depth

        # Ignore output-only space
        if (
            recursion == 0
            and not dac
            and "vector<" in code
            and "return" in code
        ):
            aux_space = False

    # ---------------- RESULTS ----------------
    time_c = infer_time_complexity(
        depth, recursion, dac, log_loops
    )

    space_c = infer_space_complexity(
        aux_space, recursion, rec_depth
    )

    time_reason = generate_reasoning(
        depth, recursion, dac, log_loops
    )

    space_reason = generate_space_reasoning(
        aux_space, recursion, rec_depth
    )

    # =================================================
    # OUTPUT
    # =================================================
    st.success("Analysis Complete")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("⏱ Time Complexity")
        st.code(time_c)
        st.markdown("**Reason:**")
        for r in time_reason:
            st.markdown(f"- {r}")

    with col2:
        st.subheader("💾 Space Complexity")
        st.code(space_c)
        st.markdown("**Reason:**")
        for r in space_reason:
            st.markdown(f"- {r}")
