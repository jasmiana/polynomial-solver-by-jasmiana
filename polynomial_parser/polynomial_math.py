from fractions import Fraction
from .polynomial import Polynomial

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