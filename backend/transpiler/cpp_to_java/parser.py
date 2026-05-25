import re
import json
from ..config import OUTPUT_DIR

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = tokens[0] if tokens else None
        self.ast = {
            "type": "Program",
            "body": [],
            "functions": [],
            "class_name": None
        }


    # Core helpers
    def peek(self):
        return self.current_token

    def peek_ahead(self, offset=1):
        idx = self.position + offset
        return self.tokens[idx] if idx < len(self.tokens) else None

    def next_token(self):
        self.position += 1
        self.current_token = self.tokens[self.position] if self.position < len(self.tokens) else None
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
        expected = (
            f"{expected_type}/{expected_value}"
            if expected_type and expected_value
            else expected_type or expected_value
        )
        raise Exception(f"Syntax Error: Expected {expected}, got {self.current_token}")

    def _parse_remaining_functions(self):
        while self.current_token:

            if self.match("DATA_TYPE") or (
                self.match("KEYWORD") and
                self.current_token["value"] in ("void", "int", "static", "inline")
            ):
                start_pos = self.position
                return_type = self.consume()["value"]

                # Consume any modifiers like static, inline that come after
                while self.match("KEYWORD") and self.current_token["value"] in ("static", "inline", "const"):
                    return_type += " " + self.consume()["value"]

                # Pointer/reference decorators
                while self.match("OPERATOR") and self.current_token["value"] in ("*", "&"):
                    return_type += self.consume()["value"]

                if not self.match("IDENTIFIER"):
                    # Not a function or declaration — rollback and parse as statement
                    self.position = start_pos
                    self.current_token = self.tokens[self.position]
                    stmt = self.parse_statement()
                    if stmt:
                        self.ast["body"].append(stmt)
                    continue

                name = self.consume("IDENTIFIER")["value"]

                if self.match("SYMBOL", "("):
                    self.parse_method(name, return_type, [])
                else:
                    # It's a variable declaration — rollback and let parse_statement handle it
                    self.position = start_pos
                    self.current_token = self.tokens[self.position]
                    stmt = self.parse_statement()
                    if stmt:
                        self.ast["body"].append(stmt)

            else:
                stmt = self.parse_statement()
                if stmt:
                    self.ast["body"].append(stmt)

    def parse(self):
        if not self.tokens:
            return self.ast

        self._skip_preprocessor()

        if self.match("KEYWORD", "class") or self._is_class_ahead():
            self.parse_class_declaration()
            self._parse_remaining_functions()
        else:
            self._parse_remaining_functions()

        return self.ast

    def _skip_preprocessor(self):
        """Skip #include lines and 'using namespace …;' statements."""
        while self.current_token:
            # using namespace std;
            if self.match("KEYWORD", "using"):
                while self.current_token and not self.match("SYMBOL", ";"):
                    self.next_token()
                if self.match("SYMBOL", ";"):
                    self.next_token()
                continue
            break

    def _is_class_ahead(self):
        """Look for access-modifier run followed by 'class'."""
        i = self.position
        while i < len(self.tokens):
            v = self.tokens[i]["value"]
            if v in ("public", "private", "protected", "abstract", "final"):
                i += 1
                continue
            return v == "class"
        return False


    # Class
    def parse_class_declaration(self):
        # Skip leading access modifiers
        while self.match("KEYWORD") and self.current_token["value"] in (
            "public", "private", "protected", "abstract", "final"
        ):
            self.next_token()

        self.consume("KEYWORD", "class")
        class_name = self.consume("IDENTIFIER")["value"]
        self.ast["class_name"] = class_name

        if self.match("OPERATOR", ":"):
            self.next_token()
            while self.current_token and not self.match("SYMBOL", "{"):
                self.next_token()

        if self.match("SYMBOL", "{"):
            self.consume("SYMBOL", "{")
            self.parse_class_body()
            self.consume("SYMBOL", "}")
            # optional trailing semicolon
            if self.match("SYMBOL", ";"):
                self.next_token()

    def parse_class_body(self):
        while self.current_token and not self.match("SYMBOL", "}"):
            # Access specifier labels  (public:  private:  protected:)
            if self.match("KEYWORD") and self.current_token["value"] in (
                "public", "private", "protected"
            ):
                self.next_token()
                if self.match("OPERATOR", ":"):
                    self.next_token()
                continue

            if self._is_method_or_field_start():
                self.parse_method_or_field()
            else:
                self.next_token()

    def _is_method_or_field_start(self):
        if self.match("DATA_TYPE"):
            return True
        if self.match("KEYWORD") and self.current_token["value"] in (
            "void", "virtual", "static", "inline", "explicit",
            "const", "friend", "public", "private", "protected"
        ):
            return True
        if self.match("IDENTIFIER"):
            ahead = self.peek_ahead()
            if ahead and ahead["value"] == "(":
                return True
        return False

    def parse_method_or_field(self):
        modifiers = []
        while self.match("KEYWORD") and self.current_token["value"] in (
            "public", "private", "protected", "static", "virtual",
            "inline", "explicit", "const", "friend"
        ):
            modifiers.append(self.consume()["value"])

        # return type or data type
        if self.match("DATA_TYPE") or (
            self.match("KEYWORD") and self.current_token["value"] == "void"
        ):
            type_token = self.consume()
            type_str = type_token["value"]

            # pointer / reference decorators
            while self.match("OPERATOR") and self.current_token["value"] in ("*", "&"):
                type_str += self.consume()["value"]

            if self.match("IDENTIFIER"):
                name_token = self.consume()
                if self.match("SYMBOL", "("):
                    self.parse_method(name_token["value"], type_str, modifiers)
                else:
                    self.parse_field(name_token["value"], type_str, modifiers)
        elif self.match("IDENTIFIER"):
            # Possibly a constructor  MyClass(…)  or a field of a user-defined type
            name_token = self.consume()
            if self.match("SYMBOL", "("):
                self.parse_method(name_token["value"], "void", modifiers)
            elif self.match("IDENTIFIER"):
                field_name = self.consume()
                self.parse_field(field_name["value"], name_token["value"], modifiers)
            else:
                # skip
                while self.current_token and not self.match("SYMBOL", ";"):
                    self.next_token()
                if self.match("SYMBOL", ";"):
                    self.next_token()

    def parse_field(self, name, data_type, modifiers):
        field = {
            "type": "FieldDeclaration",
            "name": name,
            "data_type": data_type,
            "modifiers": modifiers,
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

        # trailing const
        if self.match("KEYWORD", "const"):
            self.next_token()

        method = {
            "type": "MethodDeclaration",
            "name": name,
            "return_type": return_type,
            "modifiers": modifiers,
            "parameters": parameters,
            "body": [],
        }

        # pure virtual  = 0;
        if self.match("OPERATOR", "="):
            self.next_token()
            self.next_token()  # skip '0'
            self.consume("SYMBOL", ";")
            self.ast["functions"].append(method)
            self.ast["body"].append(method)
            return

        if self.match("SYMBOL", "{"):
            self.consume("SYMBOL", "{")
            method["body"] = self.parse_block()
            self.consume("SYMBOL", "}")
        else:
            # declaration only (;)
            self.consume("SYMBOL", ";")

        self.ast["functions"].append(method)
        self.ast["body"].append(method)

    def parse_parameters(self):
        parameters = []
        while True:
            # type
            if self.match("DATA_TYPE"):
                param_type = self.consume()["value"]
            elif self.match("KEYWORD") and self.current_token["value"] == "const":
                self.next_token()
                param_type = self.consume()["value"] if self.current_token else "auto"
            elif self.match("IDENTIFIER"):
                param_type = self.consume()["value"]
            else:
                break

            # pointer / reference
            while self.match("OPERATOR") and self.current_token["value"] in ("*", "&"):
                param_type += self.consume()["value"]

            # name (optional in declarations)
            if self.match("IDENTIFIER"):
                param_name = self.consume()["value"]
            else:
                param_name = f"_p{len(parameters)}"

            # array brackets
            while self.match("SYMBOL", "["):
                self.consume("SYMBOL", "[")
                if not self.match("SYMBOL", "]"):
                    self.parse_expression()
                self.consume("SYMBOL", "]")
                param_type += "[]"

            # default value
            if self.match("OPERATOR", "="):
                self.next_token()
                self.parse_expression()

            parameters.append({"type": param_type, "name": param_name})

            if self.match("SYMBOL", ","):
                self.consume("SYMBOL", ",")
                continue
            break
        return parameters

    def parse_program(self):
        while self.current_token:
            if (self.match("KEYWORD") or self.match("DATA_TYPE") or
                    self.match("IDENTIFIER") or self.match("COUT")):
                stmt = self.parse_statement()
                if stmt:
                    self.ast["body"].append(stmt)
            else:
                self.next_token()


    # Statements
    def parse_statement(self):
        # const qualifier before data type
        if self.match("KEYWORD", "const"):
            self.next_token()

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
        elif self.match("COUT"):
            return self.parse_cout_statement()
        # elif self.match("CIN"):
        #     return self.parse_cin_statement()
        elif self.match("IDENTIFIER"):
            return self.parse_assignment_or_call()
        elif self.match("SYMBOL", "{"):
            self.consume("SYMBOL", "{")
            stmts = self.parse_block()
            self.consume("SYMBOL", "}")
            return {"type": "Block", "statements": stmts}
        else:
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

        # pointer / reference
        while self.match("OPERATOR") and self.current_token["value"] in ("*", "&"):
            data_type += self.consume()["value"]

        variable_name = self.consume("IDENTIFIER")["value"]

        # array  int arr[10]
        if self.match("SYMBOL", "["):
            self.consume("SYMBOL", "[")
            if not self.match("SYMBOL", "]"):
                self.parse_expression()
            self.consume("SYMBOL", "]")
            data_type += "[]"

        declaration = {"type": "Declaration", "data_type": data_type, "name": variable_name}

        if self.match("OPERATOR", "="):
            self.consume("OPERATOR", "=")
            declaration["initializer"] = self.parse_expression()

        # Multi-variable:  int a = 1, b = 2;
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

        # Scoped call  std::cout / ns::fn
        if self.match("OPERATOR", ":") and self.peek_ahead() and self.peek_ahead()["value"] == ":":
            self.next_token(); self.next_token()
            identifier += "::" + self.consume("IDENTIFIER")["value"]

        if self.match("SYMBOL", "("):
            return self.parse_function_call(identifier)

        elif self.match("OPERATOR", "++") or self.match("OPERATOR", "--"):
            op = self.consume()["value"]
            self.consume("SYMBOL", ";")
            return {
                "type": "Unary",
                "operator": op,
                "prefix": False,
                "operand": {"type": "Identifier", "name": identifier},
            }

        elif self.match("OPERATOR") and self.current_token["value"] in ("+=", "-=", "*=", "/=", "%="):
            op = self.consume()["value"]
            expression = self.parse_expression()
            self.consume("SYMBOL", ";")
            return {
                "type": "CompoundAssignment",
                "left": identifier,
                "operator": op,
                "right": expression,
            }

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


    # cout  →  Print
    def parse_cout_statement(self):
        """
        cout << expr1 << expr2 << endl;
        Maps to a Print node. Multiple << operands are folded into
        string-concatenation Binary nodes like the Java transpiler does.
        """
        self.consume("COUT")
        has_newline = False
        parts = []

        while self.match("OPERATOR", "<<"):
            self.consume("OPERATOR", "<<")
            if self.match("ENDL"):
                self.consume("ENDL")
                has_newline = True
                break
            parts.append(self.parse_expression())

        self.consume("SYMBOL", ";")

        if not parts:

            value = {
                "type": "Literal",
                "value": '""',
                "value_type": "string"
            }

        elif len(parts) == 1:

            value = parts[0]

        else:

            value = {
                "type": "PrintChain",
                "parts": parts
            }

        return {"type": "Print", "value": value, "newline": has_newline}

    
    # Control flow
    def parse_if_statement(self):
        self.consume("KEYWORD", "if")
        self.consume("SYMBOL", "(")
        condition = self.parse_expression()
        self.consume("SYMBOL", ")")

        if_stmt = {"type": "If", "condition": condition, "then": None, "else": None}

        if self.match("SYMBOL", "{"):
            self.consume("SYMBOL", "{")
            if_stmt["then"] = self.parse_block()
            self.consume("SYMBOL", "}")
        else:
            if_stmt["then"] = [self.parse_statement()]

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

        if self.match("DATA_TYPE"):
            init = self.parse_declaration()
        elif self.match("IDENTIFIER"):
            init = self.parse_assignment_or_call()
        else:
            init = None
            self.consume("SYMBOL", ";")

        condition = self.parse_expression()
        self.consume("SYMBOL", ";")

        update = None
        if not self.match("SYMBOL", ")"):
            update = self.parse_expression()

        self.consume("SYMBOL", ")")

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

    
    # Expressions
    def parse_expression(self):
        return self.parse_ternary()

    def parse_ternary(self):
        condition = self.parse_logical_or()
        if self.match("OPERATOR", "?"):
            self.consume("OPERATOR", "?")
            then_expr = self.parse_expression()
            self.consume("OPERATOR", ":")
            else_expr = self.parse_expression()
            return {"type": "Ternary", "condition": condition, "then": then_expr, "else": else_expr}
        return condition

    def parse_logical_or(self):
        left = self.parse_logical_and()
        while self.match("OPERATOR", "||"):
            self.consume()
            right = self.parse_logical_and()
            left = {"type": "Binary", "operator": "||", "left": left, "right": right}
        return left

    def parse_logical_and(self):
        left = self.parse_equality()
        while self.match("OPERATOR", "&&"):
            self.consume()
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
        while (self.match("OPERATOR", "<") or self.match("OPERATOR", ">") or
               self.match("OPERATOR", "<=") or self.match("OPERATOR", ">=")):
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
        if self.match("OPERATOR", "++") or self.match("OPERATOR", "--"):
            operator = self.consume()["value"]
            operand = self.parse_primary()
            return {"type": "Unary", "operator": operator, "prefix": True, "operand": operand}

        if self.match("OPERATOR", "-") or self.match("OPERATOR", "+") or self.match("OPERATOR", "!"):
            operator = self.consume()["value"]
            operand = self.parse_unary()
            return {"type": "Unary", "operator": operator, "prefix": True, "operand": operand}

        # dereference / address-of — treat as pass-through
        if self.match("OPERATOR", "*") or self.match("OPERATOR", "&"):
            self.consume()
            return self.parse_primary()

        expr = self.parse_primary()

        if self.match("OPERATOR", "++") or self.match("OPERATOR", "--"):
            operator = self.consume()["value"]
            return {"type": "Unary", "operator": operator, "prefix": False, "operand": expr}

        return expr

    def parse_primary(self):
        if self.match("NUMBER"):
            token = self.consume("NUMBER")
            # Strip C++ numeric suffixes (f, l, u, …)
            raw = re.sub(r'[fFlLuU]+$', '', token["value"])
            return {"type": "Literal", "value": raw, "value_type": "number"}

        elif self.match("STRING"):
            token = self.consume("STRING")
            return {"type": "Literal", "value": token["value"], "value_type": "string"}

        elif self.match("CHAR"):
            token = self.consume("CHAR")
            return {"type": "Literal", "value": token["value"], "value_type": "char"}

        elif self.match("BOOLEAN"):
            token = self.consume("BOOLEAN")
            return {"type": "Literal", "value": token["value"], "value_type": "boolean"}

        elif self.match("NULLPTR"):
            self.consume("NULLPTR")
            return {"type": "Literal", "value": "null", "value_type": "null"}

        elif self.match("ENDL"):
            self.consume("ENDL")
            return {"type": "Literal", "value": '"\\n"', "value_type": "string"}

        elif self.match("IDENTIFIER") or self.match("COUT") or self.match("CIN"):
            identifier = self.consume()["value"]

            # Scoped  std::something
            if self.match("OPERATOR", ":") and self.peek_ahead() and self.peek_ahead()["value"] == ":":
                self.next_token(); self.next_token()
                identifier += "::" + self.consume("IDENTIFIER")["value"]

            if self.match("SYMBOL", "("):
                self.consume("SYMBOL", "(")
                arguments = []
                if not self.match("SYMBOL", ")"):
                    arguments = []
                    while not self.match("SYMBOL", ")"):

                        arguments.append(self.parse_expression())

                        if self.match("SYMBOL", ","):
                            self.consume("SYMBOL", ",")
                        else:
                            break
                self.consume("SYMBOL", ")")
                return {"type": "FunctionCall", "name": identifier, "arguments": arguments}

            # Member access  obj.member  /  ptr->member
            if self.match("SYMBOL", ".") or (self.match("OPERATOR") and self.current_token["value"] == "->"):
                self.consume()
                if self.match("IDENTIFIER"):
                    member = self.consume("IDENTIFIER")["value"]
                    if self.match("SYMBOL", "("):
                        self.consume("SYMBOL", "(")
                        arguments = []
                        if not self.match("SYMBOL", ")"):
                            arguments = self.parse_arguments()
                        self.consume("SYMBOL", ")")
                        return {
                            "type": "MethodCall",
                            "object": identifier,
                            "method": member,
                            "arguments": arguments,
                        }
                    return {
                        "type": "MemberAccess",
                        "object": identifier,
                        "member": member,
                    }

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

    with open(f"{OUTPUT_DIR}/syntax_tree.json", "w") as f:
        json.dump(syntax_tree, f, indent=4)

    return syntax_tree
