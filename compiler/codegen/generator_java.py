from compiler.ast_nodes import *

class JavaGenerator:
    def __init__(self):
        self.indent_level = 2
        self.code = ""

    def emit(self, line):
        indent = "    " * self.indent_level
        self.code += f"{indent}{line}\n"

    def generate(self, node):
        self.code = "public class Main {\n    public static void main(String[] args) {\n"
        
        if isinstance(node, list):
            for n in node:
                self.visit(n)
        else:
            self.visit(node)
            
        self.code += "    }\n}\n"
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
            # Using 'var' allows Java to figure out the type automatically
            self.emit(f"var {node.target.name} = {val};")
            
        elif isinstance(node, Print):
            val = self.visit(node.expression)
            self.emit(f"System.out.println({val});")
            
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