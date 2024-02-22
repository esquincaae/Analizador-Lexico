from lark import Transformer, Token, Tree

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