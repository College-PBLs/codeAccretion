import json
from ..config import OUTPUT_DIR

class SemanticAnalyzer:
    def __init__(self, tree):
        self.tree = tree
        self.symbol_table = {}
        self.current_scope = "global"
        self.scopes = [{"name": "global", "symbols": {}}]
        self.errors = []
        self.functions = {}
    
    def is_symbol_declared(self, name):
        """Walk all scopes from innermost to outermost."""
        for scope in reversed(self.scopes):
            if name in scope["symbols"]:
                return True
        return False

    def analyze(self):
        for func in self.tree.get("functions", []):
            self.functions[func["name"]] = func
        
        self.analyze_body(self.tree["body"])
        
        return {
            "status": "Passed" if len(self.errors) == 0 else "Failed",
            "symbol_table": self.symbol_table,
            "functions": self.functions,
            "errors": self.errors
        }
    
    def analyze_body(self, body):
        for node in body:
            self.analyze_node(node)
    
    def analyze_node(self, node):
        if node is None:
            return
        
        node_type = node["type"]
        
        if node_type == "Declaration":
            self.analyze_declaration(node)
        elif node_type == "MultiDeclaration":
            for decl in node["declarations"]:
                self.analyze_declaration(decl)
        elif node_type == "Assignment":
            self.analyze_assignment(node)
        elif node_type == "If":
            self.analyze_if(node)
        elif node_type == "For":
            self.analyze_for(node)
        elif node_type == "While":
            self.analyze_while(node)
        elif node_type == "DoWhile":
            self.analyze_do_while(node)
        elif node_type == "Switch":
            self.analyze_switch(node)
        elif node_type in ["Break", "Continue"]:
            pass  # Valid in loop context
        elif node_type == "Return":
            self.analyze_return(node)
        elif node_type == "Print":
            self.analyze_print(node)
        elif node_type == "Unary":
            self.analyze_expression(node["operand"])
        elif node_type == "FunctionCall":
            self.analyze_function_call(node)
        elif node_type == "MethodDeclaration":
            self.analyze_method_declaration(node)
        elif node_type == "FieldDeclaration":
            self.analyze_field_declaration(node)
        elif node_type == "Block":
            self.analyze_block(node)
        elif node_type == "Expression":
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
        for stmt in node["then"]:
            self.analyze_node(stmt)
        self.pop_scope()
        
        if node.get("else"):
            self.push_scope()
            for stmt in node["else"]:
                self.analyze_node(stmt)
            self.pop_scope()
    
    def analyze_for(self, node):
        self.push_scope()
        
        if node["init"]:
            self.analyze_node(node["init"])
        if node["condition"]:
            self.analyze_expression(node["condition"])
        if node["update"]:
            self.analyze_expression(node["update"])
        
        for stmt in node["body"]:
            self.analyze_node(stmt)
        
        self.pop_scope()
    
    def analyze_while(self, node):
        self.analyze_expression(node["condition"])
        self.push_scope()
        for stmt in node["body"]:
            self.analyze_node(stmt)
        self.pop_scope()
    
    def analyze_do_while(self, node):
        self.push_scope()
        for stmt in node["body"]:
            self.analyze_node(stmt)
        self.pop_scope()
        self.analyze_expression(node["condition"])
    
    def analyze_switch(self, node):
        self.analyze_expression(node["expression"])
        for case in node["cases"]:
            self.analyze_expression(case["value"])
            self.push_scope()
            for stmt in case["body"]:
                self.analyze_node(stmt)
            self.pop_scope()
        if node["default"]:
            self.push_scope()
            for stmt in node["default"]:
                self.analyze_node(stmt)
            self.pop_scope()
    
    def analyze_return(self, node):
        if node["value"]:
            self.analyze_expression(node["value"])
    
    def analyze_print(self, node):
        self.analyze_expression(node["value"])
    
    def analyze_function_call(self, node):
        if node["name"] not in self.functions:
            self.errors.append(f"Function '{node['name']}' not declared")
        else:
            expected_params = len(self.functions[node["name"]].get("parameters", []))
            actual_params = len(node["arguments"])
            if expected_params != actual_params:
                self.errors.append(f"Function '{node['name']}' expects {expected_params} arguments, got {actual_params}")
            
            for arg in node["arguments"]:
                self.analyze_expression(arg)
    
    def analyze_method_declaration(self, node):
        self.push_scope(f"function:{node['name']}")
        
        for param in node["parameters"]:
            self.add_symbol(param["name"], param["type"])
        
        for stmt in node["body"]:
            self.analyze_node(stmt)
        
        self.pop_scope()
    
    def analyze_field_declaration(self, node):
        if node["name"] in self.get_current_scope_symbols():
            self.errors.append(f"Field '{node['name']}' already declared")
        else:
            self.add_symbol(node["name"], node["data_type"])
    
    def analyze_block(self, node):
        self.push_scope()
        for stmt in node.get("statements", []):
            self.analyze_node(stmt)
        self.pop_scope()
    
    def analyze_expression(self, expr):
        if expr is None:
            return
        
        expr_type = expr["type"]
        
        if expr_type == "Binary":
            self.analyze_expression(expr["left"])
            self.analyze_expression(expr["right"])
        elif expr_type == "Unary":
            self.analyze_expression(expr["operand"])
        elif expr_type == "Ternary":
            self.analyze_expression(expr["condition"])
            self.analyze_expression(expr["then"])
            self.analyze_expression(expr["else"])
        elif expr_type == "Identifier":
            if not self.is_symbol_declared(expr["name"]):
                self.errors.append(f"Variable '{expr['name']}' not declared")
        elif expr_type == "FunctionCall":
            self.analyze_function_call(expr)
        # Literals (number, string, char, boolean) don't need checking
    
    def get_current_scope_symbols(self):
        if self.scopes:
            return self.scopes[-1]["symbols"]
        return {}
    
    def add_symbol(self, name, type_info):
        if self.scopes:
            self.scopes[-1]["symbols"][name] = type_info
            self.symbol_table[name] = type_info
    
    def push_scope(self, name=None):
        if name is None:
            name = f"scope_{len(self.scopes)}"
        self.scopes.append({"name": name, "symbols": {}})
    
    def pop_scope(self):
        if len(self.scopes) > 1:
            self.scopes.pop()


def semantic_analyzer(tree):
    analyzer = SemanticAnalyzer(tree)
    result = analyzer.analyze()
    
    with open(f"{OUTPUT_DIR}/semantic.json", "w") as file:
        json.dump(result, file, indent=4)
    
    return result
