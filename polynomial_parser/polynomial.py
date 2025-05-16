from fractions import Fraction

# --- Polynomial 类 ---

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

    def is_zero(self):
        """判断多项式是否为零多项式。"""
        return not self.terms

    def is_constant(self):
        """判断多项式是否为常数多项式（次数小于等于 0）。"""
        # 零多项式也是常数多项式
        if self.is_zero():
            return True
        # 非零多项式是常数多项式当且仅当其最高次数为 0
        return self.degree() == 0

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

    def power(self, n):
        """
        计算多项式的非负整数次幂。
        n: 非负整数指数。
        """
        if not isinstance(n, int) or n < 0:
            raise ValueError("多项式的指数必须是非负整数")

        if n == 0:
            # 任何非零多项式的 0 次幂是常数 1
            # 零多项式的 0 次幂通常定义为 1，但有时也未定义，我们此处遵循前者
            return Polynomial({0: Fraction(1)})

        if n == 1:
            return self # 1 次幂是多项式本身

        # 使用平方求幂法（Exponentiation by squaring）提高效率
        result = Polynomial({0: Fraction(1)}) # 结果初始化为常数 1
        base = Polynomial(self.terms.copy()) # 复制一份多项式作为乘法的基础

        while n > 0:
            if n % 2 == 1:
                # 如果指数是奇数，将当前结果乘以 base
                result = result * base
            # 将 base 自身平方
            base = base * base
            # 指数减半（整数除法）
            n //= 2

        return result

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

    '''
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
    '''

    def _to_polynomial(self, value):
        if isinstance(value, Polynomial):
            return value
        elif isinstance(value, (int, Fraction)):
            return Polynomial({0: value})
        else:
            raise TypeError(f"无法将类型 {type(value)}转换为 Polynomial")