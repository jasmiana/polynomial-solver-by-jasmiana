from v2 import *

# --- 测试改进的解析器 v5 ---
print("\n--- 测试改进的解析器 v5 ---")
poly_str1_v5 = "3*x^2 + x - 5" # 期待: 3*x^2 + x - 5
poly_str2_v5 = "-x^3 + 2/3*x + 7"  # 期待: -x^3 + 2/3*x + 7
poly_str3_v5 = "1/2*x^4"          # 期待: 1/2*x^4
poly_str4_v5 = "-10"             # 期待: -10
poly_str5_v5 = "x"               # 期待: x
poly_str6_v5 = "-x"              # 期待: -x
poly_str7_v5 = "5/2"             # 期待: 5/2
poly_str8_v5 = "x^2 - 1"         # 期待: x^2 - 1
poly_str9_v5 = "x^3+8"          # 期待: x^3 + 8
poly_str10_v5 = "-x^2-x+1"      # 期待: -x^2 - x + 1
poly_str11_v5 = "2x" # Test implicit multiply (should work)
poly_str12_v5 = "-5x^2" # Test implicit multiply with sign (should work)
poly_str13_v5 = "x + 1/2*x^2 - 3" # Test mixed order and fraction
poly_str14_v5 = "0" # Test zero polynomial
poly_str15_v5 = "" # Test empty string

test_strings_v5 = [
    poly_str1_v5, poly_str2_v5, poly_str3_v5, poly_str4_v5, poly_str5_v5,
    poly_str6_v5, poly_str7_v5, poly_str8_v5, poly_str9_v5, poly_str10_v5,
    poly_str11_v5, poly_str12_v5, poly_str13_v5, poly_str14_v5, poly_str15_v5
]

for test_str in test_strings_v5:
    try:
        poly = parse_polynomial(test_str) # Use the updated function name
        print(f"Parsing '{test_str}' -> {poly}")
    except ValueError as e:
        print(f"Parsing '{test_str}' failed: {e}")

# 测试运算与解析器的结合
print("\n--- 测试运算与解析器的结合 ---")
try:
    p_a = parse_polynomial("x^2 + 2*x + 1")
    p_b = parse_polynomial("x + 1")
    p_sum = p_a + p_b
    p_diff = p_a - p_b
    p_prod = p_a * p_b
    p_div = p_a / p_b # (x^2 + 2x + 1) / (x + 1) = x + 1

    print(f"({p_a}) + ({p_b}) = {p_sum}")
    print(f"({p_a}) - ({p_b}) = {p_diff}")
    print(f"({p_a}) * ({p_b}) = {p_prod}")
    print(f"({p_a}) / ({p_b}) = {p_div}")

    # 测试分数和负系数
    p_c = parse_polynomial("1/2*x^2 - 3/4")
    p_d = parse_polynomial("2*x + 1/2")
    p_sum_frac = p_c + p_d
    p_prod_frac = p_c * p_d

    print(f"({p_c}) + ({p_d}) = {p_sum_frac}")
    print(f"({p_c}) * ({p_d}) = {p_prod_frac}")

except ValueError as e:
    print(f"运算测试失败: {e}")

print("\n--- 测试多项式除法并显示商和余数 ---")

# 示例 1: 可以整除
poly_dividend1 = parse_polynomial("x^3 - 8") # x^3 - 8
poly_divisor1 = parse_polynomial("x - 2")    # x - 2

try:
    quotient1, remainder1 = poly_dividend1.divmod_polynomial(poly_divisor1)
    print(f"({poly_dividend1}) 除以 ({poly_divisor1})")
    print(f"商: {quotient1}")
    print(f"余数: {remainder1}")
    # 验证: P(x) = Q(x) * 商(x) + 余数(x)
    # print(f"验证: ({poly_divisor1}) * ({quotient1}) + ({remainder1}) = {poly_divisor1 * quotient1 + remainder1}")

except ValueError as e:
    print(f"除法失败: {e}")


print("-" * 20)

# 示例 2: 有余数
poly_dividend2 = parse_polynomial("x^2 + 1") # x^2 + 1
poly_divisor2 = parse_polynomial("x + 1") # x + 1

try:
    quotient2, remainder2 = poly_dividend2.divmod_polynomial(poly_divisor2)
    print(f"({poly_dividend2}) 除以 ({poly_divisor2})")
    print(f"商: {quotient2}")
    print(f"余数: {remainder2}")
     # 验证: P(x) = Q(x) * 商(x) + 余数(x)
    # print(f"验证: ({poly_divisor2}) * ({quotient2}) + ({remainder2}) = {poly_divisor2 * quotient2 + remainder2}")

except ValueError as e:
     print(f"除法失败: {e}")
