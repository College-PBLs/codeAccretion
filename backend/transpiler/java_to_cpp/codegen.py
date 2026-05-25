class CppGenerator:
    def __init__(self):
        self.indent_level = 0
        self.code_lines = []
    
    def indent(self):
        return "    " * self.indent_level
    
    def generate(self, tree):
        self.code_lines = []
        
        # Add headers
        self.code_lines.append("#include <bits/stdc++.h>")
        self.code_lines.append("using namespace std;")
        self.code_lines.append("")
        
        # Generate functions
        for node in tree.get("functions", []):
            self.gen_function(node)
            self.code_lines.append("")
        
        # Generate main function if present
        if not any(f["name"] == "main" for f in tree.get("functions", [])):
            self.gen_main(tree)
        
        return "\n".join(self.code_lines)
    
    def gen_function(self, node):
        # Java's main becomes int main() in C++
        if node["name"] == "main":
            self.code_lines.append("int main() {")
            self.indent_level += 1
            for stmt in node["body"]:
                self.gen_statement(stmt)
            self.code_lines.append(f"{self.indent()}return 0;")
            self.indent_level -= 1
            self.code_lines.append("}")
            return

        return_type = self.convert_type(node["return_type"])
        params = []
        for param in node["parameters"]:
            param_type = self.convert_type(param["type"])
            params.append(f"{param_type} {param['name']}")

        params_str = ", ".join(params)
        self.code_lines.append(f"{return_type} {node['name']}({params_str}) {{")

        self.indent_level += 1
        for stmt in node["body"]:
            self.gen_statement(stmt)
        self.indent_level -= 1
        self.code_lines.append("}")
    
    def gen_main(self, tree):
        self.code_lines.append("int main() {")
        self.indent_level += 1
        
        for node in tree["body"]:
            if node["type"] not in ["MethodDeclaration", "FieldDeclaration"]:
                self.gen_statement(node)
        
        self.code_lines.append(f"{self.indent()}return 0;")
        self.indent_level -= 1
        self.code_lines.append("}")
    
    def gen_statement(self, stmt):
        if stmt is None:
            return

        stmt_type = stmt["type"]

        if stmt_type == "Declaration":
            self.gen_declaration(stmt)
        elif stmt_type == "MultiDeclaration":
            self.gen_multi_declaration(stmt)
        elif stmt_type == "Assignment":
            self.gen_assignment(stmt)
        elif stmt_type == "If":
            self.gen_if(stmt)
        elif stmt_type == "For":
            self.gen_for(stmt)
        elif stmt_type == "While":
            self.gen_while(stmt)
        elif stmt_type == "DoWhile":
            self.gen_do_while(stmt)
        elif stmt_type == "Switch":
            self.gen_switch(stmt)
        elif stmt_type == "Break":
            self.code_lines.append(f"{self.indent()}break;")
        elif stmt_type == "Continue":
            self.code_lines.append(f"{self.indent()}continue;")
        elif stmt_type == "Return":
            self.gen_return(stmt)
        elif stmt_type == "Print":
            self.gen_print(stmt)
        elif stmt_type == "FunctionCall":
            self.gen_function_call(stmt)
        elif stmt_type == "Block":
            self.gen_block(stmt)
        elif stmt_type == "Unary":
            expr = self.gen_expression(stmt)
            self.code_lines.append(f"{self.indent()}{expr};")
        elif stmt_type == "Expression":
            pass
    
    def gen_declaration(self, stmt):
        cpp_type = self.convert_type(stmt["data_type"])
        if "initializer" in stmt:
            init_expr = self.gen_expression(stmt["initializer"])
            self.code_lines.append(f"{self.indent()}{cpp_type} {stmt['name']} = {init_expr};")
        else:
            self.code_lines.append(f"{self.indent()}{cpp_type} {stmt['name']};")

    def gen_multi_declaration(self, stmt):
        declarations = stmt["declarations"]

        cpp_type = self.convert_type(
            declarations[0]["data_type"]
        )

        parts = []

        for decl in declarations:

            text = decl["name"]

            if "initializer" in decl:
                init_expr = self.gen_expression(
                    decl["initializer"]
                )

                text += f" = {init_expr}"

            parts.append(text)

        joined = ", ".join(parts)

        self.code_lines.append(
            f"{self.indent()}{cpp_type} {joined};"
        )
    
    def gen_assignment(self, stmt):
        right_expr = self.gen_expression(stmt["right"])
        self.code_lines.append(f"{self.indent()}{stmt['left']} = {right_expr};")
    
    def gen_if(self, stmt):
        condition = self.gen_expression(stmt["condition"])
        self.code_lines.append(f"{self.indent()}if ({condition}) {{")
        
        self.indent_level += 1
        for then_stmt in stmt["then"]:
            self.gen_statement(then_stmt)
        self.indent_level -= 1
        
        if stmt.get("else"):
            self.code_lines.append(f"{self.indent()}}} else {{")
            self.indent_level += 1
            for else_stmt in stmt["else"]:
                self.gen_statement(else_stmt)
            self.indent_level -= 1
            self.code_lines.append(f"{self.indent()}}}")
        else:
            self.code_lines.append(f"{self.indent()}}}")
    
    def gen_for(self, stmt):
        init = ""
        if stmt["init"]:
            init_node = stmt["init"]
            if init_node["type"] == "Declaration":
                init = f"{self.convert_type(init_node['data_type'])} {init_node['name']}"
                if "initializer" in init_node:
                    init += f" = {self.gen_expression(init_node['initializer'])}"
            elif init_node["type"] == "MultiDeclaration":
                # Handle multi-variable declaration in for loop
                decls = init_node["declarations"]
                base_type = self.convert_type(decls[0]["data_type"])
                parts = []
                for d in decls:
                    part = d["name"]
                    if "initializer" in d:
                        part += f" = {self.gen_expression(d['initializer'])}"
                    parts.append(part)
                init = f"{base_type} {', '.join(parts)}"
            else:
                init = self.gen_expression(init_node)
        
        condition = self.gen_expression(stmt["condition"]) if stmt["condition"] else ""
        update = self.gen_expression(stmt["update"]) if stmt["update"] else ""
        
        self.code_lines.append(f"{self.indent()}for ({init}; {condition}; {update}) {{")
        
        self.indent_level += 1
        for body_stmt in stmt["body"]:
            self.gen_statement(body_stmt)
        self.indent_level -= 1
        
        self.code_lines.append(f"{self.indent()}}}")
    
    def gen_while(self, stmt):
        condition = self.gen_expression(stmt["condition"])
        self.code_lines.append(f"{self.indent()}while ({condition}) {{")
        
        self.indent_level += 1
        for body_stmt in stmt["body"]:
            self.gen_statement(body_stmt)
        self.indent_level -= 1
        
        self.code_lines.append(f"{self.indent()}}}")
    
    def gen_do_while(self, stmt):
        self.code_lines.append(f"{self.indent()}do {{")
        
        self.indent_level += 1
        for body_stmt in stmt["body"]:
            self.gen_statement(body_stmt)
        self.indent_level -= 1
        
        condition = self.gen_expression(stmt["condition"])
        self.code_lines.append(f"{self.indent()}}} while ({condition});")
    
    def gen_switch(self, stmt):
        expr = self.gen_expression(stmt["expression"])
        self.code_lines.append(f"{self.indent()}switch ({expr}) {{")
        self.indent_level += 1
        
        for case in stmt["cases"]:
            value = self.gen_expression(case["value"])
            self.code_lines.append(f"{self.indent()}case {value}:")
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
        if stmt["value"]:
            value = self.gen_expression(stmt["value"])
            self.code_lines.append(f"{self.indent()}return {value};")
        else:
            self.code_lines.append(f"{self.indent()}return;")
    
    def gen_print(self, stmt):
        expr = stmt["value"]

        # If expression is string concatenation chain
        if self.is_string_concat(expr):

            parts = self.flatten_concat(expr)
            chain = " << ".join(parts)

        else:
            # Normal arithmetic / expression
            chain = self.gen_expression(expr)

        endl = " << endl" if stmt["newline"] else ""

        self.code_lines.append(
            f"{self.indent()}cout << {chain}{endl};"
        )


    def is_string_concat(self, expr):
        # String literal involved
        if expr["type"] == "Literal" and expr.get("value_type") == "string":
            return True

        # Recursive binary +
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
    
    def gen_function_call(self, stmt):
        args = [self.gen_expression(arg) for arg in stmt["arguments"]]
        args_str = ", ".join(args)
        self.code_lines.append(f"{self.indent()}{stmt['name']}({args_str});")
    
    def gen_block(self, stmt):
        self.code_lines.append(f"{self.indent()}{{")
        self.indent_level += 1
        for substmt in stmt.get("statements", []):
            self.gen_statement(substmt)
        self.indent_level -= 1
        self.code_lines.append(f"{self.indent()}}}")
    
    def gen_expression(self, expr):
        expr_type = expr["type"]
        
        if expr_type == "Literal":
            return expr["value"]
        
        elif expr_type == "Identifier":
            return expr["name"]
        
        elif expr_type == "Unary":
            operand = self.gen_expression(expr["operand"])
            op = expr["operator"]
            if expr.get("prefix", True):
                return f"{op}{operand}"
            else:
                return f"{operand}{op}"
        
        elif expr_type == "Binary":
            left = self.gen_expression(expr["left"])
            right = self.gen_expression(expr["right"])
            return f"{left} {expr['operator']} {right}"
        
        elif expr_type == "Ternary":
            cond = self.gen_expression(expr["condition"])
            then = self.gen_expression(expr["then"])
            els = self.gen_expression(expr["else"])
            return f"{cond} ? {then} : {els}"
        
        elif expr_type == "FunctionCall":
            args = [self.gen_expression(arg) for arg in expr["arguments"]]
            return f"{expr['name']}({', '.join(args)})"
        
        return ""
    
    def convert_type(self, java_type):
        type_map = {
            "int": "int",
            "float": "float",
            "double": "double",
            "char": "char",
            "boolean": "bool",
            "String": "string",
            "void": "void",
            "byte": "char",
            "short": "short",
            "long": "long"
        }
        return type_map.get(java_type, java_type)
