from compiler.ast_nodes import *

class ASTOptimizer:
    """Passes over the AST to optimize it before code generation."""
    
    def optimize(self, node):
        if isinstance(node, list):
            # Optimize a block of statements
            optimized_block = []
            for n in node:
                opt_n = self.optimize(n)
                if opt_n is not None:
                    optimized_block.append(opt_n)
            return optimized_block
            
        elif isinstance(node, BinOp):
            node.left = self.optimize(node.left)
            node.right = self.optimize(node.right)
            
            # CONSTANT FOLDING: If both sides are numbers, compute it now!
            if isinstance(node.left, Number) and isinstance(node.right, Number):
                left_val = node.left.value
                right_val = node.right.value
                
                if node.op == '+': return Number(left_val + right_val)
                elif node.op == '-': return Number(left_val - right_val)
                elif node.op == '*': return Number(left_val * right_val)
                elif node.op == '/': 
                    if right_val != 0:
                        return Number(left_val / right_val)
            return node
            
        elif isinstance(node, Assign):
            node.value = self.optimize(node.value)
            return node
            
        elif isinstance(node, Print):
            node.expression = self.optimize(node.expression)
            return node
            
        elif isinstance(node, IfElse):
            node.condition = self.optimize(node.condition)
            node.true_block = self.optimize(node.true_block)
            if node.false_block:
                node.false_block = self.optimize(node.false_block)
                
            # DEAD CODE ELIMINATION: 
            # If the condition is a hardcoded '0' or 'False', drop the true block entirely.
            if isinstance(node.condition, Number):
                if node.condition.value == 0:
                    return node.false_block if node.false_block else None
                else:
                    return node.true_block
            return node
            
        elif isinstance(node, WhileLoop):
            node.condition = self.optimize(node.condition)
            node.body = self.optimize(node.body)
            # Eliminate loops that are guaranteed to be false instantly
            if isinstance(node.condition, Number) and node.condition.value == 0:
                return None 
            return node
            
        # Return the node unchanged if it's a primitive (Number, String, Identifier)
        return node