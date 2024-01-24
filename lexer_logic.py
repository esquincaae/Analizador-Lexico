from lark import Lark, Transformer, Token, Tree

grammar = """
    start: any_estructure*

    any_estructure: FUNC | VAR | FOR | PRINT | IF | ELSE | var_type
       | SEMICOLON | BRACKET | PAREN | OPERATOR | IDENTIFIER 
       | NUMBER | FLOAT | BOOLEAN | STRING | CHAR | PM | EQUAL
       | UNKNOWN

    FUNC: "func"
    VAR: "var"
    FOR: "Para"
    PRINT: "imprimir"
    IF: "si"
    ELSE: "sino"
    var_type: "ent" | "flot" | "bool" | "cad" | "car"
    SEMICOLON: ";"
    BRACKET: "{" | "}"
    PAREN: "(" | ")"
    OPERATOR: "<" | ">" | "<=" | ">=" | "!=" | "=="
    PM: "++" | "--" 
    EQUAL: "="
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
    UNKNOWN: /./

    %import common.WS
    %ignore WS
"""

lexer_parser = Lark(grammar, parser='lalr')

class MyTransformer(Transformer):
    def __init__(self):
        self.token_counts = {}

    def add_token(self, token_type, token_value):
        if token_type not in self.token_counts:
            self.token_counts[token_type] = 0
        self.token_counts[token_type] += 1

    def start(self, items):
        for item in items:
            self._process_item(item)

    def _process_item(self, item):
        if isinstance(item, Token):
            self.add_token(item.type, item)
        elif isinstance(item, Tree):
            for child in item.children:
                self._process_item(child)

    def get_token_counts(self):
        return self.token_counts


def procesar_entrada(entrada):
    try:
        tree = lexer_parser.parse(entrada)
        transformer = MyTransformer()
        transformer.transform(tree)
        return transformer.get_token_counts()
    except Exception as e:
        raise e
