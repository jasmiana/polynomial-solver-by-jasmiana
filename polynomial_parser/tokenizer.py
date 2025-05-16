import re

# --- Tokenizer ---

# 定义 token 类型
TOKEN_TYPE_NUMBER = 'NUMBER' # 整数或分数
TOKEN_TYPE_VARIABLE = 'VARIABLE' # 'x'
TOKEN_TYPE_OPERATOR = 'OPERATOR' # +, -, *, /, ^
TOKEN_TYPE_LPAREN = 'LPAREN'   # (
TOKEN_TYPE_RPAREN = 'RPAREN'   # )
TOKEN_TYPE_EOF = 'EOF'         # End of File
TOKEN_TYPE_MUL_IMPLICIT = 'MUL_IMPLICIT' # 隐式乘法 token

class Token:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}, {self.value})"

    def __repr__(self):
        return self.__str__()


def tokenize(expression_str):
    """
    将数学表达式字符串分解成 token 列表，处理隐式乘法。
    """
    tokens = []
    # Combine patterns, order matters (e.g., operators before single chars)
    token_patterns = [
        (TOKEN_TYPE_NUMBER, r'\d+(\/\d+)?'), # 匹配整数或分数 (如 3 或 1/2)
        (TOKEN_TYPE_OPERATOR, r'[\+\-\*\/\^]'), # Operators should be before VARIABLE to avoid 'x' matching '-'
        (TOKEN_TYPE_VARIABLE, r'x'),
        (TOKEN_TYPE_LPAREN, r'\('),
        (TOKEN_TYPE_RPAREN, r'\)'),
    ]

    full_pattern = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_patterns)
    token_regex = re.compile(full_pattern)

    i = 0
    while i < len(expression_str):
        # 显式跳过空格
        if expression_str[i].isspace():
            i += 1
            continue

        match = token_regex.match(expression_str, i)
        if match:
            token_type = match.lastgroup
            token_value = match.group(token_type)

            # 在添加当前 token 之前，检查是否需要插入隐式乘法 token
            if tokens: # 仅当已存在 token 时进行检查
                last_token_type = tokens[-1].type
                # 检查当前匹配到的 token 类型，以及它在原字符串中的起始位置
                current_match_start = match.start()

                insert_mul_implicit = False
                # 条件：前一个 token 是数字、变量或右括号，且当前匹配的字符是左括号或变量
                if last_token_type in (TOKEN_TYPE_NUMBER, TOKEN_TYPE_VARIABLE, TOKEN_TYPE_RPAREN) and \
                   expression_str[current_match_start] in ('x', '('):
                    insert_mul_implicit = True
                # 特殊情况：前一个 token 是数字，当前匹配到变量 'x'
                elif last_token_type == TOKEN_TYPE_NUMBER and expression_str[current_match_start] == 'x':
                     insert_mul_implicit = True
                # 特殊情况：前一个 token 是变量，当前匹配到左括号
                elif last_token_type == TOKEN_TYPE_VARIABLE and expression_str[current_match_start] == '(':
                     insert_mul_implicit = True
                # 特殊情况：前一个 token 是右括号，当前匹配到变量 'x' 或 左括号 '('
                elif last_token_type == TOKEN_TYPE_RPAREN and expression_str[current_match_start] in ('x', '('):
                     insert_mul_implicit = True


                # 如果需要插入隐式乘法 token，则插入一个
                if insert_mul_implicit:
                    tokens.append(Token(TOKEN_TYPE_MUL_IMPLICIT, '*'))

            # 添加当前 token
            tokens.append(Token(token_type, token_value))
            i = match.end()
        else:
            raise ValueError(f"无法识别的字符: {expression_str[i]} 在位置 {i}")

    tokens.append(Token(TOKEN_TYPE_EOF))
    return tokens