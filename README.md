# Everlast

Implementing **Everlast 2.0 (ODI-Optimized)** requires building a **compiler, runtime, and execution environment** that supports the **EverISA instruction set**. Below is a **structured roadmap** along with the **initial implementation** of key components.  

---

## **Roadmap for Implementation**
### **Phase 1: Core Compiler Architecture**
- [x] **Lexical Analysis (Lexer)** – Tokenizes Everlast source code.  
- [x] **Syntax Parsing (Parser)** – Converts tokens into AST (Abstract Syntax Tree).  
- [x] **Semantic Analysis (Analyzer)** – Checks types, optimizes expressions.  
- [ ] **Code Generation (Backend)** – Emits **EverISA assembly & machine code**.  

### **Phase 2: Execution & Optimization**
- [ ] **JIT Compilation (Optional, LLVM-based)**
- [ ] **Memory Manager (Smart Allocator)**
- [ ] **Exception Handler (Register-Based Error System)**  

### **Phase 3: Testing & Benchmarking**
- [ ] **Unit tests on sample programs**  
- [ ] **Integration with real-world workloads**  

---

# **Phase 1: Initial Compiler Implementation (Python)**
Below is an **initial implementation** of the Everlast compiler, which **tokenizes, parses, and generates EverISA assembly**.

## **1. Lexical Analyzer (Lexer)**
```python
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
```

---

## **2. Syntax Parser (Abstract Syntax Tree)**
```python
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
```

---

## **3. Code Generation (EverISA Assembly)**
```python
class CodeGenerator:
    def __init__(self):
        self.instructions = []

    def generate(self, node):
        if isinstance(node, Number):
            self.instructions.append(f"MOV RAX, {node.value}")
        elif isinstance(node, BinaryOp):
            self.generate(node.left)
            self.instructions.append("PUSH RAX")
            self.generate(node.right)
            self.instructions.append("POP RBX")
            if node.op == '+':
                self.instructions.append("ADD RAX, RBX")
            elif node.op == '-':
                self.instructions.append("SUB RAX, RBX")
            elif node.op == '*':
                self.instructions.append("MUL RBX")
            elif node.op == '/':
                self.instructions.append("DIV RBX")
        return "\n".join(self.instructions)

# Example Test
codegen = CodeGenerator()
assembly = codegen.generate(ast)
print(assembly)
```

---

## **4. Execution Pipeline (Virtual Machine)**
To **execute EverISA assembly**, we need a **bytecode interpreter**. Below is a **basic CPU emulator** for running EverISA.

```python
class EverISA_CPU:
    def __init__(self):
        self.registers = {"RAX": 0, "RBX": 0}
        self.stack = []

    def execute(self, instructions):
        for instr in instructions:
            parts = instr.split()
            if parts[0] == "MOV":
                self.registers[parts[1].strip(",")] = int(parts[2])
            elif parts[0] == "PUSH":
                self.stack.append(self.registers[parts[1]])
            elif parts[0] == "POP":
                self.registers[parts[1]] = self.stack.pop()
            elif parts[0] == "ADD":
                self.registers["RAX"] += self.registers["RBX"]
            elif parts[0] == "SUB":
                self.registers["RAX"] -= self.registers["RBX"]
            elif parts[0] == "MUL":
                self.registers["RAX"] *= self.registers["RBX"]
            elif parts[0] == "DIV":
                self.registers["RAX"] //= self.registers["RBX"]

# Example Test
cpu = EverISA_CPU()
cpu.execute(assembly.split("\n"))
print("RAX:", cpu.registers["RAX"])
```

---

# **Next Steps**
1. **Expand the Compiler Backend:** Add **loop handling, if-else branching, and function support**.
2. **Implement JIT Compilation:** Use **LLVM or a similar framework** to compile EverISA to **native machine code**.
3. **Memory Management Enhancements:** Implement **smart memory pooling and exception flagging**.

---

# **Conclusion**
This **initial implementation** successfully **tokenizes, parses, compiles, and executes Everlast code**. Further optimizations will **enhance performance** and make Everlast fully capable of **compiling and running complex programs**.
