from v1 import *

poly1 = Polynomial({2: 3, 1: 1, 0: -5}) # 3x^2 + x - 5
poly2 = Polynomial({1: 1, 0: 5})      # x + 5
poly_sum = poly1 + poly2
poly_diff = poly1 - poly2
poly_prod = poly1 * poly2

print(f"Poly1: {poly1}")
print(f"Poly2: {poly2}")
print(f"Sum: {poly_sum}")
print(f"Diff: {poly_diff}")
print(f"Prod: {poly_prod}")

# 除法示例
poly_dividend = Polynomial({3: 1, 0: -8}) # x^3 - 8
poly_divisor = Polynomial({1: 1, 0: -2})  # x - 2
poly_quotient = poly_dividend / poly_divisor
print(f"Division ({poly_dividend} / {poly_divisor}): {poly_quotient}") # 应该输出 x^2 + 2x + 4

poly_dividend2 = Polynomial({2: 1, 0: 1}) # x^2 + 1
poly_divisor2 = Polynomial({1: 1, 0: 1}) # x + 1
# 这个除法有余数
poly_quotient2 = poly_dividend2 / poly_divisor2
print(f"Division ({poly_dividend2} / {poly_divisor2}): {poly_quotient2}") # 应该输出 x - 1 (余数 2 被忽略)
