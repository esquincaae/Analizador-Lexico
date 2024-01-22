from lark import Lark, Transformer

grammar = """
    start: (variable_decl SEMICOLON)* (function_decl)*

    variable_decl: VAR type IDENTIFIER EQUAL value

    function_decl: FUNC IDENTIFIER LPAREN RPAREN LBRACE statement* RBRACE
    statement: function_call SEMICOLON
    function_call: IDENTIFIER LPAREN STRING RPAREN

    FUNC: "func"
    VAR: "var"
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

    value: NUMBER       -> number
         | FLOAT       -> float
         | BOOLEAN     -> boolean
         | STRING      -> string
         | CHAR        -> char

    IDENTIFIER: /[a-zA-Z_][a-zA-Z0-9_]*/
    NUMBER: /\d+/
    FLOAT: /\d+\.\d+/
    BOOLEAN: "verdadero" | "falso"
    STRING: /"[^"]*"/
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

    def FUNC(self, token):
        self.add_token("FUNC", token)
        return token

    def VAR(self, token):
        self.add_token("VAR", token)
        return token

    def ENT(self, token):
        self.add_token("TYPE", token)
        return token

    def FLOT(self, token):
        self.add_token("TYPE", token)
        return token

    def BOOL(self, token):
        self.add_token("TYPE", token)
        return token

    def CAD(self, token):
        self.add_token("TYPE", token)
        return token

    def CAR(self, token):
        self.add_token("TYPE", token)
        return token

    def EQUAL(self, token):
        self.add_token("EQUAL", token)
        return token

    def SEMICOLON(self, token):
        self.add_token("CLOSELINE", token)
        return token

    def IDENTIFIER(self, token):
        self.add_token("IDENTIFIER", token)
        return token

    def NUMBER(self, token):
        self.add_token("NUMBER", token)
        return token

    def FLOAT(self, token):
        self.add_token("FLOAT", token)
        return token

    def BOOLEAN(self, token):
        self.add_token("BOOLEAN", token)
        return token

    def STRING(self, token):
        self.add_token("STRING", token)
        return token

    def CHAR(self, token):
        self.add_token("CHAR", token)
        return token

    def function_decl(self, items):
        function_name = items[1]
        self.add_token("FUNCTION", function_name)
        return items

    def function_call(self, items):
        function_name = items[0]
        self.add_token("FUNC_CALL", function_name)
        return items
    
    def LBRACE(self, token):
        self.add_token("LBRACE", token)
        return token

    def RBRACE(self, token):
        self.add_token("RBRACE", token)
        return token

    def LPAREN(self, token):
        self.add_token("LPAREN", token)
        return token

    def RPAREN(self, token):
        self.add_token("RPAREN", token)
        return token

text = """
var ent num1 = 10;
var flot num2 = 10.5;
var bool flag = falso;
var cad saludo = "Hola mundo";
var car letra = 'a';

func saludo() {
    imprimir("hola, mundo");
}
"""

transformer = MyTransformer()
tree = lexer_parser.parse(text)
transformer.transform(tree)

for token in transformer.tokens:
    print(token, end="")
    if ',' in str(token):
        print()