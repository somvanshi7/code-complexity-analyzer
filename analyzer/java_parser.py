import re


class JavaParser:
    def __init__(self, code):
        self.code = code

        # ---------------- TIME ----------------
        self.loops = 0
        self.log_loops = 0
        self.max_depth = 0
        self.recursion = 0
        self.divide_and_conquer = False
        self.function_name = None

        # ---------------- SPACE ----------------
        self.aux_space = False
        self.recursion_depth = None

    # =================================================
    def analyze(self):
        self._detect_function_name()
        self._detect_loops()
        self._detect_recursion()
        self._detect_divide_and_conquer()
        self._detect_space()

    # =================================================
    def _detect_function_name(self):
        match = re.search(
            r'\b(public|private|protected)?\s*\w+\s+(\w+)\s*\([^)]*\)\s*{',
            self.code
        )
        if match:
            self.function_name = match.group(2)

    # =================================================
    def _detect_loops(self):
        depth = 0

        for line in self.code.splitlines():
            if re.search(r'\b(for|while)\b', line):
                self.loops += 1
                depth += 1
                self.max_depth = max(self.max_depth, depth)

                if re.search(r'(\*=|/=|>>=)', line):
                    self.log_loops += 1
                if re.search(r'/\s*2', line):
                    self.log_loops += 1

            if re.search(r'}\s*$', line) and depth > 0:
                depth -= 1

    # =================================================
    def _detect_recursion(self):
        if not self.function_name:
            self.recursion = 0
            return

        calls = re.findall(
            rf'\b{self.function_name}\s*\(',
            self.code
        )

        self.recursion = max(0, len(calls) - 1)

    # =================================================
    def _detect_divide_and_conquer(self):
        if (
            "mid" in self.code
            or "/ 2" in self.code
            or ">> 1" in self.code
        ):
            self.divide_and_conquer = True

    # =================================================
    def _detect_space(self):
        aux = False

        # -----------------------------
        # Ignore input arrays
        # -----------------------------
        header_end = self.code.find("{")
        header = self.code[:header_end] if header_end != -1 else ""

        param_arrays = re.findall(
            r'\b\w+\s+\w+\s*\[\]',
            header
        )

        body_arrays = re.findall(
            r'\b\w+\s+\w+\s*\[\]',
            self.code
        )

        if body_arrays and not param_arrays:
            aux = True

        # -----------------------------
        # Handle Lists / ArrayLists (ignore output)
        # -----------------------------
        list_defs = re.findall(
            r'(List|ArrayList)<.*?>\s+(\w+)',
            self.code
        )

        return_vars = re.findall(
            r'return\s+(\w+)',
            self.code
        )

        for _, name in list_defs:
            if name not in return_vars:
                aux = True

        self.aux_space = aux

        # -----------------------------
        # Recursion stack
        # -----------------------------
        if self.recursion > 0:
            self.recursion_depth = (
                "log n" if self.divide_and_conquer else "n"
            )
