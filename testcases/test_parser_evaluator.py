from polynomial_parser import parse_and_evaluate

# --- 测试解析器和求值器 ---
print("\n--- 测试解析器和求值器 ---")

expressions_to_test = [
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

    # 新增隐式乘法测试用例
    "2x",                         # 2 * x
    "3(x+1)",                     # 3 * (x+1) = 3x + 3
    "x(x+1)",                     # x * (x+1) = x^2 + x
    "(x+1)(x-1)",                 # (x+1) * (x-1) = x^2 - 1
    "(x+1)x",                     # (x+1) * x = x^2 + x
    "2(x+1) + 3x",                # 2 * (x+1) + 3 * x = 2x + 2 + 3x = 5x + 2
    "x^2(x-1)",                   # x^2 * (x-1) = x^3 - x^2
    "1/2(x+1)",                   # 1/2 * (x+1) = 1/2*x + 1/2
]

for expr in expressions_to_test:
    print(f"输入: '{expr}'")
    try:
        result_fp = parse_and_evaluate(expr)
        print(f"结果: {result_fp}")
        print("-" * 30)
    except Exception as e:
         print(f"处理失败: {e}")
         print("-" * 30)


# 更多复杂的例子
expressions_to_test_complex = [
     "((x+1)/(x-1)) + ((x-1)/(x+1))", # (x^2+2x+1 + x^2-2x+1) / (x^2-1) = (2x^2+2)/(x^2-1)
    "(x^3-4x^2+6x+7) / (x^2+2x+4)",
    "(-x^4-2x^2+x-8) / (x+1) + (2x^5+3x^4+4x^2+5) / (x^2+5)",
    "(2x^5+3x^4+4x^2+5) / (x^2+5)",
    "(x^7+8x^5-9x^4-18x^2+3) / (x^2-9x-7)"
]

for expr in expressions_to_test_complex:
     print(f"输入: '{expr}'")
     try:
         result_fp = parse_and_evaluate(expr)
         print(f"结果: {result_fp}")
         print("-" * 30)
     except Exception as e:
          print(f"处理失败: {e}")
          print("-" * 30)
          
          