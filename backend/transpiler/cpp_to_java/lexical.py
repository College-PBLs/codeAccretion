import re
import json
from ..config import OUTPUT_DIR

TOKEN_REGEX = [
    ("KEYWORD",    r'\b(auto|break|case|catch|class|const|continue|default|delete|do|else|enum|explicit|extern|finally|for|friend|goto|if|inline|mutable|namespace|new|operator|private|protected|public|register|return|sizeof|static|struct|switch|template|this|throw|try|typedef|typeid|typename|union|using|virtual|volatile|while)\b'),
    ("BOOLEAN",    r'\b(true|false)\b'),
    ("NULLPTR",    r'\bnullptr\b'),
    ("DATA_TYPE",  r'\b(void|bool|char|short|int|long|float|double|string|auto|size_t|uint8_t|int8_t|uint16_t|int16_t|uint32_t|int32_t|uint64_t|int64_t)\b'),
    ("COUT",       r'cout'),
    ("ENDL",       r'endl'),
    ("COMMENT",    r'//[^\n]*|/\*[\s\S]*?\*/'),
    ("NUMBER",     r'\b\d+(\.\d+)?([eE][+-]?\d+)?(f|l|u|ul|ll|ull)?\b'),
    ("STRING",     r'"[^"\\]*(\\.[^"\\]*)*"'),
    ("CHAR",       r"'(\\['\\]|[^'])'"),
    ("IDENTIFIER", r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    ("OPERATOR",   r'==|!=|<=|>=|\+=|-=|\*=|/=|%=|\+\+|--|&&|\|\||<<|>>|->|\*|&|[-+/%=<>!^~?:]'),
    ("SYMBOL",     r'[{}()\[\];,.]'),
    ("WHITESPACE", r'\s+'),
]


def preprocess(code):
    """Strip C++ preprocessor directives (#include, #define, #pragma, etc.)"""
    lines = code.splitlines()
    cleaned = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#'):
            continue  # drop the entire directive line
        cleaned.append(line)
    return '\n'.join(cleaned)


def lexical_analyzer(code):
    code = preprocess(code)
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
            raise Exception(f"Lexical Error: Invalid character '{code[position]}' at position {position}")

    with open(f"{OUTPUT_DIR}/tokens.json", "w") as f:
        json.dump(tokens, f, indent=4)

    return tokens
