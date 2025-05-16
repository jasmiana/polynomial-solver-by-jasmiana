from fractions import Fraction
import re

# 引入 Polynomial, polynomial_gcd, AST 节点定义 (假设之前的代码在这里)
# class Polynomial: ...
# def polynomial_gcd(poly1, poly2): ...
# class Node: ...
# class PolynomialNode(Node): ...
# class BinOpNode(Node): ...
# class UnaryOpNode(Node): ...
# class Token: ...
# def tokenize(expression_str): ...
# def insert_implicit_multiplication(tokens): ...
# class Parser: ...
# class ASTEvaluator: ...
# def parse_and_evaluate(expression_str): ...


# --- Polynomial 类定义 (接上面的代码) ---
class Polynomial:
    def __init__(self, terms=None):
        """
        初始化一个多项式。
        terms: 一个字典，键为指数（int），值为系数（Fraction）。
        例如：{2: 3, 1: 2, 0: -1} 表示 3x^2 + 2x - 1
        """
        self.terms = {}
        if terms is not None:
            for exp, coeff in terms.items():
                try:
                    int_exp = int(exp)
                    frac_coeff = Fraction(coeff)
                    if frac_coeff != 0:
                         self.terms[int_exp] = frac_coeff
                except (ValueError, TypeError):
                    pass

        self._clean_terms()

    def _clean_terms(self):
        """移除字典中系数为零的项。"""
        for exp, coeff in list(self.terms.items()):
            if coeff == 0:
                del self.terms[exp]

    def _leading_term(self):
        """返回多项式的最高次项 (指数, 系数)。"""
        if not self.terms:
            return (None, Fraction(0))

        leading_exp = max(self.terms.keys())
        return (leading_exp, self.terms[leading_exp])

    def degree(self):
        """返回多项式的次数。"""
        leading_exp, _ = self._leading_term()
        return leading_exp if leading_exp is not None else -1

    def __str__(self):
        """返回多项式的字符串表示。"""
        if not self.terms:
            return "0"

        sorted_terms = sorted(self.terms.items(), key=lambda item: item[0], reverse=True)

        terms_str = []
        for exp, coeff in sorted_terms:
            if coeff == 0:
                continue

            if coeff.denominator == 1:
                coeff_val_str = str(coeff.numerator)
            else:
                coeff_val_str = str(coeff)

            if exp != 0 and coeff_val_str == "1":
                coeff_str = ""
            elif exp != 0 and coeff_val_str == "-1":
                coeff_str = "-"
            else:
                coeff_str = coeff_val_str

            if exp == 0:
                variable_str = ""
            elif exp == 1:
                variable_str = "x"
            else:
                variable_str = f"x^{exp}"

            if exp > 0:
                if coeff_str == "" or coeff_str == "-":
                    term_str = coeff_str + variable_str
                else:
                     term_str = f"{coeff_str}*{variable_str}"
            else:
                 term_str = coeff_str

            terms_str.append(term_str)

        final_str = ""
        first_term = True
        for term_str in terms_str:
            if not term_str:
                continue

            starts_with_minus = term_str.startswith('-')
            if starts_with_minus:
                term_content = term_str[1:]
            else:
                term_content = term_str

            if first_term:
                if starts_with_minus:
                    final_str += "-" + term_content
                else:
                    final_str += term_content
                first_term = False
            else:
                if starts_with_minus:
                    final_str += " - " + term_content
                else:
                    final_str += " + " + term_content

        return final_str if final_str else "0"

    def __add__(self, other):
        if isinstance(other, (int, Fraction)):
            other = Polynomial({0: other})
        elif not isinstance(other, Polynomial):
            return NotImplemented

        result_terms = self.terms.copy()
        for exp, coeff in other.terms.items():
            result_terms[exp] = result_terms.get(exp, Fraction(0)) + coeff

        return Polynomial(result_terms)

    def __radd__(self, other):
         return self + other

    def __neg__(self):
        return Polynomial({exp: -coeff for exp, coeff in self.terms.items()})

    def __sub__(self, other):
        if isinstance(other, (int, Fraction)):
             other = Polynomial({0: other})
        elif not isinstance(other, Polynomial):
            return NotImplemented
        return self + (-other)

    def __rsub__(self, other):
        if isinstance(other, (int, Fraction)):
            other = Polynomial({0: other})
            return other - self
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (int, Fraction)):
            result_terms = {exp: coeff * Fraction(other) for exp, coeff in self.terms.items()}
            return Polynomial(result_terms)
        elif not isinstance(other, Polynomial):
             return NotImplemented

        result_terms = {}
        for exp1, coeff1 in self.terms.items():
            for exp2, coeff2 in other.terms.items():
                new_exp = exp1 + exp2
                new_coeff = coeff1 * coeff2
                result_terms[new_exp] = result_terms.get(new_exp, Fraction(0)) + new_coeff

        return Polynomial(result_terms)

    def __rmul__(self, other):
        return self * other

    def divmod_polynomial(self, other):
        if not isinstance(other, Polynomial):
            raise TypeError("除数必须是一个 Polynomial 对象")

        if not other.terms:
            if not self.terms:
                 return (Polynomial(), Polynomial())
            else:
                raise ValueError("除数不能是零多项式")


        quotient = Polynomial()
        remainder = Polynomial(self.terms)

        divisor_leading_exp, divisor_leading_coeff = other._leading_term()

        if divisor_leading_coeff == 0:
             raise ValueError("除数的主项系数不能为零")

        while remainder.degree() >= other.degree() and remainder.terms:
            remainder_leading_exp, remainder_leading_coeff = remainder._leading_term()

            if remainder_leading_coeff == 0:
                 break

            term_coeff = remainder_leading_coeff / divisor_leading_coeff
            term_exp = remainder_leading_exp - divisor_leading_exp

            if term_exp < 0:
                break

            current_quotient_term = Polynomial({term_exp: term_coeff})
            quotient = quotient + current_quotient_term
            term_to_subtract = current_quotient_term * other
            remainder = remainder - term_to_subtract

        remainder._clean_terms()
        quotient._clean_terms()

        return (quotient, remainder)

    def __truediv__(self, other):
        if isinstance(other, Polynomial):
             if not other.terms:
                  raise ValueError("除数不能是零多项式")
             return FractionalPolynomial(self, other)
        elif isinstance(other, (int, Fraction)):
             if other == 0:
                  raise ValueError("除数不能为零")
             return FractionalPolynomial(self, Polynomial({0: other}))
        else:
             return NotImplemented

    def __rtruediv__(self, other):
         if isinstance(other, (int, Fraction)):
              num_poly = Polynomial({0: other})
              return FractionalPolynomial(num_poly, self)
         else:
              return NotImplemented

    def _to_polynomial(self, value):
        if isinstance(value, Polynomial):
            return value
        elif isinstance(value, (int, Fraction)):
            return Polynomial({0: value})
        else:
            raise TypeError(f"无法将类型 {type(value)}转换为 Polynomial")

# --- 多项式 GCD 函数 ---
def polynomial_gcd(poly1: Polynomial, poly2: Polynomial) -> Polynomial:
    """
    计算两个多项式的最大公约数 (GCD)，并返回一个首一多项式。
    使用欧几里得算法。
    """
    if not isinstance(poly1, Polynomial) or not isinstance(poly2, Polynomial):
        raise TypeError("输入必须是 Polynomial 对象")

    a = poly1
    b = poly2

    while b.terms:
        try:
            _, remainder = a.divmod_polynomial(b)
            a = b
            b = remainder
        except ValueError:
            print(f"警告: GCD 计算中除法失败，返回当前候选项。a: {a}, b: {b}")
            break

    gcd = a

    if gcd.terms:
        leading_exp, leading_coeff = gcd._leading_term()
        if leading_coeff != 0 and leading_coeff != 1:
             reciprocal_coeff = Fraction(1) / leading_coeff
             monic_gcd_terms = {exp: coeff * reciprocal_coeff for exp, coeff in gcd.terms.items()}
             gcd = Polynomial(monic_gcd_terms)

    return gcd

# --- FractionalPolynomial 类定义 ---
class FractionalPolynomial:
    def __init__(self, numerator: Polynomial, denominator: Polynomial):
        """
        初始化一个分式多项式。
        numerator: 分子 (Polynomial 对象)
        denominator: 分母 (Polynomial 对象)
        """
        if not isinstance(numerator, Polynomial) or not isinstance(denominator, Polynomial):
            raise TypeError("分子和分母必须是 Polynomial 对象")

        # 检查分母是否为零多项式
        if not denominator.terms:
            if not numerator.terms:
                 raise ValueError("分式不能是 0/0 的形式")
            else:
                 raise ValueError("分母不能是零多项式")

        self.numerator = numerator
        self.denominator = denominator

        # 实例化时进行简化
        self._simplify()

    def _simplify(self):
        """
        简化分式多项式。
        通过计算分子和分母的 GCD 并进行约分。
        """
        # 如果分子是零多项式，结果是 0 / D = 0
        if not self.numerator.terms:
            self.numerator = Polynomial()
            self.denominator = Polynomial({0: 1})
            return

        gcd = polynomial_gcd(self.numerator, self.denominator)

        if gcd.degree() > 0 or (gcd.degree() == 0 and gcd.terms.get(0) != Fraction(1)):
             try:
                 new_numerator, rem_num = self.numerator.divmod_polynomial(gcd)
                 new_denominator, rem_den = self.denominator.divmod_polynomial(gcd)

                 if rem_num.terms or rem_den.terms:
                     print("警告: 约分后余数不为零，可能存在问题。")

                 self.numerator = new_numerator
                 self.denominator = new_denominator

             except ValueError as e:
                 print(f"约分过程中发生错误: {e}")

        if self.denominator.terms:
             den_leading_exp, den_leading_coeff = self.denominator._leading_term()
             if den_leading_coeff < 0:
                 self.numerator = self.numerator * -1
                 self.denominator = self.denominator * -1
             elif den_leading_coeff != 1 and den_leading_exp == 0:
                 constant_factor = den_leading_coeff
                 new_num_terms = {exp: coeff / constant_factor for exp, coeff in self.numerator.terms.items()}
                 new_den_terms = {0: Fraction(1)}

                 self.numerator = Polynomial(new_num_terms)
                 self.denominator = Polynomial(new_den_terms)

    def __str__(self):
        """返回分式多项式的字符串表示（混合形式）。"""
        # 如果分母是常数多项式 1，直接返回分子多项式的字符串表示
        if len(self.denominator.terms) == 1 and self.denominator.terms.get(0) == Fraction(1):
            return str(self.numerator)

        # 如果分子次数小于分母次数，或者分子是零多项式（已在 _simplify 中处理为 0/1）
        # 保持原有的分式形式
        if self.numerator.degree() < self.denominator.degree():
             # 用括号括起来以明确分式结构
            return f"({self.numerator}) / ({self.denominator})"

        # 如果分子次数大于等于分母次数且分母不是常数 1，执行多项式除法
        try:
            quotient, remainder = self.numerator.divmod_polynomial(self.denominator)

            # 如果余数为零多项式，结果就是商多项式
            if not remainder.terms:
                return str(quotient)
            else:
                # 余数不为零，结果是 商 + 余数/除数
                # 规范化余数分式 (可以创建一个临时的 FractionalPolynomial 来利用其简化和字符串表示)
                remainder_fraction = FractionalPolynomial(remainder, self.denominator)

                # 组合商和余数分式字符串
                # 如果商是零多项式，只显示余数分式
                if not quotient.terms:
                    return str(remainder_fraction)
                else:
                    # 如果商不是零多项式，显示 商 + 余数分式
                    # 余数分式本身带括号，所以连接时需要判断余数分式的字符串表示是否需要 '+'
                    # FractionalPolynomial 的 __str__ 已经处理了余数分式的格式，包括正负号和括号。
                    # 我们只需要将商的字符串和余数分式字符串连接起来。
                    # 如果余数分式的字符串表示以 '-' 开头，我们用 " - " 连接
                    # 否则用 " + " 连接
                    remainder_str = str(remainder_fraction)
                    if remainder_str.startswith('-'):
                         return f"{quotient} - {remainder_str[1:]}" # 移除余数分式字符串开头的 '-'
                    else:
                        return f"{quotient} + {remainder_str}"


        except ValueError as e:
            # 如果除法过程中发生错误（例如分母为零，虽然已在 __init__ 检查）
            # 返回原始的分式形式并附带错误信息（可选）
            print(f"警告: 字符串表示中多项式除法错误: {e}")
            return f"({self.numerator}) / ({self.denominator})" # 回退到基本分式表示

    # --- 算术运算 ---
    # (FractionalPolynomial 类的算术运算方法 (__add__, __sub__, __mul__, __truediv__, __radd__, __rsub__, __rmul__, __rtruediv__) 保持不变)

    def __add__(self, other):
        if isinstance(other, (Polynomial, int, Fraction)):
            other = FractionalPolynomial(self._to_polynomial(other), Polynomial({0: 1}))
        elif not isinstance(other, FractionalPolynomial):
            return NotImplemented

        new_numerator = self.numerator * other.denominator + other.numerator * self.denominator
        new_denominator = self.denominator * other.denominator

        return FractionalPolynomial(new_numerator, new_denominator)

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, (Polynomial, int, Fraction)):
             other = FractionalPolynomial(self._to_polynomial(other), Polynomial({0: 1}))
        elif not isinstance(other, FractionalPolynomial):
            return NotImplemented

        new_numerator = self.numerator * other.denominator - other.numerator * self.denominator
        new_denominator = self.denominator * other.denominator

        return FractionalPolynomial(new_numerator, new_denominator)

    def __rsub__(self, other):
        """反向减法: other - self"""
        if isinstance(other, (int, Fraction)):
             other = FractionalPolynomial(self._to_polynomial(other), Polynomial({0: 1}))
             return other - self
        return NotImplemented

    def __mul__(self, other):
        if isinstance(other, (Polynomial, int, Fraction)):
             other = FractionalPolynomial(self._to_polynomial(other), Polynomial({0: 1}))
        elif not isinstance(other, FractionalPolynomial):
            return NotImplemented

        new_numerator = self.numerator * other.numerator
        new_denominator = self.denominator * other.denominator

        return FractionalPolynomial(new_numerator, new_denominator)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        if isinstance(other, (Polynomial, int, Fraction)):
             other = FractionalPolynomial(self._to_polynomial(other), Polynomial({0: 1}))
        elif not isinstance(other, FractionalPolynomial):
            return NotImplemented

        if not other.numerator.terms:
            raise ValueError("除数不能是零")

        new_numerator = self.numerator * other.denominator
        new_denominator = self.denominator * other.numerator

        return FractionalPolynomial(new_numerator, new_denominator)

    def __rtruediv__(self, other):
        """反向除法: other / self"""
        if isinstance(other, (int, Fraction)):
             other = FractionalPolynomial(self._to_polynomial(other), Polynomial({0: 1}))
             return other / self
        return NotImplemented

    def _to_polynomial(self, value):
        """将 int, Fraction, Polynomial 转换为 Polynomial 对象"""
        if isinstance(value, Polynomial):
            return value
        elif isinstance(value, (int, Fraction)):
            return Polynomial({0: value})
        else:
            raise TypeError(f"无法将类型 {type(value)} 转换为 Polynomial")


# --- AST 节点定义 (保持不变) ---
class Node:
    """AST 节点的基类。"""
    pass

class PolynomialNode(Node):
    """表示多项式或常数（叶子节点）。"""
    def __init__(self, poly: Polynomial):
        if not isinstance(poly, Polynomial):
            raise TypeError("PolynomialNode 的值必须是 Polynomial 对象")
        self.poly = poly

    def __str__(self):
        return str(self.poly) # 使用 Polynomial 的字符串表示

class BinOpNode(Node):
    """表示二元运算符节点 (+, -, *, /)。"""
    def __init__(self, operator: str, left: Node, right: Node):
        if operator not in ['+', '-', '*', '/']:
            raise ValueError(f"不支持的二元运算符: {operator}")
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"

class UnaryOpNode(Node):
    """表示一元运算符节点 (目前主要是负号 -)。"""
    def __init__(self, operator: str, operand: Node):
        if operator not in ['-']:
            raise ValueError(f"不支持的一元运算符: {operator}")
        self.operator = operator
        self.operand = operand

    def __str__(self):
        return f"{self.operator}{self.operand}"


# --- Tokenizer (保持不变) ---
# 定义 token 类型
TOKEN_TYPE_NUMBER = 'NUMBER' # 整数或分数
TOKEN_TYPE_VARIABLE = 'VARIABLE' # 'x'
TOKEN_TYPE_OPERATOR = 'OPERATOR' # +, -, *, /, ^
TOKEN_TYPE_LPAREN = 'LPAREN'   # (
TOKEN_TYPE_RPAREN = 'RPAREN'   # )
TOKEN_TYPE_EOF = 'EOF'         # End of File

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
    将数学表达式字符串分解成 token 列表。
    """
    tokens = []
    token_patterns = {
        TOKEN_TYPE_NUMBER: r'\d+(\/\d+)?', # 匹配整数或分数 (如 3 或 1/2)
        TOKEN_TYPE_VARIABLE: r'x',
        TOKEN_TYPE_OPERATOR: r'[\+\-\*\/\^]',
        TOKEN_TYPE_LPAREN: r'\(',
        TOKEN_TYPE_RPAREN: r'\)',
    }

    token_regex = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_patterns.items()))

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

            tokens.append(Token(token_type, token_value))
            i = match.end()
        else:
            raise ValueError(f"无法识别的字符: {expression_str[i]} 在位置 {i}")

    tokens.append(Token(TOKEN_TYPE_EOF))
    return tokens

# --- Insert Implicit Multiplication (保持不变) ---
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


# --- Parser (保持不变) ---
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

        while self.current_token().type == TOKEN_TYPE_OPERATOR and self.current_token().value in ('*', '/'):
            token = self.current_token()
            self.eat(TOKEN_TYPE_OPERATOR)
            right_node = self.factor()
            node = BinOpNode(token.value, node, right_node)

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


# --- AST Evaluator (保持不变) ---
class ASTEvaluator:
    """遍历 AST 并求值。"""
    def evaluate(self, node: Node):
        """根据节点类型递归求值。"""
        if isinstance(node, PolynomialNode):
            return FractionalPolynomial(node.poly, Polynomial({0: 1}))

        elif isinstance(node, BinOpNode):
            left_val = self.evaluate(node.left)
            right_val = self.evaluate(node.right)

            # 左右子节点的值应该是 FractionalPolynomial 对象
            if not isinstance(left_val, FractionalPolynomial) or not isinstance(right_val, FractionalPolynomial):
                 raise TypeError("二元运算符的操作数必须是 FractionalPolynomial")

            if node.operator == '+':
                return left_val + right_val
            elif node.operator == '-':
                return left_val - right_val
            elif node.operator == '*':
                return left_val * right_val
            elif node.operator == '/':
                return left_val / right_val
            else:
                raise ValueError(f"未知运算符: {node.operator}")

        elif isinstance(node, UnaryOpNode):
            operand_val = self.evaluate(node.operand)

            if not isinstance(operand_val, FractionalPolynomial):
                 raise TypeError("一元运算符的操作数必须是 FractionalPolynomial")

            if node.operator == '-':
                return FractionalPolynomial(operand_val.numerator * -1, operand_val.denominator)
            else:
                raise ValueError(f"未知一元运算符: {node.operator}")

        else:
            raise TypeError(f"无法识别的 AST 节点类型: {type(node)}")


# --- 集成解析和求值 (保持不变) ---

def parse_and_evaluate(expression_str: str) -> FractionalPolynomial:
    """
    解析数学表达式字符串，构建 AST，然后求值，返回最终的 FractionalPolynomial。
    """
    try:
        # 1. Tokenize
        tokens = tokenize(expression_str)
        # print("Tokens before implicit multiply:", tokens) # Debugging

        # 2. Insert implicit multiplication tokens
        tokens_with_implicit = insert_implicit_multiplication(tokens)
        # print("Tokens after implicit multiply:", tokens_with_implicit) # Debugging

        # 3. Parse tokens into AST
        parser = Parser(tokens_with_implicit)
        ast = parser.parse()
        # print("AST:", ast) # Debugging

        # 4. Evaluate AST
        evaluator = ASTEvaluator()
        result = evaluator.evaluate(ast)
        return result
    except (ValueError, SyntaxError, TypeError) as e:
        print(f"解析或求值错误: {e}")
        raise # 重新抛出异常
