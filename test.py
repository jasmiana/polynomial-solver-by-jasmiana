from polynomial_parser.tokenizer import tokenize
from polynomial_parser.parser import Parser
from polynomial_parser.evaluator import ASTEvaluator

def solve_expression(expression_string):
    """
    解析并计算一个多项式/分式多项式表达式。

    Args:
        expression_string: 包含数学表达式的字符串。

    Returns:
        FractionalPolynomial 对象，表示计算结果。
    """
    try:
        # 1. 词法分析 (Tokenization)
        tokens = tokenize(expression_string)
        # print(f"Tokens: {tokens}") # 打印 token 列表查看

        # 2. 语法解析 (Parsing) 和 构建 AST
        parser = Parser(tokens)
        ast = parser.parse()
        # print(f"AST: {ast}") # 打印 AST 查看结构

        # 3. 求值 (Evaluation)
        evaluator = ASTEvaluator()
        result = evaluator.evaluate(ast)

        return result

    except Exception as e:
        print(f"处理表达式时发生错误: {e}")
        return None

if __name__ == "__main__":
    # 示例用法
    expressions = [
        "x + 1",                      # x + 1
        "x * (x + 1)",                # x^2 + x
        "(x + 1) / (x - 1)",          # (x + 1) / (x - 1)
        "x^2 - 1 / (x + 1)",          # x^2 - 1/(x+1) = (x^3 + x^2 - 1)/(x+1)
        "3 * x + 2/3",                # 3*x + 2/3
        "-x^2 + 5",                   # -x^2 + 5
        "(x + 1) * (x - 1) / (x^2 - 1)", # (x^2 - 1) / (x^2 - 1) = 1 (约分)
        "1 + 1/x",                    # 1 + 1/x = (x+1)/x
        "x / x",                      # x/x = 1
        "5",                          # 5
        "1/2",                        # 1/2
        "x^2 / x",                    # x
        "(x^2 - 4) / (x - 2)",        # x + 2 (约分)
        "((x+1)*(x-1))/(x^2-1)",      # 1 (约分)
        "x^2 + 2*x + 1 / (x + 1)",    # x^2 + 2x + 1/(x+1)
        "(x^2 + 2*x + 1) / (x + 1)",  # x + 1 (约分)
        "-(x + 1)",                   # -x - 1
        "2 * -(x + 1)",               # -2x - 2
        "1 - (x + 1)",                # 1 - x - 1 = -x

        # 隐式乘法测试用例
        "2x",                         # 2 * x
        "3(x+1)",                     # 3 * (x+1) = 3x + 3
        "x(x+1)",                     # x * (x+1) = x^2 + x
        "(x+1)(x-1)",                 # (x+1) * (x-1) = x^2 - 1
        "(x+1)x",                     # (x+1) * x = x^2 + x
        "2(x+1) + 3x",                # 2 * (x+1) + 3 * x = 2x + 2 + 3x = 5x + 2
        "x^2(x-1)",                   # x^2 * (x-1) = x^3 - x^2
        "1/2(x+1)",                   # 1/2 * (x+1) = 1/2*x + 1/2
    ]

    for expr in expressions:
        print(f"表达式: {expr}")
        result = solve_expression(expr)
        if result:
            # FractionalPolynomial 的 __str__ 方法会负责格式化输出
            print(f"结果: {result}")
        print("-" * 20)
