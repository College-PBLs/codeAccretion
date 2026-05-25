import json
from ..config import OUTPUT_DIR

class SemanticAnalyzer:
    def __init__(self, tree):
        self.tree = tree
        self.symbol_table = {}
        self.scopes = [{"name": "global", "symbols": {}}]
        self.errors = []
        self.functions = {}

    def is_symbol_declared(self, name):
        for scope in reversed(self.scopes):
            if name in scope["symbols"]:
                return True
        return False

    def analyze(self):
        for func in self.tree.get("functions", []):
            self.functions[func["name"]] = func

        self.analyze_body(self.tree["body"])

        return {
            "status": "Passed" if not self.errors else "Failed",
            "symbol_table": self.symbol_table,
            "functions": self.functions,
            "errors": self.errors,
        }

    def analyze_body(self, body):
        for node in body:
            self.analyze_node(node)

    def analyze_node(self, node):
        if node is None:
            return
        t = node["type"]
        if t == "Declaration":
            self.analyze_declaration(node)
        elif t == "MultiDeclaration":
            for d in node["declarations"]:
                self.analyze_declaration(d)
        elif t == "Assignment":
            self.analyze_assignment(node)
        elif t == "If":
            self.analyze_if(node)
        elif t == "For":
            self.analyze_for(node)
        elif t == "While":
            self.analyze_while(node)
        elif t == "DoWhile":
            self.analyze_do_while(node)
        elif t == "Switch":
            self.analyze_switch(node)
        elif t in ("Break", "Continue"):
            pass
        elif t == "Return":
            self.analyze_return(node)
        elif t == "Print":
            self.analyze_print(node)
        elif t == "Input":
            pass
        elif t == "Unary":
            self.analyze_expression(node["operand"])
        elif t == "FunctionCall":
            self.analyze_function_call(node)
        elif t == "MethodDeclaration":
            self.analyze_method_declaration(node)
        elif t == "FieldDeclaration":
            self.analyze_field_declaration(node)
        elif t == "Block":
            self.analyze_block(node)
        elif t == "Expression":
            pass

    def analyze_declaration(self, node):
        name = node["name"]
        if name in self.get_current_scope_symbols():
            self.errors.append(f"Variable '{name}' already declared in this scope")
        else:
            self.add_symbol(name, node["data_type"])
            if "initializer" in node:
                self.analyze_expression(node["initializer"])

    def analyze_assignment(self, node):
        if not self.is_symbol_declared(node["left"]):
            self.errors.append(f"Variable '{node['left']}' not declared")
        else:
            self.analyze_expression(node["right"])

    def analyze_if(self, node):
        self.analyze_expression(node["condition"])
        self.push_scope()
        for s in node["then"]:
            self.analyze_node(s)
        self.pop_scope()
        if node.get("else"):
            self.push_scope()
            for s in node["else"]:
                self.analyze_node(s)
            self.pop_scope()

    def analyze_for(self, node):
        self.push_scope()
        if node["init"]:
            self.analyze_node(node["init"])
        if node["condition"]:
            self.analyze_expression(node["condition"])
        if node["update"]:
            self.analyze_expression(node["update"])
        for s in node["body"]:
            self.analyze_node(s)
        self.pop_scope()

    def analyze_while(self, node):
        self.analyze_expression(node["condition"])
        self.push_scope()
        for s in node["body"]:
            self.analyze_node(s)
        self.pop_scope()

    def analyze_do_while(self, node):
        self.push_scope()
        for s in node["body"]:
            self.analyze_node(s)
        self.pop_scope()
        self.analyze_expression(node["condition"])

    def analyze_switch(self, node):
        self.analyze_expression(node["expression"])
        for case in node["cases"]:
            self.analyze_expression(case["value"])
            self.push_scope()
            for s in case["body"]:
                self.analyze_node(s)
            self.pop_scope()
        if node["default"]:
            self.push_scope()
            for s in node["default"]:
                self.analyze_node(s)
            self.pop_scope()

    def analyze_return(self, node):
        if node["value"]:
            self.analyze_expression(node["value"])

    def analyze_print(self, node):
        self.analyze_expression(node["value"])

    def analyze_function_call(self, node):
        raw_name = node["name"]
        name = raw_name.split("::")[-1]   # ← strip class/namespace prefix

        if name not in self.functions:
            self.errors.append(f"Function '{raw_name}' not declared")
        else:
            expected = len(self.functions[name].get("parameters", []))
            actual   = len(node["arguments"])
            if expected != actual:
                self.errors.append(
                    f"Function '{raw_name}' expects {expected} arguments, got {actual}"
                )
        for arg in node["arguments"]:
            self.analyze_expression(arg)

    def analyze_method_declaration(self, node):
        self.push_scope(f"function:{node['name']}")
        for param in node["parameters"]:
            self.add_symbol(param["name"], param["type"])
        for s in node["body"]:
            self.analyze_node(s)
        self.pop_scope()

    def analyze_field_declaration(self, node):
        if node["name"] in self.get_current_scope_symbols():
            self.errors.append(f"Field '{node['name']}' already declared")
        else:
            self.add_symbol(node["name"], node["data_type"])

    def analyze_block(self, node):
        self.push_scope()
        for s in node.get("statements", []):
            self.analyze_node(s)
        self.pop_scope()

    def analyze_expression(self, expr):
        if expr is None:
            return
        t = expr["type"]
        if t == "Binary":
            self.analyze_expression(expr["left"])
            self.analyze_expression(expr["right"])
        elif t == "Unary":
            self.analyze_expression(expr["operand"])
        elif t == "Ternary":
            self.analyze_expression(expr["condition"])
            self.analyze_expression(expr["then"])
            self.analyze_expression(expr["else"])
        elif t == "Identifier":
            if not self.is_symbol_declared(expr["name"]):
                self.errors.append(f"Variable '{expr['name']}' not declared")
        elif t == "FunctionCall":
            self.analyze_function_call(expr)
        elif t in ("MethodCall", "MemberAccess"):
            pass  # object-oriented access — not tracked at this level

    def get_current_scope_symbols(self):
        return self.scopes[-1]["symbols"] if self.scopes else {}

    def add_symbol(self, name, type_info):
        if self.scopes:
            self.scopes[-1]["symbols"][name] = type_info
            self.symbol_table[name] = type_info

    def push_scope(self, name=None):
        self.scopes.append({"name": name or f"scope_{len(self.scopes)}", "symbols": {}})

    def pop_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()


def semantic_analyzer(tree):
    analyzer = SemanticAnalyzer(tree)
    result = analyzer.analyze()

    with open(f"{OUTPUT_DIR}/semantic.json", "w") as f:
        json.dump(result, f, indent=4)

    return result
