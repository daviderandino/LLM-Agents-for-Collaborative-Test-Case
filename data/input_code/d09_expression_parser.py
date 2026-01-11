from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    PLUS = auto()
    MINUS = auto()
    MUL = auto()
    DIV = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
    
    def get_token(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1
        if self.pos >= len(self.text):
            return Token(TokenType.EOF, None)
        c = self.text[self.pos]
        if c.isdigit():
            num = ""
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                num += self.text[self.pos]
                self.pos += 1
            return Token(TokenType.NUMBER, int(num))
        self.pos += 1
        tokens = {"+": TokenType.PLUS, "-": TokenType.MINUS, 
                  "*": TokenType.MUL, "/": TokenType.DIV,
                  "(": TokenType.LPAREN, ")": TokenType.RPAREN}
        if c in tokens:
            return Token(tokens[c], c)
        raise SyntaxError(f"Unknown char: {c}")

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.token = self.lexer.get_token()
    
    def eat(self, type_):
        if self.token.type == type_:
            self.token = self.lexer.get_token()
        else:
            raise SyntaxError(f"Expected {type_}")
    
    def expr(self):
        result = self.term()
        while self.token.type in (TokenType.PLUS, TokenType.MINUS):
            if self.token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
                result += self.term()
            else:
                self.eat(TokenType.MINUS)
                result -= self.term()
        return result
    
    def term(self):
        result = self.factor()
        while self.token.type in (TokenType.MUL, TokenType.DIV):
            if self.token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
                result *= self.factor()
            else:
                self.eat(TokenType.DIV)
                result //= self.factor()
        return result
    
    def factor(self):
        if self.token.type == TokenType.NUMBER:
            val = self.token.value
            self.eat(TokenType.NUMBER)
            return val
        elif self.token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            result = self.expr()
            self.eat(TokenType.RPAREN)
            return result
        raise SyntaxError("Unexpected token")

def evaluate(expr):
    return Parser(Lexer(expr)).expr()
