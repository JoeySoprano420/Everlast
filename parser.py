class ASTNode:
    pass

class Number(ASTNode):
    def __init__(self, value):
        self.value = int(value)

class Variable(ASTNode):
    def __init__(self, name):
        self.name = name

class BinaryOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, None)

    def consume(self):
        token = self.tokens[self.pos]
        self.pos += 1
        return token

    def parse_expression(self):
        left = self.parse_primary()
        while self.peek()[0] == 'OP':
            op = self.consume()[1]
            right = self.parse_primary()
            left = BinaryOp(left, op, right)
        return left

    def parse_primary(self):
        token_type, value = self.consume()
        if token_type == 'NUMBER':
            return Number(value)
        elif token_type == 'IDENT':
            return Variable(value)
        elif token_type == 'LPAREN':
            expr = self.parse_expression()
            self.consume()  # Consume RPAREN
            return expr
        raise SyntaxError(f"Unexpected token: {value}")

    def parse(self):
        return self.parse_expression()

# Example Test
tokens = tokenize("10 + 5")
parser = Parser(tokens)
ast = parser.parse()
print(ast)
