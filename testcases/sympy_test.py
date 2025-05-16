# 导入 SymPy 库中的 symbols 函数
from sympy import symbols, sqrt, pi

# 1. 定义多项式中的变量（例如 'x'）为 SymPy 符号
# 如果需要其他符号，可以在 symbols() 中一起定义，例如：x, y, z = symbols('x y z')
x = symbols('x')

# 2. 创建一个简单的多项式表达式
# 可以直接使用 SymPy 符号和 Python 的运算符来构建表达式
expr1 = x**2 + 2*x + 1

# 也可以包含无理数，SymPy 会自动处理
expr2 = sqrt(2)*x + pi

# 3. 进行计算 (例如，将两个表达式相加)
result_add = expr1 + expr2

# 4. 进行计算 (例如，将表达式 expr1 乘以 x)
result_mul = expr1 * x

# 5. 对表达式进行求值 (例如，当 x = 3 时计算 expr1 的值)
# 使用 subs() 方法替换符号的值
value_at_x_eq_3 = expr1.subs(x, 3)

# 求值包含无理数的表达式 (例如，当 x = sqrt(2) 时计算 result_add 的值)
value_at_x_eq_sqrt2 = result_add.subs(x, sqrt(2))


# 6. 打印结果
print(f"表达式 expr1: {expr1}")
print(f"表达式 expr2: {expr2}")
print(f"expr1 + expr2 的结果: {result_add}")
print(f"expr1 * x 的结果: {result_mul}")
print(f"当 x = 3 时，expr1 的值: {value_at_x_eq_3}")
print(f"当 x = sqrt(2) 时，expr1 + expr2 的值: {value_at_x_eq_sqrt2}")