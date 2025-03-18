import re

TOKEN_SPEC = [
    ('NUMBER', r'\b\d+\b'),          # Integer numbers
    ('IDENT', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),  # Identifiers
    ('OP', r'[\+\-\*/=]'),           # Operators
    ('LPAREN', r'\('), ('RPAREN', r'\)'),
    ('LBRACE', r'\{'), ('RBRACE', r'\}'),
    ('SEMICOLON', r';'), ('WHITESPACE', r'\s+'),
]

TOKEN_REGEX = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in TOKEN_SPEC)

def tokenize(source_code):
    tokens = []
    for match in re.finditer(TOKEN_REGEX, source_code):
        token_type = match.lastgroup
        value = match.group(token_type)
        if token_type != 'WHITESPACE':  # Ignore spaces
            tokens.append((token_type, value))
    return tokens

# Example Test
source = "let X = 10 + 5;"
print(tokenize(source))
