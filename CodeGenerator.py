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
