
# -------- BigInt Implementation --------
class BigInt:
    @staticmethod
    def add(a, b):
        a, b = a[::-1], b[::-1]
        carry = 0
        result = []

        for i in range(max(len(a), len(b))):
            da = int(a[i]) if i < len(a) else 0
            db = int(b[i]) if i < len(b) else 0
            s = da + db + carry
            result.append(str(s % 10))
            carry = s // 10

        if carry:
            result.append(str(carry))

        return ''.join(result[::-1])

    @staticmethod
    def multiply(a, b):
        result = "0"
        b = b[::-1]

        for i, digit in enumerate(b):
            carry = 0
            temp = []

            for d in a[::-1]:
                prod = int(d) * int(digit) + carry
                temp.append(str(prod % 10))
                carry = prod // 10

            if carry:
                temp.append(str(carry))

            temp = ''.join(temp[::-1]) + "0" * i
            result = BigInt.add(result, temp)

        return result


# -------- Lexer --------
class Token:
    NUMBER = 'NUMBER'
    PLUS   = '+'
    MINUS  = '-'
    MUL    = '*'
    LPAREN = '('
    RPAREN = ')'
    EOF    = 'EOF'

    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0

    def get_next_token(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

        if self.pos >= len(self.text):
            return Token(Token.EOF)

        ch = self.text[self.pos]

        if ch.isdigit():
            start = self.pos
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1
            return Token(Token.NUMBER, self.text[start:self.pos])

        self.pos += 1

        if ch == '+': return Token(Token.PLUS)
        if ch == '-': return Token(Token.MINUS)
        if ch == '*': return Token(Token.MUL)
        if ch == '(': return Token(Token.LPAREN)
        if ch == ')': return Token(Token.RPAREN)

        raise Exception(f"Invalid character: {ch}")


# -------- Parser & Interpreter --------
class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current = lexer.get_next_token()

    def eat(self, token_type):
        if self.current.type == token_type:
            self.current = self.lexer.get_next_token()
        else:
            raise Exception("Syntax Error")

    def factor(self):
        token = self.current

        if token.type == Token.NUMBER:
            self.eat(Token.NUMBER)
            return token.value

        if token.type == Token.LPAREN:
            self.eat(Token.LPAREN)
            result = self.expr()
            self.eat(Token.RPAREN)
            return result

        raise Exception("Invalid factor")

    def term(self):
        result = self.factor()

        while self.current.type == Token.MUL:
            self.eat(Token.MUL)
            result = BigInt.multiply(result, self.factor())

        return result

    def expr(self):
        result = self.term()

        while self.current.type == Token.PLUS:
            self.eat(Token.PLUS)
            result = BigInt.add(result, self.term())

        return result


# -------- Main Program --------
def run():
    print("Mini-Language BigInt Calculator")
    print("Type 'exit' to quit")

    while True:
        text = input(">> ")

        if text.lower() == "exit":
            break

        lexer = Lexer(text)
        parser = Parser(lexer)
        result = parser.expr()
        print(result)


if __name__ == "__main__":
    run()
