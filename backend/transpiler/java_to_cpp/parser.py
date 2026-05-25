import json
from ..config import OUTPUT_DIR

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = None
        self.ast = {"type": "Program", "body": [], "functions": [], "class_name": None}
        if tokens:
            self.current_token = tokens[0]
    
    def peek(self):
        return self.current_token
    
    def next_token(self):
        self.position += 1
        if self.position < len(self.tokens):
            self.current_token = self.tokens[self.position]
        else:
            self.current_token = None
        return self.current_token
    
    def match(self, expected_type=None, expected_value=None):
        if self.current_token is None:
            return False
        
        if expected_type and self.current_token["type"] != expected_type:
            return False
        
        if expected_value and self.current_token["value"] != expected_value:
            return False
        
        return True
    
    def consume(self, expected_type=None, expected_value=None):
        if self.match(expected_type, expected_value):
            token = self.current_token
            self.next_token()
            return token
        else:
            expected = f"{expected_type}/{expected_value}" if expected_type and expected_value else expected_type or expected_value
            raise Exception(f"Syntax Error: Expected {expected}, got {self.current_token}")
    
    def parse(self):
        if not self.tokens:
            return self.ast

        while self.match("KEYWORD") and self.current_token["value"] in \
                ["public", "private", "protected", "abstract", "final"]:
            self.next_token()

        if self.match("KEYWORD", "class"):
            self.parse_class_declaration()
        else:
            self.parse_program()

        return self.ast
    
    def parse_class_declaration(self):
        self.consume("KEYWORD", "class")
        class_name = self.consume("IDENTIFIER")["value"]
        self.ast["class_name"] = class_name
        
        if self.match("SYMBOL", "{"):
            self.consume("SYMBOL", "{")
            self.parse_class_body()
            self.consume("SYMBOL", "}")
    
    def parse_class_body(self):
        while self.current_token and not (self.match("SYMBOL", "}")):
            if self.match("KEYWORD", "public") or self.match("KEYWORD", "private") or self.match("KEYWORD", "static"):
                self.parse_method_or_field()
            else:
                break
    
    def parse_method_or_field(self):
        # Handle modifiers
        modifiers = []
        while self.match("KEYWORD") and self.current_token["value"] in ["public", "private", "protected", "static"]:
            modifiers.append(self.consume()["value"])
        
        # Check for return type or data type
        if self.match("DATA_TYPE") or (self.match("KEYWORD") and self.current_token["value"] == "void"):
            type_token = self.consume()
            
            if self.match("IDENTIFIER"):
                name_token = self.consume()
                
                # Method declaration
                if self.match("SYMBOL", "("):
                    self.parse_method(name_token["value"], type_token["value"], modifiers)
                # Field declaration
                else:
                    self.parse_field(name_token["value"], type_token["value"], modifiers)
    
    def parse_field(self, name, data_type, modifiers):
        field = {
            "type": "FieldDeclaration",
            "name": name,
            "data_type": data_type,
            "modifiers": modifiers
        }
        
        if self.match("OPERATOR", "="):
            self.consume("OPERATOR", "=")
            field["initializer"] = self.parse_expression()
        
        self.consume("SYMBOL", ";")
        self.ast["body"].append(field)
    
    def parse_method(self, name, return_type, modifiers):
        self.consume("SYMBOL", "(")
        
        parameters = []
        if not self.match("SYMBOL", ")"):
            parameters = self.parse_parameters()
        
        self.consume("SYMBOL", ")")
        
        method = {
            "type": "MethodDeclaration",
            "name": name,
            "return_type": return_type,
            "modifiers": modifiers,
            "parameters": parameters,
            "body": []
        }
        
        self.consume("SYMBOL", "{")
        method["body"] = self.parse_block()
        self.consume("SYMBOL", "}")
        
        self.ast["functions"].append(method)
        self.ast["body"].append(method)
    
    def parse_parameters(self):
        parameters = []

        while True:

            param_type = self.consume("DATA_TYPE")["value"]

            # Handle String[] args
            while self.match("SYMBOL", "["):
                self.consume("SYMBOL", "[")
                self.consume("SYMBOL", "]")
                param_type += "[]"

            param_name = self.consume("IDENTIFIER")["value"]

            parameters.append({
                "type": param_type,
                "name": param_name
            })

            if self.match("SYMBOL", ","):
                self.consume("SYMBOL", ",")
                continue

            break

        return parameters
    
    def parse_program(self):
        while self.current_token:
            if self.match("KEYWORD") or self.match("DATA_TYPE") or \
               self.match("IDENTIFIER") or self.match("PRINT"):
                statement = self.parse_statement()
                if statement:
                    self.ast["body"].append(statement)
            else:
                self.next_token()
    
    def parse_statement(self):
        if self.match("DATA_TYPE"):
            return self.parse_declaration()
        elif self.match("KEYWORD", "if"):
            return self.parse_if_statement()
        elif self.match("KEYWORD", "for"):
            return self.parse_for_loop()
        elif self.match("KEYWORD", "while"):
            return self.parse_while_loop()
        elif self.match("KEYWORD", "do"):
            return self.parse_do_while_loop()
        elif self.match("KEYWORD", "switch"):
            return self.parse_switch_statement()
        elif self.match("KEYWORD", "break"):
            return self.parse_break_statement()
        elif self.match("KEYWORD", "continue"):
            return self.parse_continue_statement()
        elif self.match("KEYWORD", "return"):
            return self.parse_return_statement()
        elif self.match("IDENTIFIER"):
            return self.parse_assignment_or_call()
        elif self.match("PRINT"):
            return self.parse_print_statement()
        elif self.match("SYMBOL", "{"):
            self.consume("SYMBOL", "{")
            stmts = self.parse_block()
            self.consume("SYMBOL", "}")
            return {"type": "Block", "statements": stmts}
        else:
            # Skip unknown tokens
            self.next_token()
            return None
    
    def parse_block(self):
        statements = []
        while self.current_token and not self.match("SYMBOL", "}"):
            stmt = self.parse_statement()
            if stmt:
                statements.append(stmt)
        
        return statements
    
    def parse_declaration(self):
        data_type = self.consume("DATA_TYPE")["value"]
        variable_name = self.consume("IDENTIFIER")["value"]
        
        declaration = {
            "type": "Declaration",
            "data_type": data_type,
            "name": variable_name
        }
        
        if self.match("OPERATOR", "="):
            self.consume("OPERATOR", "=")
            declaration["initializer"] = self.parse_expression()
        
        # Multi-variable declaration: int a = 1, b = 2, c = 3;
        if self.match("SYMBOL", ","):
            declarations = [declaration]
            while self.match("SYMBOL", ","):
                self.consume("SYMBOL", ",")
                next_name = self.consume("IDENTIFIER")["value"]
                next_decl = {"type": "Declaration", "data_type": data_type, "name": next_name}
                if self.match("OPERATOR", "="):
                    self.consume("OPERATOR", "=")
                    next_decl["initializer"] = self.parse_expression()
                declarations.append(next_decl)
            self.consume("SYMBOL", ";")
            return {"type": "MultiDeclaration", "declarations": declarations}
        
        self.consume("SYMBOL", ";")
        return declaration
    
    def parse_assignment_or_call(self):
        identifier = self.consume("IDENTIFIER")["value"]

        # Function call
        if self.match("SYMBOL", "("):
            return self.parse_function_call(identifier)

        # Postfix increment/decrement used as statement: count++; x--;
        elif self.match("OPERATOR", "++") or self.match("OPERATOR", "--"):
            op = self.consume()["value"]
            self.consume("SYMBOL", ";")
            return {
                "type": "Unary",
                "operator": op,
                "prefix": False,
                "operand": {"type": "Identifier", "name": identifier}
            }

        # Compound assignment: a += 5, a -= 3, a *= 2, a /= 4, a %= 3
        elif self.match("OPERATOR") and self.current_token["value"] in ["+=", "-=", "*=", "/=", "%="]:
            op = self.consume()["value"]
            expression = self.parse_expression()
            self.consume("SYMBOL", ";")
            base_op = op[0]  # Extract +, -, *, /, %
            # Desugar: a += b becomes a = a + b
            return {
                "type": "Assignment",
                "left": identifier,
                "right": {
                    "type": "Binary",
                    "operator": base_op,
                    "left": {"type": "Identifier", "name": identifier},
                    "right": expression
                }
            }

        # Assignment
        elif self.match("OPERATOR", "="):
            self.consume("OPERATOR", "=")
            expression = self.parse_expression()
            self.consume("SYMBOL", ";")
            return {"type": "Assignment", "left": identifier, "right": expression}

        else:
            return {"type": "Expression", "value": identifier}
    
    def parse_function_call(self, name):
        self.consume("SYMBOL", "(")
        arguments = []
        
        if not self.match("SYMBOL", ")"):
            arguments = self.parse_arguments()
        
        self.consume("SYMBOL", ")")
        self.consume("SYMBOL", ";")
        
        return {"type": "FunctionCall", "name": name, "arguments": arguments}
    
    def parse_arguments(self):
        arguments = []
        
        while True:
            arguments.append(self.parse_expression())
            
            if self.match("SYMBOL", ","):
                self.consume("SYMBOL", ",")
                continue
            break
        
        return arguments
    
    def parse_if_statement(self):
        self.consume("KEYWORD", "if")
        self.consume("SYMBOL", "(")
        condition = self.parse_expression()
        self.consume("SYMBOL", ")")
        
        if_stmt = {"type": "If", "condition": condition, "then": None, "else": None}
        
        # Then branch
        if self.match("SYMBOL", "{"):
            self.consume("SYMBOL", "{")
            if_stmt["then"] = self.parse_block()
            self.consume("SYMBOL", "}")
        else:
            if_stmt["then"] = [self.parse_statement()]
        
        # Else branch
        if self.match("KEYWORD", "else"):
            self.consume("KEYWORD", "else")
            
            if self.match("KEYWORD", "if"):
                if_stmt["else"] = [self.parse_if_statement()]
            elif self.match("SYMBOL", "{"):
                self.consume("SYMBOL", "{")
                if_stmt["else"] = self.parse_block()
                self.consume("SYMBOL", "}")
            else:
                if_stmt["else"] = [self.parse_statement()]
        
        return if_stmt
    
    def parse_for_loop(self):
        self.consume("KEYWORD", "for")
        self.consume("SYMBOL", "(")
        
        # Initialization
        if self.match("DATA_TYPE"):
            init = self.parse_declaration()
        elif self.match("IDENTIFIER"):
            init = self.parse_assignment_or_call()
        else:
            init = None
            self.consume("SYMBOL", ";")
        
        # Condition
        condition = self.parse_expression()
        self.consume("SYMBOL", ";")
        
        # Update
        update = None
        if not self.match("SYMBOL", ")"):
            update = self.parse_expression()
        
        self.consume("SYMBOL", ")")
        
        # Body
        if self.match("SYMBOL", "{"):
            self.consume("SYMBOL", "{")
            body = self.parse_block()
            self.consume("SYMBOL", "}")
        else:
            body = [self.parse_statement()]
        
        return {"type": "For", "init": init, "condition": condition, "update": update, "body": body}
    
    def parse_while_loop(self):
        self.consume("KEYWORD", "while")
        self.consume("SYMBOL", "(")
        condition = self.parse_expression()
        self.consume("SYMBOL", ")")
        
        if self.match("SYMBOL", "{"):
            self.consume("SYMBOL", "{")
            body = self.parse_block()
            self.consume("SYMBOL", "}")
        else:
            body = [self.parse_statement()]
        
        return {"type": "While", "condition": condition, "body": body}
    
    def parse_do_while_loop(self):
        self.consume("KEYWORD", "do")
        
        if self.match("SYMBOL", "{"):
            self.consume("SYMBOL", "{")
            body = self.parse_block()
            self.consume("SYMBOL", "}")
        else:
            body = [self.parse_statement()]
        
        self.consume("KEYWORD", "while")
        self.consume("SYMBOL", "(")
        condition = self.parse_expression()
        self.consume("SYMBOL", ")")
        self.consume("SYMBOL", ";")
        
        return {"type": "DoWhile", "condition": condition, "body": body}
    
    def parse_switch_statement(self):
        self.consume("KEYWORD", "switch")
        self.consume("SYMBOL", "(")
        expression = self.parse_expression()
        self.consume("SYMBOL", ")")
        self.consume("SYMBOL", "{")
        
        cases = []
        default_body = None
        
        while self.current_token and not self.match("SYMBOL", "}"):
            if self.match("KEYWORD", "case"):
                self.consume("KEYWORD", "case")
                value = self.parse_expression()
                self.consume("OPERATOR", ":")
                stmts = []
                while (self.current_token and
                       not self.match("KEYWORD", "case") and
                       not self.match("KEYWORD", "default") and
                       not self.match("SYMBOL", "}")):
                    stmt = self.parse_statement()
                    if stmt:
                        stmts.append(stmt)
                cases.append({"value": value, "body": stmts})
            elif self.match("KEYWORD", "default"):
                self.consume("KEYWORD", "default")
                self.consume("OPERATOR", ":")
                stmts = []
                while (self.current_token and
                       not self.match("KEYWORD", "case") and
                       not self.match("SYMBOL", "}")):
                    stmt = self.parse_statement()
                    if stmt:
                        stmts.append(stmt)
                default_body = stmts
            else:
                self.next_token()
        
        self.consume("SYMBOL", "}")
        return {"type": "Switch", "expression": expression, "cases": cases, "default": default_body}
    
    def parse_break_statement(self):
        self.consume("KEYWORD", "break")
        self.consume("SYMBOL", ";")
        return {"type": "Break"}
    
    def parse_continue_statement(self):
        self.consume("KEYWORD", "continue")
        self.consume("SYMBOL", ";")
        return {"type": "Continue"}
    
    def parse_return_statement(self):
        self.consume("KEYWORD", "return")
        expression = None
        
        if not self.match("SYMBOL", ";"):
            expression = self.parse_expression()
        
        self.consume("SYMBOL", ";")
        return {"type": "Return", "value": expression}
    
    def parse_print_statement(self):
        print_token = self.consume("PRINT")
        has_newline = "ln" in print_token["value"]
        
        self.consume("SYMBOL", "(")
        expression = self.parse_expression()
        self.consume("SYMBOL", ")")
        self.consume("SYMBOL", ";")
        
        return {"type": "Print", "value": expression, "newline": has_newline}
    
    def parse_expression(self):
        return self.parse_ternary()
    
    def parse_ternary(self):
        condition = self.parse_logical_or()

        if self.match("OPERATOR", "?"):
            self.consume("OPERATOR", "?")
            then_expr = self.parse_expression()
            self.consume("OPERATOR", ":")
            else_expr = self.parse_expression()
            return {
                "type": "Ternary",
                "condition": condition,
                "then": then_expr,
                "else": else_expr
            }

        return condition
    
    def parse_logical_or(self):
        left = self.parse_logical_and()
        
        while self.match("OPERATOR", "||"):
            self.consume("OPERATOR", "||")
            right = self.parse_logical_and()
            left = {"type": "Binary", "operator": "||", "left": left, "right": right}
        
        return left
    
    def parse_logical_and(self):
        left = self.parse_equality()
        
        while self.match("OPERATOR", "&&"):
            self.consume("OPERATOR", "&&")
            right = self.parse_equality()
            left = {"type": "Binary", "operator": "&&", "left": left, "right": right}
        
        return left
    
    def parse_equality(self):
        left = self.parse_relational()
        
        while self.match("OPERATOR", "==") or self.match("OPERATOR", "!="):
            operator = self.consume()["value"]
            right = self.parse_relational()
            left = {"type": "Binary", "operator": operator, "left": left, "right": right}
        
        return left
    
    def parse_relational(self):
        left = self.parse_additive()
        
        while self.match("OPERATOR", "<") or self.match("OPERATOR", ">") or \
              self.match("OPERATOR", "<=") or self.match("OPERATOR", ">="):
            operator = self.consume()["value"]
            right = self.parse_additive()
            left = {"type": "Binary", "operator": operator, "left": left, "right": right}
        
        return left
    
    def parse_additive(self):
        left = self.parse_multiplicative()
        
        while self.match("OPERATOR", "+") or self.match("OPERATOR", "-"):
            operator = self.consume()["value"]
            right = self.parse_multiplicative()
            left = {"type": "Binary", "operator": operator, "left": left, "right": right}
        
        return left
    
    def parse_multiplicative(self):
        left = self.parse_unary()
        
        while self.match("OPERATOR", "*") or self.match("OPERATOR", "/") or self.match("OPERATOR", "%"):
            operator = self.consume()["value"]
            right = self.parse_unary()
            left = {"type": "Binary", "operator": operator, "left": left, "right": right}
        
        return left
    
    def parse_unary(self):
        # Prefix: ++i, --i
        if self.match("OPERATOR", "++") or self.match("OPERATOR", "--"):
            operator = self.consume()["value"]
            operand = self.parse_primary()
            return {"type": "Unary", "operator": operator, "prefix": True, "operand": operand}

        if self.match("OPERATOR", "-") or self.match("OPERATOR", "+") or self.match("OPERATOR", "!"):
            operator = self.consume()["value"]
            operand = self.parse_unary()
            return {"type": "Unary", "operator": operator, "prefix": True, "operand": operand}

        expr = self.parse_primary()

        # Postfix: i++, i--
        if self.match("OPERATOR", "++") or self.match("OPERATOR", "--"):
            operator = self.consume()["value"]
            return {"type": "Unary", "operator": operator, "prefix": False, "operand": expr}

        return expr
    
    def parse_primary(self):
        if self.match("NUMBER"):
            token = self.consume("NUMBER")
            return {"type": "Literal", "value": token["value"], "value_type": "number"}

        elif self.match("STRING"):
            token = self.consume("STRING")
            return {"type": "Literal", "value": token["value"], "value_type": "string"}

        elif self.match("CHAR"):
            token = self.consume("CHAR")
            return {"type": "Literal", "value": token["value"], "value_type": "char"}

        elif self.match("BOOLEAN"):
            token = self.consume("BOOLEAN")
            return {"type": "Literal", "value": token["value"], "value_type": "boolean"}

        elif self.match("IDENTIFIER"):
            identifier = self.consume("IDENTIFIER")["value"]

            if self.match("SYMBOL", "("):
                self.consume("SYMBOL", "(")
                arguments = []
                if not self.match("SYMBOL", ")"):
                    arguments = self.parse_arguments()
                self.consume("SYMBOL", ")")
                return {"type": "FunctionCall", "name": identifier, "arguments": arguments}

            return {"type": "Identifier", "name": identifier}

        elif self.match("SYMBOL", "("):
            self.consume("SYMBOL", "(")
            expr = self.parse_expression()
            self.consume("SYMBOL", ")")
            return expr

        else:
            raise Exception(f"Unexpected token in expression: {self.current_token}")


def syntax_analyzer(tokens):
    if not tokens:
        return {"type": "Program", "body": []}
    
    parser = Parser(tokens)
    syntax_tree = parser.parse()
    
    with open(f"{OUTPUT_DIR}/syntax_tree.json", "w") as file:
        json.dump(syntax_tree, file, indent=4)
    
    return syntax_tree
