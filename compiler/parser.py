from sly import Parser
from compiler.lexer import HinglishLexer
from compiler.ast_nodes import *

class HinglishParser(Parser):
    tokens = HinglishLexer.tokens

    # Enforce BODMAS / Operator Precedence
    precedence = (
        ('left', EQ, NEQ, LT, GT, LEQ, GEQ),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('right', UMINUS), 
    )

    def __init__(self):
        self.errors = []

    def error(self, token):
        if token:
            msg = f"Line {token.lineno}: Arre bhai, syntax error idhar hai -> '{token.value}'. Kuch toh gadbad hai."
            self.errors.append(msg)
        else:
            self.errors.append("Bhai, code achanak khatam ho gaya (Unexpected EOF). Bracket ya semicolon miss kiya kya?")

    # --- Program & Statements ---
    @_('statement_list')
    def program(self, p):
        return p.statement_list

    @_('statement statement_list')
    def statement_list(self, p):
        return [p.statement] + p.statement_list

    # THE FIX: This represents an empty production without causing infinite recursion
    @_('') 
    def statement_list(self, p):
        return []

    @_('assign_stmt', 'print_stmt', 'if_stmt', 'while_stmt', 'func_def', 'return_stmt', 'import_stmt')
    def statement(self, p):
        return p[0]
    
    @_('ID LBRACKET expr RBRACKET ASSIGN expr SEMICOLON')
    def assign_stmt(self, p):
        return ArrayAssign(p.ID, p.expr0, p.expr1)

    # --- Implementations ---
    @_('MAAN_LO ID ASSIGN expr SEMICOLON')
    def assign_stmt(self, p):
        return Assign(Identifier(p.ID), p.expr)

    @_('ID ASSIGN expr SEMICOLON')
    def assign_stmt(self, p):
        return Assign(Identifier(p.ID), p.expr)

    @_('DIKHAO LPAREN expr RPAREN SEMICOLON')
    def print_stmt(self, p):
        return Print(p.expr)

    @_('AGAR LPAREN expr RPAREN LBRACE statement_list RBRACE')
    def if_stmt(self, p):
        return IfElse(p.expr, p.statement_list, None)

    @_('AGAR LPAREN expr RPAREN LBRACE statement_list RBRACE WARNA LBRACE statement_list RBRACE')
    def if_stmt(self, p):
        return IfElse(p.expr, p.statement_list0, p.statement_list1)

    @_('JAB_TAK LPAREN expr RPAREN LBRACE statement_list RBRACE')
    def while_stmt(self, p):
        return WhileLoop(p.expr, p.statement_list)

    @_('MANGAAO ID SEMICOLON')
    def import_stmt(self, p):
        return ImportModule(p.ID)

    @_('BHEJ_DO expr SEMICOLON')
    def return_stmt(self, p):
        return ReturnStmt(p.expr)

    @_('KAAM ID LPAREN RPAREN LBRACE statement_list RBRACE')
    def func_def(self, p):
        return FunctionDef(p.ID, [], p.statement_list)

    # --- Expressions & Math ---
    @_('expr PLUS expr',
       'expr MINUS expr',
       'expr TIMES expr',
       'expr DIVIDE expr',
       'expr EQ expr',
       'expr NEQ expr',
       'expr LT expr',
       'expr GT expr',
       'expr LEQ expr',
       'expr GEQ expr')
    def expr(self, p):
        return BinOp(p.expr0, p[1], p.expr1)

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return BinOp(Number(0), '-', p.expr)

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return Number(p.NUMBER)

    @_('STRING')
    def expr(self, p):
        return StringLiteral(p.STRING)

    @_('ID')
    def expr(self, p):
        return Identifier(p.ID)
    
    @_('POOCHO LPAREN RPAREN')
    def expr(self, p):
        return Poocho()
    
    # Array define karna: [10, 20, 30]
    @_('LBRACKET elements RBRACKET')
    def expr(self, p):
        return ArrayLiteral(p.elements)

    # Khali Array: []
    @_('LBRACKET RBRACKET')
    def expr(self, p):
        return ArrayLiteral([])

    # Elements list handle karna (10, 20, 30)
    @_('expr COMMA elements')
    def elements(self, p):
        return [p.expr] + p.elements

    @_('expr')
    def elements(self, p):
        return [p.expr]

    # Array se value nikalna: marks[0]
    @_('ID LBRACKET expr RBRACKET')
    def expr(self, p):
        return ArrayIndex(p.ID, p.expr)