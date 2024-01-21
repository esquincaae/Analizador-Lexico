from lark import Lark, Transformer

grammar = """
    start: (variable_decl ";")+

    variable_decl: VAR type IDENTIFIER EQUAL value

    VAR: "var"
    type: ENT | FLOT | BOOL | CAD | CAR
    ENT: "ent"
    FLOT: "flot"
    BOOL: "bool"
    CAD: "cad"
    CAR: "car"
    EQUAL: "="

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

    def variable_decl(self, items):
        return items

text = """
var ent num1 = 10;
var flot num2 = 10.5;
var bool  flag = falso;
var cad saludo = "123 456";
var car letra = 'a';
"""

transformer = MyTransformer()
tree = lexer_parser.parse(text)
transformer.transform(tree)

# Imprimir la lista de tokens
print(transformer.tokens)
