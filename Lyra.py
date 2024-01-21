from lark import Lark, Transformer, v_args

grammar = """
    start: (variable_decl ";")+

    variable_decl: "var" type IDENTIFIER "=" value

    type: "ent" | "flot" | "bool" | "cad" | "car"
    
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


@v_args(inline=True)    # Aplies the transformer to the children of a node
class MyTransformer(Transformer):
    def variable_decl(self, var_type, identifier, value):
        return (str(var_type), str(identifier), value)

    number = int
    float = float
    boolean = lambda self, x: x == "verdadero"
    string = lambda self, x: x[1:-1]  # Remove quotes
    char = lambda self, x: x[1:-1]    # Remove single quotes


text = """
var ent num1 = 10;
var flot num2 = 10.5;
var bool flag = falso;
var cad saludo = "Hola mundo";
var car letra = 'a';
"""

tree = lexer_parser.parse(text)
transformed = MyTransformer().transform(tree)
print(transformed.pretty())
