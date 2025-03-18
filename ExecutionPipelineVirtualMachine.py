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
