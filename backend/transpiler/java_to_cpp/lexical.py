import re
import json
from ..config import OUTPUT_DIR

TOKEN_REGEX = [
    ("KEYWORD", r'\b(public|private|protected|static|void|class|new|this|super|return|if|else|for|while|do|break|continue|switch|case|default|try|catch|finally|throw|throws|import|package|extends|implements|interface|abstract|final|native|synchronized|transient|volatile|strictfp|enum|assert)\b'),
    ("BOOLEAN", r'\b(true|false)\b'),
    ("DATA_TYPE", r'\b(int|float|double|char|boolean|byte|short|long|String)\b'),
    ("PRINT", r'System\.out\.print(ln)?'),
    ("COMMENT", r'//[^\n]*|/\*[\s\S]*?\*/'),
    ("NUMBER", r'\b\d+(\.\d+)?([eE][+-]?\d+)?([fFdDlL])?\b'),
    ("STRING", r'"[^"\\]*(\\.[^"\\]*)*"'),
    ("CHAR", r"'(\\['\\]|[^'])'"),
    ("IDENTIFIER", r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ("OPERATOR", r'==|!=|<=|>=|\+=|-=|\*=|/=|%=|\+\+|--|&&|\|\||<<|>>|>>>|[-+*/%=<>!&|^~?:]'),
    ("SYMBOL", r'[{}()\[\];,.]'),
    ("WHITESPACE", r'\s+'),
]


def lexical_analyzer(code):
    tokens = []
    position = 0
    
    while position < len(code):
        match = None
        
        for token_type, pattern in TOKEN_REGEX:
            regex = re.compile(pattern, re.MULTILINE)
            match = regex.match(code, position)
            
            if match:
                value = match.group(0)
                
                if token_type not in ["WHITESPACE", "COMMENT"]:
                    tokens.append({
                        "type": token_type,
                        "value": value,
                        "position": position
                    })
                
                position = match.end(0)
                break
        
        if not match:
            raise Exception(f"Lexical Error: Invalid Character '{code[position]}' at position {position}")
    
    with open(f"{OUTPUT_DIR}/tokens.json", "w") as file:
        json.dump(tokens, file, indent=4)
    
    return tokens
