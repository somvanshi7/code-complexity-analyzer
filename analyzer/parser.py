import ast


class CodeParser(ast.NodeVisitor):
    def __init__(self, target_function=None):
        self.target_function = target_function

        # -------- TIME --------
        self.current_depth = 0
        self.max_depth = 0
        self.loops = 0

        self.function_name = None
        self.recursive_calls = 0
        self.divide_and_conquer = False

        # Track pointer variables
        self.pointer_vars = set()
        self.reset_vars = set()

        # -------- SPACE --------
        self.aux_space = False
        self.recursion_depth = None

        self.inside_target = False

    # =================================================
    def visit_FunctionDef(self, node):
        if node.name == self.target_function:
            self.function_name = node.name
            self.inside_target = True
            self.generic_visit(node)
            self.inside_target = False

    # =================================================
    def visit_For(self, node):
        if not self.inside_target:
            return

        self.current_depth += 1
        self.loops += 1
        self.max_depth = max(self.max_depth, self.current_depth)

        self.generic_visit(node)

        self.current_depth -= 1

    def visit_While(self, node):
        if not self.inside_target:
            return

        # Check if this loop walks pointers
        walks_pointer = False
        for stmt in ast.walk(node):
            if isinstance(stmt, ast.AugAssign):
                if isinstance(stmt.target, ast.Name):
                    self.pointer_vars.add(stmt.target.id)
                    walks_pointer = True

        # If pointer was reset earlier, this is REAL nesting
        if walks_pointer and not (self.pointer_vars & self.reset_vars):
            # Morris-style amortized loop
            self.loops += 1
            self.max_depth = max(self.max_depth, self.current_depth + 1)
            self.generic_visit(node)
            return

        # Otherwise, treat as real nesting
        self.current_depth += 1
        self.loops += 1
        self.max_depth = max(self.max_depth, self.current_depth)

        self.generic_visit(node)

        self.current_depth -= 1

    # =================================================
    def visit_Assign(self, node):
        if not self.inside_target:
            return

        # Track variable resets
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.reset_vars.add(target.id)

        # Ignore output containers
        if isinstance(node.value, (ast.List, ast.Dict, ast.Set)):
            return

        self.aux_space = True
        self.generic_visit(node)

    # =================================================
    def visit_Call(self, node):
    # Detect recursion
        if (
            self.inside_target
            and isinstance(node.func, ast.Name)
            and node.func.id == self.function_name
        ):
            self.recursive_calls += 1

    # Detect slicing (Python-specific auxiliary space)
        for arg in node.args:
            if isinstance(arg, ast.Subscript):
                # arr[mid:], arr[:mid] → slicing → NEW LIST
                if isinstance(arg.slice, (ast.Slice, ast.Tuple)):
                    self.aux_space = True
                    self.divide_and_conquer = True

        self.generic_visit(node)


    # =================================================
    def finalize(self):
        if self.recursive_calls > 0:
            self.recursion_depth = (
                "log n" if self.divide_and_conquer else "n"
            )

