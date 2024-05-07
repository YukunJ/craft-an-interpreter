"""
1. Modify the code to allow multiple-digit integers in the input, for example “12+3”
2. Add a method that skips whitespace characters 
   so that your calculator can handle inputs with whitespace characters like ” 12 + 3”
3. Modify the code and instead of ‘+’ handle ‘-‘ to evaluate subtractions like “7-5”
"""


# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexcial analysis
INTEGER = 'INTEGER'
PLUS    = 'PLUS'
MINUS   = 'MINUS'
EOF     = 'EOF'

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value
    
    def __str__(self):
        return f'Token({self.type}, {self.value})'
    
    def __repr__(self):
        return self.__str__()
    

class Interpreter:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
    
    def error(self, msg):
        raise Exception(f'Error parsing input, {msg}')
    
    def skip_space(self):
        while self.pos <= len(self.text) -1:
            if self.text[self.pos] == ' ':
                self.pos += 1
                continue
            break
    
    def read_number(self):
        assert self.text[self.pos].isdigit()
        num = 0
        while self.pos < len(self.text) and self.text[self.pos].isdigit():
            num =  10 * num + int(self.text[self.pos])
            self.pos += 1
        return num
            
    def get_next_token(self):
        self.skip_space()
        if self.pos > len(self.text) - 1:
            return Token(EOF, None)
        current_char = self.text[self.pos]
        
        if current_char.isdigit():
            num = self.read_number()
            token = Token(INTEGER, num)
            return token
        
        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        if current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token
        self.error(f'could not parse current_char {current_char} into a token')
    
    def eat(self, token_types):
        if self.current_token.type in token_types:
            self.current_token = self.get_next_token()
        else:
            self.error(f'type mismatch, current_token of type {self.current_token} but expect {token_types}')
    
    def expr(self):
        self.current_token = self.get_next_token()
        
        left = self.current_token
        self.eat([INTEGER])
        
        op = self.current_token
        self.eat([PLUS, MINUS])
        
        right = self.current_token
        self.eat([INTEGER])
        
        if op.type == PLUS:
            result = left.value + right.value
        elif op.type == MINUS:
            result = left.value - right.value
        else:
            self.error(f'Unknown operator type {op}')
        return result

def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            print("Exiting")
            break
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)
        
if __name__ == '__main__':
    main()


        