from .tokenizer import tokenize
from .implicit_multiply import insert_implicit_multiplication
from .parser import Parser
from .evaluator import ASTEvaluator
from .fractional_polynomial import FractionalPolynomial
from .polynomial import Polynomial

# --- 集成解析和求值 ---

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
