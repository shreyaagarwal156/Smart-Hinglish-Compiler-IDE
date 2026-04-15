from sly import Lexer

class HinglishLexer(Lexer):
    tokens = { 
        MAAN_LO, DIKHAO, AGAR, WARNA, JAB_TAK, KAAM, BHEJ_DO, MANGAAO, POOCHO,
        ID, NUMBER, STRING, PLUS, MINUS, TIMES, DIVIDE, ASSIGN,
        EQ, NEQ, LT, GT, LEQ, GEQ, LPAREN, RPAREN, LBRACE, RBRACE,
        LBRACKET, RBRACKET, COMMA, SEMICOLON
    }

    # Ignore spaces, tabs, and carriage returns
    ignore = ' \t\r'
    
    # Ignore comments
    ignore_comment = r'//.*' 

    # Multi-character symbols
    EQ      = r'=='
    NEQ     = r'!='
    LEQ     = r'<='
    GEQ     = r'>='
    ASSIGN  = r'='
    LT      = r'<'
    GT      = r'>'
    PLUS    = r'\+'
    MINUS   = r'-'
    TIMES   = r'\*'
    DIVIDE  = r'/'
    LPAREN  = r'\('
    RPAREN  = r'\)'
    LBRACE  = r'\{'
    RBRACE  = r'\}'
    LBRACKET= r'\['
    RBRACKET= r'\]'
    COMMA   = r','
    SEMICOLON= r';'

    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    
    # Hinglish Keywords map (POOCHO ADDED HERE)
    ID['maan_lo'] = MAAN_LO    
    ID['dikhao']  = DIKHAO     
    ID['agar']    = AGAR       
    ID['warna']   = WARNA      
    ID['jab_tak'] = JAB_TAK    
    ID['kaam']    = KAAM       
    ID['bhej_do'] = BHEJ_DO    
    ID['mangaao'] = MANGAAO    
    ID['poocho']  = POOCHO     

    @_(r'\d+(\.\d+)?')
    def NUMBER(self, t):
        t.value = float(t.value) if '.' in t.value else int(t.value)
        return t

    @_(r'\".*?\"|\'.*?\'')
    def STRING(self, t):
        t.value = t.value[1:-1]
        return t

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print(f"Line {self.lineno}: Arre bhai, '{t.value[0]}' invalid character hai.")
        self.index += 1