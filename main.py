from lark import Lark
from trasformador import MyTransformer

def load_grammar():
    with open("grammar.lark", "r") as file:
        return file.read()

def procesar_entrada(entrada):
    try:
        grammar = load_grammar()
        lexer_parser = Lark(grammar, parser='lalr')
        tree = lexer_parser.parse(entrada) #analiza la entrada y genera un árbol de análisis sintáctico (se uso en el debug, IGNORAR)
        print(tree.pretty()) #imprime el arbol creado por la linea anterior (tambien usado para el debug, IGNORAR)
        transformer = MyTransformer()
        transformer.transform(tree)
        return transformer.get_token_counts()
    except Exception as e:
        print(e)
        raise e