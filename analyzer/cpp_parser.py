import re

class CPPParser:
    def __init__(self, code):
        self.code = code

        # ---- TIME ----
        self.loops = 0
        self.log_loops = 0
        self.max_depth = 0
        self.recursion = 0
        self.divide_and_conquer = False
        self.function_name = None

        # ---- SPACE ----
        self.aux_space = False
        self.recursion_depth = None

    # =================================================
    # ENTRY POINT
    # =================================================
    def analyze(self):
        self._detect_function_name()
        self._detect_loops()
        self._detect_recursion()
        self._detect_divide_and_conquer()
        self._detect_space()

    # =================================================
    # FUNCTION NAME DETECTION
    # =================================================
    def _detect_function_name(self):
        match = re.search(
            r'\b\w+\s+(\w+)\s*\([^)]*\)\s*{',
            self.code
        )
        if match:
            self.function_name = match.group(1)

    # =================================================
    # LOOP & NESTING DETECTION
    # =================================================
    def _detect_loops(self):
        depth = 0
        for line in self.code.splitlines():
            if re.search(r'\b(for|while)\b', line):
                self.loops += 1
                depth += 1
                self.max_depth = max(self.max_depth, depth)

                # log-n loop detection
                if re.search(r'(\*=|/=|>>=)', line):
                    self.log_loops += 1
                if re.search(r'/\s*2', line):
                    self.log_loops += 1

            # reduce depth only when loop block closes
            if re.search(r'}\s*$', line) and depth > 0:
                depth -= 1

            # Detect binary search style halving
            if (
                re.search(r'mid\s*=\s*.*\/\s*2', self.code)
                and re.search(r'(left|right)\s*=\s*mid', self.code)
            ):
                self.log_loops += 1


    # =================================================
    # RECURSION DETECTION (SELF-CALL ONLY)
    # =================================================
    def _detect_recursion(self):
        if not self.function_name:
            self.recursion = 0
            return

        calls = re.findall(
            rf'\b{self.function_name}\s*\(',
            self.code
        )

        # subtract function definition
        self.recursion = max(0, len(calls) - 1)

    # =================================================
    # DIVIDE & CONQUER DETECTION
    # =================================================
    def _detect_divide_and_conquer(self):
        if (
            "mid" in self.code
            or "/ 2" in self.code
            or ">> 1" in self.code
        ):
            self.divide_and_conquer = True

    # =================================================
    # SPACE COMPLEXITY DETECTION (CORRECT)
    # =================================================
    def _detect_space(self):
        aux = False

    # ---------------------------------------------
    # Ignore INPUT arrays (function parameters)
    # ---------------------------------------------
        header_end = self.code.find("{")
        header = self.code[:header_end] if header_end != -1 else ""

        param_arrays = re.findall(
            r'\b(int|float|double|char)\s+\w+\s*\[',
            header
        )

        body_arrays = re.findall(
            r'\b(int|float|double|char)\s+\w+\s*\[',
            self.code
        )

    # count array only if it's NOT a parameter
        if body_arrays and not param_arrays:
            aux = True

    # ---------------------------------------------
    # Handle vectors (IGNORE output vector)
    # ---------------------------------------------
        vector_defs = re.findall(
            r'vector<.*?>\s+(\w+)',
            self.code
        )

        return_vars = re.findall(
            r'return\s+(\w+)',
            self.code
        )

        for v in vector_defs:
            if v not in return_vars:
                aux = True

    # ---------------------------------------------
    # Assign FINAL decision
    # ---------------------------------------------
        self.aux_space = aux

    # ---------------------------------------------
    # Recursion stack space
    # ---------------------------------------------
        if self.recursion > 0:
            if self.divide_and_conquer:
                self.recursion_depth = "log n"
            else:
                self.recursion_depth = "n"

