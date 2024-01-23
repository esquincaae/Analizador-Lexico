from lark import Lark, Transformer, Token, Tree

grammar = """
    start: any_estructure*

    any_estructure: FUNC | VAR | FOR | PRINT | IF | ELSE | type
       | EQUAL | SEMICOLON | LBRACE | RBRACE | LPAREN | RPAREN 
       | COMP_OPERATOR | PM | IDENTIFIER 
       | NUMBER | FLOAT | BOOLEAN | STRING | CHAR

    var_decl: VAR type IDENTIFIER EQUAL value SEMICOLON

    func_decl: FUNC IDENTIFIER LPAREN RPAREN LBRACE statement* RBRACE
    statement: function_call SEMICOLON 
    function_call: PRINT LPAREN STRING RPAREN 

    for_decl: FOR LPAREN var_decl condition SEMICOLON increment RPAREN LBRACE statement* RBRACE
    condition: IDENTIFIER COMP_OPERATOR value | IDENTIFIER COMP_OPERATOR IDENTIFIER
    increment: IDENTIFIER PM

    if_decl: IF LPAREN condition RPAREN LBRACE statement* RBRACE (ELSE LBRACE statement* RBRACE)?
  

    FUNC: "func"
    VAR: "var"
    FOR: "Para"
    PRINT: "imprimir"
    IF: "si"
    ELSE: "sino"
    type: ENT | FLOT | BOOL | CAD | CAR
    ENT: "ent"
    FLOT: "flot"
    BOOL: "bool"
    CAD: "cad"
    CAR: "car"
    EQUAL: "="
    SEMICOLON: ";"
    LBRACE: "{"
    RBRACE: "}"
    LPAREN: "("
    RPAREN: ")"
    COMP_OPERATOR: "<" | ">" | "==" | "<=" | ">=" | "!="
    PM: "++" | "--"

    value: NUMBER      -> number
         | FLOAT       -> float
         | BOOLEAN     -> boolean
         | STRING      -> string
         | CHAR        -> char

    IDENTIFIER: /[a-z][a-z]*/
    NUMBER: /0|\d[0-9]*/
    FLOAT: /\d*\.\d+/
    BOOLEAN: "verdadero" | "falso"
    STRING: /"([^"]|\\")*"/
    CHAR: /'[^']'/

    %import common.WS
    %ignore WS
"""

lexer_parser = Lark(grammar, parser='lalr')

class MyTransformer(Transformer):
    def __init__(self):
        self.tokens = []

    def add_token(self, token_type, token_value):
        self.tokens.append({token_type: str(token_value)})

    def start(self, items):
        for item in items:
            self._process_item(item)

    def _process_item(self, item):
        if isinstance(item, Token):
            self.add_token(item.type, item)
        elif isinstance(item, Tree):
            for child in item.children:
                self._process_item(child)

def procesar_entrada(entrada):
    try:
        tree = lexer_parser.parse(entrada)
        transformer = MyTransformer()
        transformer.transform(tree)
        return transformer.tokens
    except Exception as e:
        raise e