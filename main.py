from polynomial_parser.tokenizer import tokenize
from polynomial_parser.parser import Parser
from polynomial_parser.evaluator import ASTEvaluator
from polynomial_parser.fractional_polynomial import FractionalPolynomial
from polynomial_parser.partial_fraction import partial_fraction_decompose, get_sort_key # Import get_sort_key
from polynomial_parser.polynomial import Polynomial
from polynomial_parser.ast_nodes import BinOpNode, PolynomialNode, UnaryOpNode
from fractions import Fraction
import sympy
from polynomial_parser.formatting import print_decomposed_terms # Import print_decomposed_terms


def solve_expression(expression_string):
    """
    解析并计算一个多项式/分式多项式表达式。
    Args:
        expression_string: 包含数学表达式的字符串。
    Returns:
        一个元组 (ast, result)，ast 是解析后的 AST，result 是 FractionalPolynomial 或 Polynomial 对象。
        如果处理失败，返回 (None, None)。
    """
    try:
        # 1. 词法分析 (Tokenization)
        tokens = tokenize(expression_string)
        # print(f"Tokens: {tokens}") # 打印 token列表查看

        # 2. 语法解析 (Parsing) 和 构建 AST
        parser = Parser(tokens)
        ast = parser.parse()
        # print(f"AST: {ast}") # 打印 AST 查看结构

        # 3. 求值 (Evaluation)
        evaluator = ASTEvaluator()
        result = evaluator.evaluate(ast)

        return ast, result

    except Exception as e:
        print(f"处理表达式时发生错误: {e}")
        return None, None


# Define the symbol for sorting and degree calculation (assuming 'x')
x = sympy.symbols('x')

# Removed get_sort_key and print_decomposed_terms from here

if __name__ == "__main__":

    print("\n多项式 / 分式多项式解析器 v1.1\n")
    print("- 输入表达式，例如：x^2 + 2x + 1 或 (x+1)/(x^2+3x+2)")
    print("- 按 'q' 退出。")
    print("\nPowered By jasmiana - © 2025 jasmiana\n")

    while True:
        try:
            user_input = input(">>> ")

            if user_input.lower() == 'q':
                break

            if not user_input.strip():
                continue

            ast, result = solve_expression(user_input)

            if result is not None: # Proceed if solve_expression was successful
                # Check if the result is a FractionalPolynomial instance
                if isinstance(result, FractionalPolynomial):
                    # Check if the original input AST was a simple division node
                    # A simple division AST has a BinOpNode with '/' as the root,
                    # and its children are PolynomialNodes or simple UnaryOpNodes containing PolynomialNodes
                    is_simple_division_ast = False
                    # Corrected: Use ast.operator instead of ast.op
                    if isinstance(ast, BinOpNode) and ast.operator == '/':
                        # Check if operands are simple enough (e.g., PolynomialNode, or simple UnaryOpNode of PolynomialNode)
                        def is_simple_operand(node):
                            return isinstance(node, PolynomialNode) or (isinstance(node, UnaryOpNode) and isinstance(node.operand, PolynomialNode))

                        if is_simple_operand(ast.left) and is_simple_operand(ast.right):
                             is_simple_division_ast = True
                        # Simpler check: just root is BinOpNode with /
                        # Corrected: Use ast.operator instead of ast.op
                        is_simple_division_ast = isinstance(ast, BinOpNode) and ast.operator == '/'


                    if is_simple_division_ast:
                        # Input was a simple division, directly perform and print partial fraction decomposition
                        # print("\n检测到单个分式输入，直接进行裂项...")
                        try:
                            decomposed_terms = partial_fraction_decompose(result)
                            print("结果:")
                            # Call the helper function to print sorted decomposed terms
                            # Ensure x is accessible (defined outside the loop)
                            print_decomposed_terms(decomposed_terms, x)

                        except Exception as e:
                            print(f"自动裂项过程中发生错误: {e}")
                            import traceback
                            traceback.print_exc()

                    else:
                        # Result is a FractionalPolynomial from a more complex input (sum of fractions, etc.)
                        # Offer the options menu
                        # print("\n- 检测到分式多项式。请选择操作：")
                        choice = input("\n通分 (a) 或裂项 (b) ?  [a/b] \n>>> ").lower() # Added prompt for input

                        if choice == 'a':
                            print("\n通分...")
                            # Print as a single fraction using the dedicated method
                            try:
                                # Ensure to_single_fraction_str is accessible (in FractionalPolynomial class)
                                print(f"结果: {result.to_single_fraction_str()}")
                            except AttributeError:
                                print("警告: FractionalPolynomial 类没有 to_single_fraction_str 方法。打印默认字符串表示。")
                                print(f"结果: {result}") # Fallback

                        elif choice == 'b':
                            print("\n裂项...")
                            try:
                                decomposed_terms = partial_fraction_decompose(result)
                                print("结果:")
                                # Call the helper function to print sorted decomposed terms
                                # Ensure x is accessible (defined outside the loop)
                                print_decomposed_terms(decomposed_terms, x)
                            except Exception as e:
                                print(f"分式裂项过程中发生错误: {e}")
                                import traceback
                                traceback.print_exc()

                        else:
                             print("无效的选项。")

                else:
                    # Result is a Polynomial (not a FractionalPolynomial with non-1 denominator)
                    print(f"结果: {result}") # For simple polynomial results

            print("-" * 20) # Separator printed by print_decomposed_terms or the direct print

        except EOFError:
            print("\n退出程序.")
            break
        except Exception as e:
            print(f"发生意外错误: {e}")
            print("-" * 20)
            