from lark import Lark, Transformer, Token, Tree

grammar = """
    start: (var_decl | func_decl | for_decl | if_decl)*

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

    IDENTIFIER: /[a-z_][a-z0-9_]*/
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

    def start(self, items):
        for item in items:
            self._process_item(item)

    def _process_item(self, item):
        if isinstance(item, Token):
            self.add_token(item.type, item)
        elif isinstance(item, Tree):
            for child in item.children:
                self._process_item(child)

text = """
var ent num = 10;
var flot num2 = 10.5;
var bool flag = falso;
var cad saludo = "Hola mundo";
var car letra = 'a';

func saludo() {
    imprimir("hola, mundo");
}

Para(var ent i=0; i<3; i++){
    imprimir("hola, mundo"); 
}

si (num > 5){
    imprimir("noche");
}sino{
    imprimir("dia");
}
"""

transformer = MyTransformer()
tree = lexer_parser.parse(text)
transformer.transform(tree)

for token in transformer.tokens:
    print(token, end="")
    if ',' in str(token):
        print()
