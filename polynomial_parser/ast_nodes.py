from .polynomial import Polynomial

# --- AST 节点 ---

class Node:
    """AST 节点的基类。"""
    pass


class PolynomialNode(Node):
    """表示多项式或常数（叶子节点）。"""
    def __init__(self, poly: Polynomial):
        if not isinstance(poly, Polynomial):
            raise TypeError("PolynomialNode 的值必须是 Polynomial 对象")
        self.poly = poly

    def __str__(self):
        return str(self.poly) # 使用 Polynomial 的字符串表示


class BinOpNode(Node):
    """表示二元运算符节点 (+, -, *, /)。"""
    def __init__(self, operator: str, left: Node, right: Node):
        if operator not in ['+', '-', '*', '/']:
            raise ValueError(f"不支持的二元运算符: {operator}")
        self.operator = operator
        self.left = left
        self.right = right

    def __str__(self):
        return f"({self.left} {self.operator} {self.right})"


class UnaryOpNode(Node):
    """表示一元运算符节点 (目前主要是负号 -)。"""
    def __init__(self, operator: str, operand: Node):
        if operator not in ['-']:
            raise ValueError(f"不支持的一元运算符: {operator}")
        self.operator = operator
        self.operand = operand

    def __str__(self):
        return f"{self.operator}{self.operand}"
