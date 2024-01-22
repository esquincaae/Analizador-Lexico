from lark import Lark, Transformer, Token, Tree
import tkinter as tk
from tkinter import messagebox

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

# Función para procesar la entrada y mostrar los tokens
def procesar():
    entrada = entry.get()
    try:
        tree = lexer_parser.parse(entrada)
        transformer = MyTransformer()
        transformer.transform(tree)
        text_area.delete('1.0', tk.END)
        for token_dict in transformer.tokens:
            for token_type, token_value in token_dict.items():
                text_area.insert(tk.END, f"{token_type}: {token_value}\n")
    except Exception as e:
        messagebox.showerror("Error de análisis", str(e))

# Crear la interfaz de usuario Tkinter
root = tk.Tk()
root.title("Lyra: Analizador Léxico")

entry = tk.Entry(root, width=100)
entry.pack(padx=10, pady=10)

boton_procesar = tk.Button(root, text="PROCESAR", command=procesar)
boton_procesar.pack(padx=10, pady=10)

text_area = tk.Text(root, height=15, width=150)
text_area.pack(padx=10, pady=10)

root.mainloop()       