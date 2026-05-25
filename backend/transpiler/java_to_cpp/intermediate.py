import json
from ..config import OUTPUT_DIR

class TACGenerator:
    def __init__(self):
        self.temp_count = 1
        self.label_count = 1
        self.code = []
        self.loop_stack = []
    
    def new_temp(self):
        temp = f"t{self.temp_count}"
        self.temp_count += 1
        return temp
    
    def new_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label
    
    def generate(self, node):
        return self.gen_node(node)
    
    def gen_node(self, node):
        if node is None:
            return ""
        
        node_type = node["type"]
        
        if node_type == "Program":
            for stmt in node["body"]:
                self.gen_node(stmt)
        
        elif node_type == "MethodDeclaration":
            self.code.append(f"func_{node['name']}:")
            for param in node["parameters"]:
                self.code.append(f"param {param['name']}")
            for stmt in node["body"]:
                self.gen_node(stmt)
            self.code.append("endfunc")
        
        elif node_type == "Declaration":
            if "initializer" in node:
                result = self.gen_expression(node["initializer"])
                self.code.append(f"{node['name']} = {result}")
        
        elif node_type == "MultiDeclaration":
            for decl in node["declarations"]:
                self.gen_node(decl)
        
        elif node_type == "Assignment":
            result = self.gen_expression(node["right"])
            self.code.append(f"{node['left']} = {result}")
        
        elif node_type == "If":
            else_label = self.new_label()
            end_label = self.new_label()
            
            condition = self.gen_expression(node["condition"])
            self.code.append(f"if not {condition} goto {else_label}")
            
            for stmt in node["then"]:
                self.gen_node(stmt)
            self.code.append(f"goto {end_label}")
            
            self.code.append(f"{else_label}:")
            if node.get("else"):
                for stmt in node["else"]:
                    self.gen_node(stmt)
            
            self.code.append(f"{end_label}:")
        
        elif node_type == "For":
            start_label = self.new_label()
            continue_label = self.new_label()
            end_label = self.new_label()
            
            if node["init"]:
                self.gen_node(node["init"])
            
            self.code.append(f"{start_label}:")
            
            if node["condition"]:
                condition = self.gen_expression(node["condition"])
                self.code.append(f"if not {condition} goto {end_label}")
            
            self.loop_stack.append((continue_label, end_label))
            for stmt in node["body"]:
                self.gen_node(stmt)
            self.loop_stack.pop()
            
            self.code.append(f"{continue_label}:")
            if node["update"]:
                self.gen_expression(node["update"])
            
            self.code.append(f"goto {start_label}")
            self.code.append(f"{end_label}:")
        
        elif node_type == "While":
            start_label = self.new_label()
            end_label = self.new_label()
            
            self.code.append(f"{start_label}:")
            condition = self.gen_expression(node["condition"])
            self.code.append(f"if not {condition} goto {end_label}")
            
            self.loop_stack.append((start_label, end_label))
            for stmt in node["body"]:
                self.gen_node(stmt)
            self.loop_stack.pop()
            
            self.code.append(f"goto {start_label}")
            self.code.append(f"{end_label}:")
        
        elif node_type == "DoWhile":
            start_label = self.new_label()
            continue_label = self.new_label()
            end_label = self.new_label()
            
            self.code.append(f"{start_label}:")
            self.loop_stack.append((continue_label, end_label))
            for stmt in node["body"]:
                self.gen_node(stmt)
            self.loop_stack.pop()
            
            self.code.append(f"{continue_label}:")
            condition = self.gen_expression(node["condition"])
            self.code.append(f"if {condition} goto {start_label}")
            self.code.append(f"{end_label}:")
        
        elif node_type == "Switch":
            end_label = self.new_label()
            case_labels = [self.new_label() for _ in node["cases"]]
            default_label = self.new_label() if node["default"] else end_label
            
            expr_val = self.gen_expression(node["expression"])
            
            # Generate comparisons for each case
            for i, case in enumerate(node["cases"]):
                case_val = self.gen_expression(case["value"])
                temp = self.new_temp()
                self.code.append(f"{temp} = {expr_val} == {case_val}")
                self.code.append(f"if {temp} goto {case_labels[i]}")
            
            self.code.append(f"goto {default_label}")
            
            # Generate case bodies
            self.loop_stack.append((end_label, end_label))  # For break
            for i, case in enumerate(node["cases"]):
                self.code.append(f"{case_labels[i]}:")
                for stmt in case["body"]:
                    self.gen_node(stmt)
            
            if node["default"]:
                self.code.append(f"{default_label}:")
                for stmt in node["default"]:
                    self.gen_node(stmt)
            
            self.loop_stack.pop()
            self.code.append(f"{end_label}:")
        
        elif node_type == "Break":
            if self.loop_stack:
                _, end_label = self.loop_stack[-1]
                self.code.append(f"goto {end_label}")
        
        elif node_type == "Continue":
            if self.loop_stack:
                continue_label, _ = self.loop_stack[-1]
                self.code.append(f"goto {continue_label}")
        
        elif node_type == "Print":
            value = self.gen_expression(node["value"])
            self.code.append(f"print {value}")
        
        elif node_type == "FunctionCall":
            args = [self.gen_expression(arg) for arg in node["arguments"]]
            args_str = ", ".join(args)
            self.code.append(f"call {node['name']}({args_str})")
        
        elif node_type == "Unary":
            self.gen_expression(node)
        
        elif node_type == "Return":
            if node["value"]:
                value = self.gen_expression(node["value"])
                self.code.append(f"return {value}")
            else:
                self.code.append("return")
        
        return "\n".join(self.code)
    
    def gen_expression(self, expr):
        expr_type = expr["type"]
        
        if expr_type == "Literal":
            return expr["value"]
        
        elif expr_type == "Identifier":
            return expr["name"]

        elif expr_type == "Unary":
            operand = self.gen_expression(expr["operand"])
            result = self.new_temp()
            op = expr["operator"]
            if expr.get("prefix", True):
                self.code.append(f"{result} = {op}{operand}")
            else:
                self.code.append(f"{result} = {operand}{op}")
            return result
        
        elif expr_type == "Binary":
            left = self.gen_expression(expr["left"])
            right = self.gen_expression(expr["right"])
            result = self.new_temp()
            self.code.append(f"{result} = {left} {expr['operator']} {right}")
            return result
        
        elif expr_type == "Ternary":
            cond = self.gen_expression(expr["condition"])
            result = self.new_temp()
            true_label = self.new_label()
            end_label = self.new_label()
            self.code.append(f"if {cond} goto {true_label}")
            false_val = self.gen_expression(expr["else"])
            self.code.append(f"{result} = {false_val}")
            self.code.append(f"goto {end_label}")
            self.code.append(f"{true_label}:")
            true_val = self.gen_expression(expr["then"])
            self.code.append(f"{result} = {true_val}")
            self.code.append(f"{end_label}:")
            return result
        
        elif expr_type == "FunctionCall":
            args = [self.gen_expression(arg) for arg in expr["arguments"]]
            args_str = ", ".join(args)
            result = self.new_temp()
            self.code.append(f"{result} = call {expr['name']}({args_str})")
            return result
        
        return ""


def intermediate_code_generator(tree):
    generator = TACGenerator()
    generator.generate(tree)
    
    ir = {
        "three_address_code": generator.code
    }
    
    with open(f"{OUTPUT_DIR}/intermediate.json", "w") as file:
        json.dump(ir, file, indent=4)
    
    return ir
