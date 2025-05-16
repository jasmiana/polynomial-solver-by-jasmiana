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
    print("\n多项式 / 分式多项式化简 v1.0\n")
    print("- 输入表达式，例如：x^2 + 2x + 1")
    print("- 输入 'quit' 或 'exit' 退出。")
    print("\nPowered By jasmiana - © 2025 jasmiana\n")

    while True:
        try:
            user_input = input(">>> ")

            if user_input.lower() in ('quit', 'exit'):
                break

            if not user_input.strip():
                continue

            result = solve_expression(user_input)

            if result:
                print(f"结果: {result}")
            print("-" * 20)

        except EOFError:
            print("\n退出程序.")
            break
        except Exception as e:
            print(f"发生意外错误: {e}")
            print("-" * 20)
