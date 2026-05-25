import json
from ..config import OUTPUT_DIR

class TACGenerator:
    def __init__(self):
        self.temp_count = 1
        self.label_count = 1
        self.code = []
        self.loop_stack = []

    def new_temp(self):
        t = f"t{self.temp_count}"
        self.temp_count += 1
        return t

    def new_label(self):
        l = f"L{self.label_count}"
        self.label_count += 1
        return l

    def generate(self, node):
        return self.gen_node(node)

    def gen_node(self, node):
        if node is None:
            return ""
        t = node["type"]

        if t == "Program":
            for stmt in node["body"]:
                self.gen_node(stmt)

        elif t == "MethodDeclaration":
            self.code.append(f"func_{node['name']}:")
            for p in node["parameters"]:
                self.code.append(f"param {p['name']}")
            for stmt in node["body"]:
                self.gen_node(stmt)
            self.code.append("endfunc")

        elif t == "Declaration":
            if "initializer" in node:
                r = self.gen_expression(node["initializer"])
                self.code.append(f"{node['name']} = {r}")

        elif t == "MultiDeclaration":
            for d in node["declarations"]:
                self.gen_node(d)

        elif t == "Assignment":
            r = self.gen_expression(node["right"])
            self.code.append(f"{node['left']} = {r}")

        elif t == "If":
            else_lbl = self.new_label()
            end_lbl  = self.new_label()
            cond = self.gen_expression(node["condition"])
            self.code.append(f"if not {cond} goto {else_lbl}")
            for s in node["then"]:
                self.gen_node(s)
            self.code.append(f"goto {end_lbl}")
            self.code.append(f"{else_lbl}:")
            if node.get("else"):
                for s in node["else"]:
                    self.gen_node(s)
            self.code.append(f"{end_lbl}:")

        elif t == "For":
            start_lbl = self.new_label()
            cont_lbl  = self.new_label()
            end_lbl   = self.new_label()
            if node["init"]:
                self.gen_node(node["init"])
            self.code.append(f"{start_lbl}:")
            if node["condition"]:
                cond = self.gen_expression(node["condition"])
                self.code.append(f"if not {cond} goto {end_lbl}")
            self.loop_stack.append((cont_lbl, end_lbl))
            for s in node["body"]:
                self.gen_node(s)
            self.loop_stack.pop()
            self.code.append(f"{cont_lbl}:")
            if node["update"]:
                self.gen_expression(node["update"])
            self.code.append(f"goto {start_lbl}")
            self.code.append(f"{end_lbl}:")

        elif t == "While":
            start_lbl = self.new_label()
            end_lbl   = self.new_label()
            self.code.append(f"{start_lbl}:")
            cond = self.gen_expression(node["condition"])
            self.code.append(f"if not {cond} goto {end_lbl}")
            self.loop_stack.append((start_lbl, end_lbl))
            for s in node["body"]:
                self.gen_node(s)
            self.loop_stack.pop()
            self.code.append(f"goto {start_lbl}")
            self.code.append(f"{end_lbl}:")

        elif t == "DoWhile":
            start_lbl = self.new_label()
            cont_lbl  = self.new_label()
            end_lbl   = self.new_label()
            self.code.append(f"{start_lbl}:")
            self.loop_stack.append((cont_lbl, end_lbl))
            for s in node["body"]:
                self.gen_node(s)
            self.loop_stack.pop()
            self.code.append(f"{cont_lbl}:")
            cond = self.gen_expression(node["condition"])
            self.code.append(f"if {cond} goto {start_lbl}")
            self.code.append(f"{end_lbl}:")

        elif t == "Switch":
            end_lbl    = self.new_label()
            case_lbls  = [self.new_label() for _ in node["cases"]]
            def_lbl    = self.new_label() if node["default"] else end_lbl
            expr_val   = self.gen_expression(node["expression"])
            for i, case in enumerate(node["cases"]):
                case_val = self.gen_expression(case["value"])
                tmp = self.new_temp()
                self.code.append(f"{tmp} = {expr_val} == {case_val}")
                self.code.append(f"if {tmp} goto {case_lbls[i]}")
            self.code.append(f"goto {def_lbl}")
            self.loop_stack.append((end_lbl, end_lbl))
            for i, case in enumerate(node["cases"]):
                self.code.append(f"{case_lbls[i]}:")
                for s in case["body"]:
                    self.gen_node(s)
            if node["default"]:
                self.code.append(f"{def_lbl}:")
                for s in node["default"]:
                    self.gen_node(s)
            self.loop_stack.pop()
            self.code.append(f"{end_lbl}:")

        elif t == "Break":
            if self.loop_stack:
                _, end_lbl = self.loop_stack[-1]
                self.code.append(f"goto {end_lbl}")

        elif t == "Continue":
            if self.loop_stack:
                cont_lbl, _ = self.loop_stack[-1]
                self.code.append(f"goto {cont_lbl}")

        elif t == "Print":
            val = self.gen_expression(node["value"])
            self.code.append(f"print {val}")

        elif t == "Input":
            for var in node["variables"]:
                self.code.append(f"input {var}")

        elif t == "FunctionCall":
            args_str = ", ".join(self.gen_expression(a) for a in node["arguments"])
            self.code.append(f"call {node['name']}({args_str})")

        elif t == "Unary":
            self.gen_expression(node)

        elif t == "Return":
            if node["value"]:
                val = self.gen_expression(node["value"])
                self.code.append(f"return {val}")
            else:
                self.code.append("return")

        return "\n".join(self.code)

    def gen_expression(self, expr):
        t = expr["type"]

        if t == "Literal":
            return expr["value"]

        elif t == "Identifier":
            return expr["name"]

        elif t == "Unary":
            operand = self.gen_expression(expr["operand"])
            result  = self.new_temp()
            op = expr["operator"]
            if expr.get("prefix", True):
                self.code.append(f"{result} = {op}{operand}")
            else:
                self.code.append(f"{result} = {operand}{op}")
            return result

        elif t == "Binary":
            left  = self.gen_expression(expr["left"])
            right = self.gen_expression(expr["right"])
            result = self.new_temp()
            self.code.append(f"{result} = {left} {expr['operator']} {right}")
            return result

        elif t == "Ternary":
            cond = self.gen_expression(expr["condition"])
            result   = self.new_temp()
            true_lbl = self.new_label()
            end_lbl  = self.new_label()
            self.code.append(f"if {cond} goto {true_lbl}")
            false_val = self.gen_expression(expr["else"])
            self.code.append(f"{result} = {false_val}")
            self.code.append(f"goto {end_lbl}")
            self.code.append(f"{true_lbl}:")
            true_val = self.gen_expression(expr["then"])
            self.code.append(f"{result} = {true_val}")
            self.code.append(f"{end_lbl}:")
            return result

        elif t == "PrintChain":
            parts = [
                self.gen_expression(p)
                for p in expr["parts"]
            ]

            return " + ".join(parts)

        elif t == "FunctionCall":
            args_str = ", ".join(self.gen_expression(a) for a in expr["arguments"])
            result = self.new_temp()
            self.code.append(f"{result} = call {expr['name']}({args_str})")
            return result

        elif t in ("MethodCall", "MemberAccess"):
            result = self.new_temp()
            self.code.append(f"{result} = {expr.get('object', '')}.{expr.get('method', expr.get('member', ''))}")
            return result

        return ""


def intermediate_code_generator(tree):
    generator = TACGenerator()
    generator.generate(tree)

    ir = {"three_address_code": generator.code}

    with open(f"{OUTPUT_DIR}/intermediate.json", "w") as f:
        json.dump(ir, f, indent=4)

    return ir
