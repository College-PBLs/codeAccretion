class JavaGenerator:
    def __init__(self):
        self.indent_level = 0
        self.code_lines = []
        self._in_main = False   # ← add this

    def indent(self):
        return "    " * self.indent_level


    # Entry point
    def generate(self, tree):
        self.code_lines = []
        self.code_lines.append("import java.util.*;")
        self.code_lines.append("import java.io.*;")
        class_name = tree.get("class_name") or "Main"

        self.code_lines.append(f"public class {class_name} {{")
        self.indent_level += 1

        # Emit field declarations first
        for node in tree.get("body", []):
            if node["type"] == "FieldDeclaration":
                self.gen_field(node)

        if tree.get("body"):
            self.code_lines.append("")

        # Emit methods
        for node in tree.get("functions", []):
            self.gen_method(node)
            self.code_lines.append("")

        # If no explicit methods, wrap top-level statements in main
        has_main = any(f["name"] == "main" for f in tree.get("functions", []))
        if not has_main:
            self._gen_main_wrapper(tree)

        self.indent_level -= 1
        self.code_lines.append("}")

        return "\n".join(self.code_lines)


    # Class members
    def gen_field(self, node):
        java_type = self.convert_type(node["data_type"])
        mods = self._java_modifiers(node.get("modifiers", []))
        mod_str = mods + " " if mods else "private "
        if "initializer" in node:
            init = self.gen_expression(node["initializer"])
            self.code_lines.append(f"{self.indent()}{mod_str}{java_type} {node['name']} = {init};")
        else:
            self.code_lines.append(f"{self.indent()}{mod_str}{java_type} {node['name']};")

    def _java_modifiers(self, modifiers):
        """Map C++ modifier list to Java equivalents."""
        java_mods = []
        for m in modifiers:
            if m in ("public", "private", "protected", "static"):
                java_mods.append(m)
            elif m == "virtual":
                pass  # handled at method level
            elif m == "inline":
                pass
        return " ".join(java_mods)

    def gen_method(self, node):
        return_type = self.convert_type(node["return_type"])
        mods = self._java_modifiers(node.get("modifiers", []))

        # C++ main → Java main
        self._in_main = (node["name"] == "main")  # ← track whether we're in main

        if node["name"] == "main":
            self.code_lines.append(
                f"{self.indent()}public static void main(String[] args) {{"
            )
            self.indent_level += 1
            for stmt in node["body"]:
                self.gen_statement(stmt)
            self.indent_level -= 1
            self.code_lines.append(f"{self.indent()}}}")
            self._in_main = False
            return

        # Build parameter list
        params = []
        for p in node["parameters"]:
            java_type = self.convert_type(p["type"])
            params.append(f"{java_type} {p['name']}")
        params_str = ", ".join(params)

        mod_str = (mods + " ") if mods else "public "
        self.code_lines.append(f"{self.indent()}{mod_str}{return_type} {node['name']}({params_str}) {{")
        self.indent_level += 1
        for stmt in node["body"]:
            self.gen_statement(stmt)
        self.indent_level -= 1
        self.code_lines.append(f"{self.indent()}}}")

    def _gen_main_wrapper(self, tree):
        self.code_lines.append(f"{self.indent()}public static void main(String[] args) {{")
        self.indent_level += 1
        for node in tree["body"]:
            if node["type"] not in ("MethodDeclaration", "FieldDeclaration"):
                self.gen_statement(node)
        self.indent_level -= 1
        self.code_lines.append(f"{self.indent()}}}")


    # Statements
    def gen_statement(self, stmt):
        if stmt is None:
            return
        t = stmt["type"]

        if t == "Declaration":
            self.gen_declaration(stmt)
        elif t == "MultiDeclaration":
            self.gen_multi_declaration(stmt)
        elif t == "CompoundAssignment":
            self.gen_compound_assignment(stmt)
        elif t == "Assignment":
            self.gen_assignment(stmt)
        elif t == "If":
            self.gen_if(stmt)
        elif t == "For":
            self.gen_for(stmt)
        elif t == "While":
            self.gen_while(stmt)
        elif t == "DoWhile":
            self.gen_do_while(stmt)
        elif t == "Switch":
            self.gen_switch(stmt)
        elif t == "Break":
            self.code_lines.append(f"{self.indent()}break;")
        elif t == "Continue":
            self.code_lines.append(f"{self.indent()}continue;")
        elif t == "Return":
            self.gen_return(stmt)
        elif t == "Print":
            self.gen_print(stmt)
        elif t == "Input":
            self.gen_input(stmt)
        elif t == "FunctionCall":
            self.gen_function_call_stmt(stmt)
        elif t == "Block":
            self.gen_block(stmt)
        elif t == "Unary":
            expr = self.gen_expression(stmt)
            self.code_lines.append(f"{self.indent()}{expr};")
        elif t == "Expression":
            pass

    def gen_declaration(self, stmt):
        java_type = self.convert_type(stmt["data_type"])
        if "initializer" in stmt:
            init = self.gen_expression(stmt["initializer"])
            # Re-add 'f' suffix for float literals so Java doesn't widen to double
            if java_type == "float" and self._is_plain_number(init):
                init = f"{init}f"
            self.code_lines.append(f"{self.indent()}{java_type} {stmt['name']} = {init};")
        else:
            self.code_lines.append(f"{self.indent()}{java_type} {stmt['name']};")

    def gen_multi_declaration(self, stmt):

        declarations = stmt["declarations"]

        java_type = self.convert_type(
            declarations[0]["data_type"]
        )

        parts = []

        for decl in declarations:

            text = decl["name"]

            if "initializer" in decl:

                init = self.gen_expression(
                    decl["initializer"]
                )

                if java_type == "float" and self._is_plain_number(init):
                    init += "f"

                text += f" = {init}"

            parts.append(text)

        joined = ", ".join(parts)

        self.code_lines.append(
            f"{self.indent()}{java_type} {joined};"
        )

    def gen_compound_assignment(self, stmt):
        right = self.gen_expression(stmt["right"])

        self.code_lines.append(
            f"{self.indent()}{stmt['left']} {stmt['operator']} {right};"
        )

    def _is_plain_number(self, value):
        """True if value is a numeric literal without an existing suffix."""
        try:
            float(value)
            return not value.endswith(('f', 'F', 'L', 'd', 'D'))
        except ValueError:
            return False

    def gen_assignment(self, stmt):
        right = self.gen_expression(stmt["right"])
        self.code_lines.append(f"{self.indent()}{stmt['left']} = {right};")

    def gen_if_inline(self, stmt):
        cond = self.gen_expression(stmt["condition"])

        self.code_lines.append(
            f"{self.indent()}if ({cond}) {{"
        )

        self.indent_level += 1

        for s in stmt["then"]:
            self.gen_statement(s)

        self.indent_level -= 1

        self.code_lines.append(f"{self.indent()}}}")

    def gen_if(self, stmt):
        cond = self.gen_expression(stmt["condition"])
        self.code_lines.append(f"{self.indent()}if ({cond}) {{")
        self.indent_level += 1
        for s in stmt["then"]:
            self.gen_statement(s)
        self.indent_level -= 1
        if stmt.get("else"):
            if (
                len(stmt["else"]) == 1 and
                stmt["else"][0]["type"] == "If"
            ):

                nested = stmt["else"][0]

                nested_cond = self.gen_expression(
                    nested["condition"]
                )

                self.code_lines.append(
                    f"{self.indent()}}} else if ({nested_cond}) {{"
                )

                self.indent_level += 1

                for s in nested["then"]:
                    self.gen_statement(s)

                self.indent_level -= 1

                if nested.get("else"):

                    self.code_lines.append(
                        f"{self.indent()}}} else {{"
                    )

                    self.indent_level += 1

                    for s in nested["else"]:
                        self.gen_statement(s)

                    self.indent_level -= 1
        self.code_lines.append(f"{self.indent()}}}")

    def gen_for(self, stmt):
        init = ""
        if stmt["init"]:
            n = stmt["init"]
            if n["type"] == "Declaration":
                init = f"{self.convert_type(n['data_type'])} {n['name']}"
                if "initializer" in n:
                    init += f" = {self.gen_expression(n['initializer'])}"
            elif n["type"] == "MultiDeclaration":
                decls = n["declarations"]
                base  = self.convert_type(decls[0]["data_type"])
                parts = []
                for d in decls:
                    p = d["name"]
                    if "initializer" in d:
                        p += f" = {self.gen_expression(d['initializer'])}"
                    parts.append(p)
                init = f"{base} {', '.join(parts)}"
            else:
                init = self.gen_expression(n)

        cond   = self.gen_expression(stmt["condition"]) if stmt["condition"] else ""
        update = self.gen_expression(stmt["update"])    if stmt["update"]    else ""

        self.code_lines.append(f"{self.indent()}for ({init}; {cond}; {update}) {{")
        self.indent_level += 1
        for s in stmt["body"]:
            self.gen_statement(s)
        self.indent_level -= 1
        self.code_lines.append(f"{self.indent()}}}")

    def gen_while(self, stmt):
        cond = self.gen_expression(stmt["condition"])
        self.code_lines.append(f"{self.indent()}while ({cond}) {{")
        self.indent_level += 1
        for s in stmt["body"]:
            self.gen_statement(s)
        self.indent_level -= 1
        self.code_lines.append(f"{self.indent()}}}")

    def gen_do_while(self, stmt):
        self.code_lines.append(f"{self.indent()}do {{")
        self.indent_level += 1
        for s in stmt["body"]:
            self.gen_statement(s)
        self.indent_level -= 1
        cond = self.gen_expression(stmt["condition"])
        self.code_lines.append(f"{self.indent()}}} while ({cond});")

    def gen_switch(self, stmt):
        expr = self.gen_expression(stmt["expression"])
        self.code_lines.append(f"{self.indent()}switch ({expr}) {{")
        self.indent_level += 1
        for case in stmt["cases"]:
            val = self.gen_expression(case["value"])
            self.code_lines.append(f"{self.indent()}case {val}:")
            self.indent_level += 1
            for s in case["body"]:
                self.gen_statement(s)
            self.indent_level -= 1
        if stmt["default"] is not None:
            self.code_lines.append(f"{self.indent()}default:")
            self.indent_level += 1
            for s in stmt["default"]:
                self.gen_statement(s)
            self.indent_level -= 1
        self.indent_level -= 1
        self.code_lines.append(f"{self.indent()}}}")

    def gen_return(self, stmt):
        if self._in_main:
            return
        if stmt["value"]:
            val = self.gen_expression(stmt["value"])
            self.code_lines.append(f"{self.indent()}return {val};")
        else:
            self.code_lines.append(f"{self.indent()}return;")

    def gen_print(self, stmt):

        expr = stmt["value"]

        if self.is_string_concat(expr):

            parts = self.flatten_concat(expr)

            output = " + ".join(parts)

        else:

            output = self.gen_expression(expr)

        method = "println" if stmt["newline"] else "print"

        self.code_lines.append(
            f"{self.indent()}System.out.{method}({output});"
        )
    
    def is_string_concat(self, expr):

        if expr["type"] == "Literal":

            return expr.get("value_type") == "string"

        if expr["type"] == "Binary" and expr["operator"] == "+":

            return (
                self.is_string_concat(expr["left"]) or
                self.is_string_concat(expr["right"])
            )

        return False


    def flatten_concat(self, expr):

        if expr["type"] == "Binary" and expr["operator"] == "+":

            return (
                self.flatten_concat(expr["left"]) +
                self.flatten_concat(expr["right"])
            )

        return [self.gen_expression(expr)]

    def gen_function_call_stmt(self, stmt):
        args = [self.gen_expression(a) for a in stmt["arguments"]]
        java_name = stmt["name"].replace("::", ".")   # ← add this
        self.code_lines.append(f"{self.indent()}{java_name}({', '.join(args)});")

    def gen_block(self, stmt):
        self.code_lines.append(f"{self.indent()}{{")
        self.indent_level += 1
        for s in stmt.get("statements", []):
            self.gen_statement(s)
        self.indent_level -= 1
        self.code_lines.append(f"{self.indent()}}}")


    # Expressions
    def gen_expression(self, expr):
        t = expr["type"]

        if t == "Literal":
            val = expr["value"]
            if val == "nullptr":
                return "null"
            # Strip f suffix from float literals
            if isinstance(val, str) and val.endswith("f"):
                return val[:-1]
            return val

        elif t == "Identifier":
            return expr["name"]

        elif t == "Unary":
            operand = self.gen_expression(expr["operand"])
            op = expr["operator"]
            if expr.get("prefix", True):
                return f"{op}{operand}"
            else:
                return f"{operand}{op}"

        elif t == "Binary":
            left  = self.gen_expression(expr["left"])
            right = self.gen_expression(expr["right"])
            return f"{left} {expr['operator']} {right}"

        elif t == "Ternary":
            cond = self.gen_expression(expr["condition"])
            then = self.gen_expression(expr["then"])
            els  = self.gen_expression(expr["else"])
            return f"{cond} ? {then} : {els}"

        elif t == "FunctionCall":
            args = [self.gen_expression(a) for a in expr["arguments"]]
            # Convert C++ scoped call TestAll::add → TestAll.add
            java_name = expr["name"].replace("::", ".")
            return f"{java_name}({', '.join(args)})"

        elif t == "MethodCall":
            args = [self.gen_expression(a) for a in expr["arguments"]]
            return f"{expr['object']}.{expr['method']}({', '.join(args)})"

        elif t == "MemberAccess":
            return f"{expr['object']}.{expr['member']}"

        return ""


    # Type mapping  C++ → Java
    def convert_type(self, cpp_type):
        type_map = {
            "int":      "int",
            "int32_t":  "int",
            "uint32_t": "int",
            "short":    "short",
            "int16_t":  "short",
            "long":     "long",
            "int64_t":  "long",
            "uint64_t": "long",
            "float":    "float",
            "double":   "double",
            "char":     "char",
            "int8_t":   "byte",
            "uint8_t":  "byte",
            "bool":     "boolean",
            "string":   "String",
            "void":     "void",
            "auto":     "var",
            "int*":     "int[]",
            "char*":    "String",
            "double*":  "double[]",
            "float*":   "float[]",
        }
        return type_map.get(cpp_type, cpp_type)
