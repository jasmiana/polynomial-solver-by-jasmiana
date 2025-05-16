from fractions import Fraction
import re # 导入正则表达式模块

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
                # 确保系数是 Fraction 类型，并处理可能的非数字输入
                try:
                    # 将指数转换为整数
                    int_exp = int(exp)
                    # 将系数转换为 Fraction
                    frac_coeff = Fraction(coeff)
                    # 如果系数为零，不添加到 terms 中
                    if frac_coeff != 0:
                         self.terms[int_exp] = frac_coeff
                except (ValueError, TypeError):
                    # 忽略无法转换为有效项的输入
                    # print(f"警告: 无法将输入 {exp}: {coeff} 转换为有效的多项式项，将忽略。")
                    pass # 在解析器中处理错误可能更合适


        # 移除系数为零的项（如果初始化时terms中有零系数项）
        self._clean_terms()

    def _clean_terms(self):
        """移除字典中系数为零的项。"""
        # 使用 items() 的列表拷贝进行迭代，避免在迭代时修改字典
        for exp, coeff in list(self.terms.items()):
            if coeff == 0:
                del self.terms[exp]

    def _leading_term(self):
        """返回多项式的最高次项 (指数, 系数)。"""
        if not self.terms:
            return (None, Fraction(0)) # 零多项式没有最高次项

        # 找到最高的指数
        leading_exp = max(self.terms.keys())
        return (leading_exp, self.terms[leading_exp])

    def degree(self):
        """返回多项式的次数。"""
        leading_exp, _ = self._leading_term()
        return leading_exp if leading_exp is not None else -1 # 零多项式的次数习惯上认为是 -1

    def __str__(self):
        """返回多项式的字符串表示。"""
        if not self.terms:
            return "0" # 零多项式

        # 按指数降序排序项
        sorted_terms = sorted(self.terms.items(), key=lambda item: item[0], reverse=True)

        terms_str = []
        for exp, coeff in sorted_terms:
            if coeff == 0:
                continue # 跳过系数为零的项

            # 构建系数部分的字符串
            # 使用 Fraction 的字符串表示，如果分母是1则只显示分子
            if coeff.denominator == 1:
                coeff_val_str = str(coeff.numerator)
            else:
                coeff_val_str = str(coeff) # 显示分数形式


            # 处理系数为 1 或 -1 的情况，除非是常数项
            if exp != 0 and coeff_val_str == "1":
                coeff_str = ""
            elif exp != 0 and coeff_val_str == "-1":
                coeff_str = "-"
            else:
                coeff_str = coeff_val_str

            # 构建变量部分的字符串
            if exp == 0:
                variable_str = "" # 常数项没有变量
            elif exp == 1:
                variable_str = "x" # 指数为1，显示x
            else:
                variable_str = f"x^{exp}" # 指数大于1，显示 x^exp

            # 组合系数和变量
            if exp > 0:
                if coeff_str == "" or coeff_str == "-": # 系数为 1 或 -1
                    term_str = coeff_str + variable_str
                else:
                     term_str = f"{coeff_str}*{variable_str}" # 其他系数
            else: # exp == 0，常数项
                 term_str = coeff_str

            terms_str.append(term_str)

        # 将各项用 '+' 或 '-' 连接起来
        final_str = ""
        first_term = True
        for term_str in terms_str:
            if not term_str:
                continue

            # 判断当前项的符号
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
        """
        实现多项式加法。
        other: 另一个 Polynomial 对象或 Fraction/int。
        """
        if isinstance(other, (int, Fraction)):
            # 如果是数字，将其视为常数多项式
            other = Polynomial({0: other})
        elif not isinstance(other, Polynomial):
            return NotImplemented # 支持与其他类型进行加法，如果需要

        result_terms = self.terms.copy()
        for exp, coeff in other.terms.items():
            result_terms[exp] = result_terms.get(exp, Fraction(0)) + coeff

        return Polynomial(result_terms)

    def __radd__(self, other):
         """实现反向加法，使得 int/Fraction + Polynomial 也能工作"""
         return self + other # 加法是可交换的

    def __neg__(self):
        """实现取反运算 -Polynomial"""
        return Polynomial({exp: -coeff for exp, coeff in self.terms.items()})

    def __sub__(self, other):
        """
        实现多项式减法。
        other: 另一个 Polynomial 对象或 Fraction/int。
        """
        if isinstance(other, (int, Fraction)):
             other = Polynomial({0: other})
        elif not isinstance(other, Polynomial):
            return NotImplemented

        # 减法相当于加上对方的负数
        return self + (-other)

    def __rsub__(self, other):
        """实现反向减法"""
        if isinstance(other, (int, Fraction)):
            other = Polynomial({0: other})
            return other - self # other - self
        return NotImplemented


    def __mul__(self, other):
        """
        实现多项式乘法。
        other: 另一个 Polynomial 对象或 Fraction/int。
        """
        if isinstance(other, (int, Fraction)):
            # 如果是数字，乘以多项式的每一个系数
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
        """实现反向乘法"""
        return self * other # 乘法是可交换的

    def divmod_polynomial(self, other):
        """
        实现多项式除法，返回商和余数。
        other: 除数，另一个 Polynomial 对象。
        返回: (商 Polynomial, 余数 Polynomial)
        """
        if not isinstance(other, Polynomial):
            raise TypeError("除数必须是一个 Polynomial 对象")

        # 检查除数是否为零多项式
        if not other.terms:
            raise ValueError("除数不能是零多项式")

        quotient = Polynomial()
        remainder = Polynomial(self.terms) # 从被除数开始

        divisor_leading_exp, divisor_leading_coeff = other._leading_term()

        # 检查除数主项系数是否为零
        if divisor_leading_coeff == 0:
             raise ValueError("除数的主项系数不能为零")

        while remainder.degree() >= other.degree() and remainder.terms:
            remainder_leading_exp, remainder_leading_coeff = remainder._leading_term()

            # 如果余数主项系数为零，且余数不为零多项式，这可能是个问题，但按逻辑它最终会变成零或次数低于除数
            # 实际上，_leading_term 应该返回非零系数的最高次项，除非是零多项式。
            if remainder_leading_coeff == 0:
                 break


            # 计算商的当前项
            term_coeff = remainder_leading_coeff / divisor_leading_coeff
            term_exp = remainder_leading_exp - divisor_leading_exp

            # 如果计算出的指数小于0，说明无法继续整除 (多项式除法要求指数为非负整数)
            if term_exp < 0:
                break # 余数次数已经低于除数

            # 创建商的当前项多项式
            current_quotient_term = Polynomial({term_exp: term_coeff})

            # 将当前项添加到总商中
            quotient = quotient + current_quotient_term

            # 计算 (商的当前项 * 除数)
            term_to_subtract = current_quotient_term * other

            # 从余数中减去这一项
            remainder = remainder - term_to_subtract


        # 确保最终余数是经过清理的
        remainder._clean_terms()
        quotient._clean_terms()


        return (quotient, remainder)


    def __truediv__(self, other):
        """实现多项式除法，返回商。"""
        # 使用 divmod_polynomial 获取商和余数，只返回商
        quotient, remainder = self.divmod_polynomial(other)

        # 如果有余数且余数不是零多项式，根据任务描述，最终结果是多项式，意味着我们可能只考虑能整除的情况。
        # 如果需要精确的分式结果，我们需要FractionalPolynomial或类似的数据结构
        if remainder.terms:
             # print("警告: 多项式不能整除，返回的只是商，余数将被忽略。") # 移除警告，按任务要求返回多项式
             pass # 如果有余数，不进行额外处理，只返回商


        return quotient

    # TODO: 添加分式表示和运算 (FractionalPolynomial 类)
    # TODO: 完善解析器以处理更复杂的输入，包括分式和括号

# --- 解析器函数 ---

def parse_polynomial(expression_str):
    """
    改进的解析器，支持形如 a*x^n, ax^n, ax 等项，并处理加减。
    Uses replace and split, handles leading '-' and empty terms.
    Still no brackets or complex fractions.
    Adds basic implicit multiply handling (e.g., 2x, -5x^2).
    """
    # Remove all spaces
    expression_str = expression_str.replace(" ", "")

    if not expression_str:
        return Polynomial() # Empty string represents zero polynomial

    # Add a dummy '0' term at the start if the expression begins with '-' or '+'
    # This simplifies splitting. We can remove the dummy term's effect later.
    if expression_str.startswith('-') or expression_str.startswith('+'):
         expression_str = '0' + expression_str

    # Replace '-' with '+-' to use '+' as a universal delimiter for splitting terms
    expression_str = expression_str.replace("-", "+-")


    # Split by '+'
    terms_list = expression_str.split("+")

    parsed_terms = {} # Stores {exponent: coefficient}

    for term_str in terms_list:
        term_str = term_str.strip()

        if not term_str or term_str == '0': # Skip empty terms and the dummy '0' term
            continue

        # Now term_str should be like "3*x^2", "-x^3", "x", "7", "1/2*x", "2x", "-5x^2" etc.
        # The sign that was part of the original term is preserved (e.g., "-x^3")

        coeff_part_str = ""
        variable_part_str = ""
        exp = 0
        coeff = Fraction(0)

        # Handle the sign of the term first
        term_sign = 1
        if term_str.startswith('-'):
             term_sign = -1
             term_str = term_str[1:] # Remove the leading '-'

        if not term_str: # Handle cases like a term that was just "-" after removing sign
             raise ValueError("Invalid term: just '-'")


        # Find where the coefficient part ends and the variable part begins (if 'x' is present)
        x_index = term_str.find('x')

        if '*' in term_str: # Explicit multiplication
            parts = term_str.split('*')
            if len(parts) == 2:
                coeff_part_str = parts[0]
                variable_part_str = parts[1] # Re-determine variable part after '*' split
                if not variable_part_str.startswith('x'):
                    raise ValueError(f"无效的变量部分 after '*': {variable_part_str} in term {term_str}")
            else:
                raise ValueError(f"无效的项格式 (多个 '*'): {term_str}")

        elif x_index != -1: # 'x' is present, implicit multiplication or just 'x' / 'x^n'
             # The part before 'x' is the coefficient string (can be empty)
             coeff_part_str = term_str[:x_index]
             variable_part_str = term_str[x_index:] # Part from 'x' onwards

             # If coeff_part_str is empty, the coefficient number is 1.
             if coeff_part_str == "":
                  numerical_coeff_part = "1"
             # If coeff_part_str is just '-', this was handled by term_sign
             # If it's something else, it should be a number or fraction string
             else:
                 numerical_coeff_part = coeff_part_str

             coeff_part_str = numerical_coeff_part # Use the determined numerical part for parsing Fraction

             # Parse exponent from variable_part_str
             if variable_part_str == 'x':
                 exp = 1
             elif variable_part_str.startswith('x^'):
                try:
                     exp = int(variable_part_str[2:])
                     if exp < 0:
                        raise ValueError("指数不能为负数") # Ensure exponent is non-negative
                except (ValueError, IndexError):
                    raise ValueError(f"无效的指数格式: {variable_part_str} in term {term_str}")
             else:
                  raise ValueError(f"无效的变量格式: {variable_part_str} in term {term_str}")

        else: # No 'x' and no '*', it's a constant term
            coeff_part_str = term_str
            variable_part_str = "" # Explicitly empty variable part
            exp = 0 # Exponent is 0 for constant term


        # Now parse the coefficient string
        try:
            if '/' in coeff_part_str:
                num_den = coeff_part_str.split('/')
                if len(num_den) == 2:
                    coeff = Fraction(int(num_den[0]), int(num_den[1]))
                else:
                     raise ValueError(f"无效的分数格式: {coeff_part_str} in term {term_str}")
            elif coeff_part_str: # Ensure it's not empty after being set to "1" if needed
                coeff = Fraction(int(coeff_part_str))
            else:
                # If coeff_part_str is empty here, it means there was a variable part
                # and coeff_part_str was "", which should have been handled as numerical_coeff_part="1"
                # So this else should ideally not be reached with variable_part.
                # If variable_part is empty, and coeff_part is empty, it's an error unless the original term_str was "0"
                if not variable_part_str: # Empty coeff_part_str and empty variable_part_str
                     raise ValueError(f"无法解析的项: {term_str}")
                # If coeff_part_str is empty and variable_part_str is not, this was handled above.


        except (ValueError, TypeError):
             raise ValueError(f"无效的系数或常数项格式: {coeff_part_str} in term {term_str}")


        # Apply the term sign that was determined first
        coeff *= term_sign


        # Add the parsed term to the dictionary, merging coefficients if exponent exists
        parsed_terms[exp] = parsed_terms.get(exp, Fraction(0)) + coeff

    # Create a Polynomial object from the parsed terms
    return Polynomial(parsed_terms)


