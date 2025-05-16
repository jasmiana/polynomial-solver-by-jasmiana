from .tokenizer import Token, TOKEN_TYPE_NUMBER, TOKEN_TYPE_VARIABLE, TOKEN_TYPE_OPERATOR, TOKEN_TYPE_LPAREN, TOKEN_TYPE_RPAREN

# --- Insert Implicit Multiplication ---

def insert_implicit_multiplication(tokens):
    """
    在需要的地方插入表示隐式乘法的 '*' token。
    例如：'2x' -> '2', '*', 'x'
         '3(x+1)' -> '3', '*', '(', 'x', '+', '1', ')'
         'x(x+1)' -> 'x', '*', '(', 'x', '+', '1', ')'
         '(x+1)(x-1)' -> '(', 'x', '+', '1', ')', '*', '(', 'x', '-', '1', ')'
         '(x+1)x' -> '(', 'x', '+', '1', ')', '*', 'x'
    """
    new_tokens = []
    i = 0
    while i < len(tokens):
        current = tokens[i]
        new_tokens.append(current)

        if i + 1 < len(tokens):
            next = tokens[i+1]

            # 隐式乘法模式：
            # 1. NUMBER 后面跟着 VARIABLE
            # 2. NUMBER 后面跟着 LPAREN
            # 3. VARIABLE 后面跟着 LPAREN
            # 4. RPAREN 后面跟着 LPAREN
            # 5. RPAREN 后面跟着 VARIABLE
            # 6. VARIABLE 后面跟着 NUMBER (例如 x2 这种情况通常无效，但有些约定允许，暂不实现以保持简单)
            # 7. NUMBER 后面跟着 NUMBER (例如 2 3 通常无效，但有些约定允许，暂不实现)

            insert = False
            if current.type == TOKEN_TYPE_NUMBER and next.type == TOKEN_TYPE_VARIABLE:
                insert = True
            elif current.type == TOKEN_TYPE_NUMBER and next.type == TOKEN_TYPE_LPAREN:
                 insert = True
            elif current.type == TOKEN_TYPE_VARIABLE and next.type == TOKEN_TYPE_LPAREN:
                 insert = True
            elif current.type == TOKEN_TYPE_RPAREN and next.type == TOKEN_TYPE_LPAREN:
                 insert = True
            elif current.type == TOKEN_TYPE_RPAREN and next.type == TOKEN_TYPE_VARIABLE:
                 insert = True

            if insert:
                new_tokens.append(Token(TOKEN_TYPE_OPERATOR, '*'))

        i += 1
    return new_tokens
