from fractions import Fraction
from .polynomial import Polynomial
from .polynomial_math import polynomial_gcd

# --- FractionalPolynomial 类 ---

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
        if denominator.is_zero():
            if not numerator.is_zero():
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
        if self.numerator.is_zero():
            self.numerator = Polynomial()
            self.denominator = Polynomial({0: 1})
            return

        gcd = polynomial_gcd(self.numerator, self.denominator)

        # 检查 GCD 是否是常数 1
        if not (gcd.is_constant() and gcd.terms.get(0) == Fraction(1)): # 使用 is_constant 方法
             try:
                 new_numerator, rem_num = self.numerator.divmod_polynomial(gcd)
                 new_denominator, rem_den = self.denominator.divmod_polynomial(gcd)

                 # 检查余数是否为零多项式
                 if not rem_num.is_zero() or not rem_den.is_zero(): # 使用 is_zero 方法
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
             # 检查分母是否是常数且不为 1
             elif self.denominator.is_constant() and den_leading_coeff != 1: # 使用 is_constant 方法
                 constant_factor = den_leading_coeff
                 new_num_terms = {exp: coeff / constant_factor for exp, coeff in self.numerator.terms.items()}
                 new_den_terms = {0: Fraction(1)}

                 self.numerator = Polynomial(new_num_terms)
                 self.denominator = Polynomial(new_den_terms)

    def __str__(self):
        """
        返回分式多项式的字符串表示（混合形式）。
        如果分子次数不小于分母次数，则表示为 多项式部分 + 余数分式 的形式。
        """
        # 确保分母不是零多项式
        if self.denominator.is_zero():
            return "除数不能为零"

        # _simplify is called in __init__, so self.numerator and self.denominator are already simplified

        # If denominator is constant 1, return string representation of numerator polynomial
        if self.denominator.is_constant() and self.denominator.terms.get(0, Fraction(0)) == Fraction(1):
            return str(self.numerator)

        # If numerator degree is less than denominator degree, return the simplified fraction form
        if self.numerator.degree() < self.denominator.degree():
             # Enclose in parentheses to clarify the fraction structure
            return f"({self.numerator}) / ({self.denominator})"

        # If numerator degree is >= denominator degree, perform polynomial long division
        try:
            quotient, remainder = self.numerator.divmod_polynomial(self.denominator)

            # If remainder is the zero polynomial, the result is just the quotient polynomial
            if remainder.is_zero():
                return str(quotient)
            else:
                # Remainder is not zero, result is Quotient + Remainder / Denominator
                quotient_str = str(quotient)
                # Check the sign of the remainder's leading coefficient for display purposes
                # Find the leading coefficient of the remainder
                if remainder.is_zero(): # 如果余数是零多项式，主导系数为 0
                    leading_coefficient = Fraction(0)
                else:
                    highest_degree = max(remainder.terms.keys())
                    leading_coefficient = remainder.terms.get(highest_degree, Fraction(0))

                if leading_coefficient < 0:
                    # 余数最高次项系数为负，使用减号，并在分子部分显示余数的绝对值
                    # 余数多项式的绝对值可以通过乘以 -1 得到
                    abs_remainder = remainder * Polynomial({0: Fraction(-1)})
                    return f"{quotient_str} - ({str(abs_remainder)}) / ({str(self.denominator)})"
                else:
                    # 余数最高次项系数为正或零，使用加号，并在分子部分显示余数本身
                    return f"{quotient_str} + ({str(remainder)}) / ({str(self.denominator)})"


        except ValueError as e:
            # If an error occurs during division (e.g., division by zero, though checked in __init__)
            # Return the original fraction form with an optional warning
            print(f"警告: 字符串表示中多项式除法错误: {e}")
            return f"({self.numerator}) / ({self.denominator})" # Fallback to basic fraction representation

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


        # 注意：Polynomial 的 __truediv__ 和 __rtruediv__ 不应该直接返回 FractionalPolynomial
        # 而是应该依赖 FractionalPolynomial 的 __add__, __sub__ 等方法来处理混合运算
        # 例如 PolynomialA + PolynomialB 在 Polynomial 类中处理，PolynomialA + FractionalB 在 FractionalPolynomial 的 __add__ 中处理
        # 所以 Polynomial 类不再需要直接返回 FractionalPolynomial 的 __truediv__ 和 __rtruediv__ 了。

        # 实际的多项式除法函数仍然是 Polynomial.divmod_polynomial

    # Polynomial 类中的 __truediv__ 和 __rtruediv__ 需要移除，因为它们会导致循环导入
    # FractionalPolynomial 的运算方法会处理与 Polynomial 的混合运算
    # 例如，PolynomialA / PolynomialB 会在 Polynomial.__truediv__ 中返回 NotImplemented
    # 然后 Python 会尝试调用 FractionalPolynomial.__rtruediv__ (如果 PolynomialB 是 FractionalPolynomial)
    # 或者，我们直接在 Polynomial.__truediv__ 中就创建并返回 FractionalPolynomial

    # 让我们修改 Polynomial.__truediv__ 和 __rtruediv__，使它们直接创建 FractionalPolynomial 对象
    # 这意味着 polynomial.py 需要导入 fractional_polynomial.py，再次造成循环导入。

    # 替代方案：将 FractionalPolynomial 的创建逻辑放在一个更顶层的文件，或者将 __truediv__ 的实现放在 FractionalPolynomial 中作为类方法或独立的函数
    # 考虑到 __truediv__ 是 Polynomial 的方法，最 Pythonic 的方式是在 Polynomial 中实现，但需要解决循环导入。
    # 解决循环导入的一种常见方式是局部导入或将相互依赖的代码放入同一个文件。
    # 另一种方式是，在 Polynomial.__truediv__ 中只返回 NotImplemented，依赖 FractionalPolynomial 的 __rtruediv__ 来处理。
    # 让我们选择后者，这更干净。Polynomial 只处理 Polynomial 之间的运算，FractionalPolynomial 处理分式之间的运算以及与 Polynomial 的混合运算。
