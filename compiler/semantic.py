from compiler.ast_nodes import *
from fuzzywuzzy import process

class SemanticAnalyzer:
    def __init__(self):
        # Stack of dictionaries to handle local and global scopes
        self.scopes = [{}] 
        self.errors = []

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def declare_variable(self, name, node_type="Any"):
        # Add variable to the current local scope
        self.scopes[-1][name] = node_type

    def lookup_variable(self, name):
        # Check from innermost scope to outermost
        for scope in reversed(self.scopes):
            if name in scope:
                return True
        return False

    def suggest_correction(self, misspelled_name):
        # Flatten all known variables across all scopes
        all_vars = [var for scope in self.scopes for var in scope.keys()]
        if not all_vars:
            return None
        
        # ML NLP Fallback: Find the closest matching variable name
        best_match, score = process.extractOne(misspelled_name, all_vars)
        if score > 75: # 75% similarity threshold
            return best_match
        return None

    def analyze(self, node):
        """Recursively traverse the AST to check semantics."""
        if isinstance(node, list):
            for n in node:
                self.analyze(n)
                
        elif isinstance(node, Assign):
            # If it's a new assignment, declare it
            self.declare_variable(node.target.name)
            self.analyze(node.value)
            
        elif isinstance(node, Identifier):
            if not self.lookup_variable(node.name):
                suggestion = self.suggest_correction(node.name)
                error_msg = f"Arre bhai, '{node.name}' toh define hi nahi kiya!"
                if suggestion:
                    error_msg += f" Did you mean '{suggestion}'?"
                self.errors.append(error_msg)
                
        elif isinstance(node, BinOp):
            self.analyze(node.left)
            self.analyze(node.right)
            
        elif isinstance(node, Print):
            self.analyze(node.expression)
            
        elif isinstance(node, IfElse):
            self.analyze(node.condition)
            self.enter_scope()
            self.analyze(node.true_block)
            self.exit_scope()
            if node.false_block:
                self.enter_scope()
                self.analyze(node.false_block)
                self.exit_scope()
                
        elif isinstance(node, WhileLoop):
            self.analyze(node.condition)
            self.enter_scope()
            self.analyze(node.body)
            self.exit_scope()