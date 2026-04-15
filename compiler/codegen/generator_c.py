from compiler.ast_nodes import *

class CGenerator:
    def __init__(self):
        self.indent_level = 1
        self.code = ""
        self.includes = ["#include <stdio.h>", "#include <stdlib.h>"]

    def emit(self, line):
        indent = "    " * self.indent_level
        self.code += f"{indent}{line}\n"

    def generate(self, node):
        headers = "\n".join(self.includes)
        self.code = f"{headers}\n\nint main() {{\n"
        
        if isinstance(node, list):
            for n in node:
                self.visit(n)
        else:
            self.visit(node)
            
        self.code += "    return 0;\n}\n"
        return self.code

    def visit(self, node):
        if node is None:
            return ""
            
        if isinstance(node, Number):
            return str(node.value)
            
        elif isinstance(node, StringLiteral):
            return f'"{node.value}"'
            
        elif isinstance(node, Identifier):
            return node.name
            
        elif isinstance(node, BinOp):
            left = self.visit(node.left)
            right = self.visit(node.right)
            return f"({left} {node.op} {right})"
            
        elif isinstance(node, Assign):
            val = self.visit(node.value)
            # C doesn't have native auto without extensions, defaulting to double
            self.emit(f"double {node.target.name} = {val};")
            
        elif isinstance(node, Print):
            val = self.visit(node.expression)
            if isinstance(node.expression, StringLiteral):
                self.emit(f'printf("%s\\n", {val});')
            else:
                self.emit(f'printf("%f\\n", (double)({val}));')
                
        elif isinstance(node, IfElse):
            cond = self.visit(node.condition)
            self.emit(f"if ({cond}) {{")
            self.indent_level += 1
            for n in node.true_block:
                self.visit(n)
            self.indent_level -= 1
            self.emit("}")
            
            if node.false_block:
                self.emit("else {")
                self.indent_level += 1
                for n in node.false_block:
                    self.visit(n)
                self.indent_level -= 1
                self.emit("}")
                
        elif isinstance(node, WhileLoop):
            cond = self.visit(node.condition)
            self.emit(f"while ({cond}) {{")
            self.indent_level += 1
            for n in node.body:
                self.visit(n)
            self.indent_level -= 1
            self.emit("}")