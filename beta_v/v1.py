from fractions import Fraction

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
                    self.terms[int(exp)] = Fraction(coeff)
                except (ValueError, TypeError):
                    print(f"警告: 无法将输入 {exp}: {coeff} 转换为有效的多项式项，将忽略。")
                    continue


        # 移除系数为零的项
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
            if coeff == 1 and exp != 0:
                coeff_str = "" # 系数为1且不是常数项，省略1
            elif coeff == -1 and exp != 0:
                coeff_str = "-" # 系数为-1且不是常数项，只显示负号
            else:
                # 使用 Fraction 的字符串表示，如果分母是1则只显示分子
                if coeff.denominator == 1:
                    coeff_str = str(coeff.numerator)
                else:
                    coeff_str = str(coeff) # 显示分数形式

            # 构建变量部分的字符串
            if exp == 0:
                variable_str = "" # 常数项没有变量
            elif exp == 1:
                variable_str = "x" # 指数为1，显示x
            else:
                variable_str = f"x^{exp}" # 指数大于1，显示 x^exp

            # 组合系数和变量
            if exp > 0:
                if coeff_str == "": # 系数为1
                    term_str = variable_str
                elif coeff_str == "-": # 系数为-1
                    term_str = "-" + variable_str
                else:
                     term_str = f"{coeff_str}*{variable_str}" # 其他系数
            else: # exp == 0，常数项
                 term_str = coeff_str

            terms_str.append(term_str)

        # 将各项用 '+' 或 '-' 连接起来
        # 处理正负号和连接符
        final_str = ""
        first_term = True
        for term_str in terms_str:
            if not term_str: # 跳过空字符串项 (应该不会出现，但作为安全检查)
                continue

            # 判断当前项的符号
            starts_with_minus = term_str.startswith('-')
            if starts_with_minus:
                 # 如果项以负号开头，移除负号，方便后面统一处理
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

        # 如果terms_str是空的，说明是零多项式，但开头已经处理了，这里作为二次检查
        if not final_str:
             return "0"

        return final_str


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

    def __sub__(self, other):
        """
        实现多项式减法。
        other: 另一个 Polynomial 对象或 Fraction/int。
        """
        if isinstance(other, (int, Fraction)):
             other = Polynomial({0: other})
        elif not isinstance(other, Polynomial):
            return NotImplemented

        result_terms = self.terms.copy()
        for exp, coeff in other.terms.items():
            result_terms[exp] = result_terms.get(exp, Fraction(0)) - coeff

        return Polynomial(result_terms)

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

        # 检查除数主项系数是否为零（理论上_clean_terms会处理，这里是双重检查）
        if divisor_leading_coeff == 0:
             raise ValueError("除数的主项系数不能为零")

        while remainder.degree() >= other.degree() and remainder.terms:
            remainder_leading_exp, remainder_leading_coeff = remainder._leading_term()

            # 如果余数主项系数为零，且余数不为零多项式，这可能是个问题，但按逻辑它最终会变成零或次数低于除数
            if remainder_leading_coeff == 0:
                 # 理论上 _leading_term 应该返回非零系数的最高次项，除非是零多项式
                 # 如果到达这里，可能是 remainder.terms 不为空但所有系数都是0，_clean_terms应该处理了
                 # 如果是正常情况，余数次数会下降，最终退出循环
                 break

            # 计算商的当前项
            # 系数 = 余数主项系数 / 除数主项系数
            # 指数 = 余数主项指数 - 除数主项指数
            term_coeff = remainder_leading_coeff / divisor_leading_coeff
            term_exp = remainder_leading_exp - divisor_leading_exp

            # 如果计算出的指数小于0，说明无法继续整除，退出循环 (多项式除法要求指数为非负整数)
            if term_exp < 0:
                break # 余数次数已经低于除数

            # 创建商的当前项多项式
            current_quotient_term = Polynomial({term_exp: term_coeff})

            # 将当前项添加到总商中
            # 注意：这里的加法会合并同类项并清理零系数
            quotient = quotient + current_quotient_term

            # 计算 (商的当前项 * 除数)
            term_to_subtract = current_quotient_term * other

            # 从余数中减去这一项
            # 注意：这里的减法会合并同类项并清理零系数
            remainder = remainder - term_to_subtract


        # 确保最终余数是经过清理的
        remainder._clean_terms()
        quotient._clean_terms()

        return (quotient, remainder)


    def __truediv__(self, other):
        """实现多项式除法，返回商。"""
        # 使用 divmod_polynomial 获取商和余数，只返回商
        quotient, remainder = self.divmod_polynomial(other)

        # 如果有余数且余数不是零多项式，则多项式不能整除
        # 根据任务描述，最终结果是多项式，这意味着我们可能只考虑能整除的情况，或者需要引入分式
        # 当前实现只返回商，如果不能整除，余数会被忽略。
        # 如果需要精确的分式结果，我们需要FractionalPolynomial或类似的数据结构
        if remainder.terms:
             print("警告: 多项式不能整除，返回的只是商，余数将被忽略。") # 或者抛出异常

        return quotient

    # TODO: 添加分式表示和运算
    # TODO: 实现完整的解析器
    
