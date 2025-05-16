from fractions import Fraction
from .tokenizer import Token, TOKEN_TYPE_NUMBER, TOKEN_TYPE_VARIABLE, TOKEN_TYPE_OPERATOR, TOKEN_TYPE_LPAREN, TOKEN_TYPE_RPAREN, TOKEN_TYPE_EOF, TOKEN_TYPE_MUL_IMPLICIT
from .ast_nodes import Node, PolynomialNode, BinOpNode, UnaryOpNode
from .polynomial import Polynomial

# --- Parser 类 ---

class Parser:
    """
    递归下降解析器，将 token 列表构建成 AST。
    遵循经典的表达式解析语法:
    expression -> term ((+ | -) term)*
    term -> factor ((* | /) factor)*
    factor -> power (^ power)*
    power -> (NUMBER | VARIABLE | '(' expression ')')
    unary_op -> '-' factor (simplified for now, treats leading '-' on factors)
    """
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0

    def current_token(self):
        """返回当前 token。"""
        return self.tokens[self.current_token_index]

    def eat(self, token_type):
        """如果当前 token 类型匹配，则消耗并前进到下一个 token。"""
        if self.current_token().type == token_type:
            self.current_token_index += 1
        else:
            raise SyntaxError(f"期望 {token_type}，但得到 {self.current_token().type} (值: {self.current_token().value})")

    def parse(self):
        """开始解析过程，构建 AST。"""
        node = self.expression()
        if self.current_token().type != TOKEN_TYPE_EOF:
            raise SyntaxError("解析未完成，输入中有多余的 token")
        return node

    def expression(self):
        """解析加法和减法 (最低优先级)。"""
        node = self.term()

        while self.current_token().type == TOKEN_TYPE_OPERATOR and self.current_token().value in ('+', '-'):
            token = self.current_token()
            self.eat(TOKEN_TYPE_OPERATOR)
            right_node = self.term()
            node = BinOpNode(token.value, node, right_node)

        return node

    def term(self):
        """解析乘法和除法。"""
        node = self.factor()

        # 包含 TokenType.MUL_IMPLICIT 来处理隐式乘法
        # 需要从 tokenizer 导入 TokenType.MUL_IMPLICIT
        # from .tokenizer import ..., TOKEN_TYPE_MUL_IMPLICIT
        while self.current_token().type in (TOKEN_TYPE_OPERATOR, TOKEN_TYPE_MUL_IMPLICIT) and \
              (self.current_token().value in ('*', '/') or self.current_token().type == TOKEN_TYPE_MUL_IMPLICIT):
            token = self.current_token()
            op_type = token.type # 存储原始 token 类型

            if op_type == TOKEN_TYPE_OPERATOR:
                if token.value == '*':
                    self.eat(TOKEN_TYPE_OPERATOR)
                elif token.value == '/':
                    self.eat(TOKEN_TYPE_OPERATOR)
            elif op_type == TOKEN_TYPE_MUL_IMPLICIT: # 处理隐式乘法
                 self.eat(TOKEN_TYPE_MUL_IMPLICIT)
                 op_type = TOKEN_TYPE_OPERATOR # 对于 AST 节点，隐式乘法视为常规乘法，使用 TokenType.OPERATOR '*'
                 token.value = '*' # 确保 BinOpNode 使用 '*' 作为操作符值


            # 使用确定的 op_type 和 token.value 创建二元运算符节点
            node = BinOpNode(token.value, node, self.factor())

        return node

    def factor(self):
        """解析基本单元：数字、变量 'x'、括号内的表达式，或带一元负号的单元。"""
        token = self.current_token()

        # 处理一元负号
        if token.type == TOKEN_TYPE_OPERATOR and token.value == '-':
             self.eat(TOKEN_TYPE_OPERATOR)
             operand_node = self.factor() # 负号作用于后面的 factor
             return UnaryOpNode('-', operand_node)

        # 处理括号
        elif token.type == TOKEN_TYPE_LPAREN:
            self.eat(TOKEN_TYPE_LPAREN)
            node = self.expression() # 递归解析括号内的表达式
            self.eat(TOKEN_TYPE_RPAREN)
            return node

        # 处理数字和变量
        elif token.type in (TOKEN_TYPE_NUMBER, TOKEN_TYPE_VARIABLE):
             start_token = self.current_token() # 记录开始的 token

             if token.type == TOKEN_TYPE_NUMBER:
                 self.eat(TOKEN_TYPE_NUMBER)
                 # 将数字 token 转换为 PolynomialNode (常数多项式)
                 try:
                     if '/' in start_token.value:
                         num, den = map(int, start_token.value.split('/'))
                         coeff = Fraction(num, den)
                     else:
                         coeff = Fraction(int(start_token.value))
                     return PolynomialNode(Polynomial({0: coeff}))
                 except (ValueError, TypeError):
                      raise ValueError(f"无效的数字格式: {start_token.value}")

             elif token.type == TOKEN_TYPE_VARIABLE:
                 self.eat(TOKEN_TYPE_VARIABLE)
                 # 解析 'x'，可能是 x^n 的形式
                 exp = 1 # 默认指数是 1
                 if self.current_token().type == TOKEN_TYPE_OPERATOR and self.current_token().value == '^':
                      self.eat(TOKEN_TYPE_OPERATOR) # 消耗 '^'
                      exp_token = self.current_token()
                      if exp_token.type == TOKEN_TYPE_NUMBER:
                           self.eat(TOKEN_TYPE_NUMBER)
                           try:
                               exp = int(exp_token.value)
                               if exp < 0:
                                    raise ValueError("指数不能为负数")
                           except (ValueError, TypeError):
                                raise ValueError(f"无效的指数格式: {exp_token.value}")
                      else:
                           raise SyntaxError(f"期望指数，但得到 {exp_token.type}")

                 # 创建 PolynomialNode (x^exp)
                 return PolynomialNode(Polynomial({exp: Fraction(1)}))

        else:
            raise SyntaxError(f"无法解析的 token: {token}")
