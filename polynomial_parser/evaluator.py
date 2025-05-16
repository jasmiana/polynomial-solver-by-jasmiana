from .ast_nodes import Node, PolynomialNode, BinOpNode, UnaryOpNode
from .fractional_polynomial import FractionalPolynomial
from .polynomial import Polynomial 

# --- AST Evaluator 类 ---

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
