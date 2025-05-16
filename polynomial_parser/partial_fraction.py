# polynomial_parser/partial_fraction.py
# print("Debug: partial_fraction.py is being loaded.") # Commented out debug print

from .fractional_polynomial import FractionalPolynomial
from .polynomial import Polynomial
from fractions import Fraction
import sympy # Import sympy

# print(sympy.__version__) # Commented out debug print

def to_sympy_poly(poly: Polynomial, symbol_name='x'):
    """Converts a custom Polynomial object to a sympy Polynomial."""
    x = sympy.symbols(symbol_name)
    # Construct dictionary using standard Python int for exponents and Fraction for coefficients
    # Let SymPy handle the conversion to its internal types (Integer, Rational).
    sympy_terms = {int(exp): coeff for exp, coeff in poly.terms.items()}
    # print(f"Debug: to_sympy_poly - Converting custom poly {poly.terms} to sympy terms: {sympy_terms}") # Commented out debug print
    return sympy.Poly(sympy_terms, x) # Let SymPy handle conversion from int/Fraction

# Helper function to get a sorting key for each term
# Returns a tuple (priority, degree)
# Higher priority comes first. Within the same priority, higher degree comes first (due to reverse=True)
def get_sort_key(term, symbol):
    try:
        if isinstance(term, Polynomial):
            # Custom Polynomial: Priority 3, actual degree
            return (3, term.degree())

        elif isinstance(term, FractionalPolynomial):
            # Custom FractionalPolynomial: Priority 2.
            # Sort by the degree difference num_deg - den_deg using sympy.
            try:
                # to_sympy_poly is in this file, no need for circular import
                sympy_num = to_sympy_poly(term.numerator, str(symbol))
                sympy_den = to_sympy_poly(term.denominator, str(symbol))
                # SymPy degree of a rational function N/D is deg(N) - deg(D)
                # Be careful with degrees of zero polynomials (-inf)
                num_deg = sympy.degree(sympy_num, symbol) if not sympy_num.is_zero else -float('inf')
                den_deg = sympy.degree(sympy_den, symbol) if not sympy_den.is_zero else -float('inf')
                return (2, num_deg - den_deg) # Priority 2, degree difference
            except Exception as e:
                print(f"警告: 计算 FractionalPolynomial 排序次数时出错: {term}, error: {e}")
                return (2, -999999) # Priority 2, very low degree on error

        elif isinstance(term, sympy.Expr):
            # SymPy Expression: Priority based on type (polynomial, rational, constant, etc.)
            try:
                if term.is_polynomial(symbol):
                    # SymPy polynomial expressions: Priority 3, actual degree
                    return (3, sympy.degree(term, symbol))
                elif term.is_rational_function(symbol):
                    # SymPy rational function expressions: Priority 2.
                    # Get numerator and denominator to calculate degree difference.
                    numerator_expr, denominator_expr = term.as_numer_denom()
                    try:
                        num_deg = sympy.degree(numerator_expr, symbol) if not numerator_expr.is_zero else -float('inf')
                        den_deg = sympy.degree(denominator_expr, symbol) if not denominator_expr.is_zero else -float('inf')
                        return (2, num_deg - den_deg) # Priority 2, degree difference
                    except Exception as e:
                        # This catches errors during degree calculation for num/den of rational function
                        print(f"警告: 计算 SymPy RationalFunction 排序次数时出错 (as_numer_denom degrees): {term}, error: {e}")
                        return (2, -1000000) # Priority 2, very low degree on error
                elif term.is_constant():
                    # SymPy constants: Priority 2, degree 0 (place with polynomials but after positive degrees)
                    return (2, 0)
                else:
                    # Other SymPy expressions: Priority 1
                    return (1, 0)

            except Exception as e:
                # Catch errors during SymPy expression analysis/classification
                print(f"警告: 分析 SymPy 表达式以获取排序键时出错: {term}, error: {e}")
                return (0, 0) # Lower priority on error


        else:
            # Unknown types: Lowest priority -1, degree 0
            print(f"警告: 遇到未知类型的项以排序: {term} (类型: {type(term)})")
            return (-1, 0)

    except Exception as e:
        # Catch any unexpected errors during outer try block
        print(f"警告: 生成排序键时发生未知错误: {term}, error: {e}")
        return (-2, 0) # Very low priority

def from_sympy_expr(expr, symbol_name='x'):
    """Converts a sympy expression back to custom objects."""
    x = sympy.symbols(symbol_name)

    # print(f"Debug: from_sympy_expr converting SymPy expression type: {type(expr)}, value: {expr}") # Commented out debug print

    # If it's an Add, convert each term and return a list
    if isinstance(expr, sympy.Add):
        # print("Debug: from_sympy_expr handling SymPy Add") # Commented out debug print
        converted_terms = []
        for i, arg in enumerate(expr.args):
             # print(f"Debug: from_sympy_expr - Add argument {i} type: {type(arg)}, value: {arg}") # Commented out debug print
             converted_term = from_sympy_expr(arg, symbol_name)
             if isinstance(converted_terms, list) and isinstance(converted_term, list): # Handle cases where recursive call returns a list
                  converted_terms.extend(converted_term)
             elif converted_term is not None:
                  converted_terms.append(converted_term)
             # print(f"Debug: from_sympy_expr - Converted Add argument {i}: {converted_term}") # Commented out debug print
        return converted_terms


    # If it's a Mul, it could be a constant, a polynomial, or a fractional term
    elif isinstance(expr, sympy.Mul):
        # print("Debug: from_sympy_expr handling SymPy Mul") # Commented out debug print
        # Try to interpret the Mul as a fractional term: constant * (poly)**-power
        constant_factor_sym = sympy.Integer(1)
        numerator_part_sym = sympy.Integer(1) # For terms not in the denominator form
        denominator_base_sym = sympy.Integer(1)
        denominator_power = 0
        is_fractional_term = False

        # Corrected: Call as_ordered_factors as a method of the expression
        factors = expr.as_ordered_factors()
        # print(f"Debug: from_sympy_expr - Mul factors: {factors}") # Commented out debug print

        # Find terms with negative powers, which are likely parts of the denominator
        negative_power_terms = [(arg.args[0], abs(arg.args[1])) for arg in factors if isinstance(arg, sympy.Pow) and isinstance(arg.args[1], (sympy.Integer, int)) and arg.args[1] < 0]

        if len(negative_power_terms) >= 1: # Handle one or more terms with negative powers
            # Combine all negative power terms into a single denominator base and power
            # This assumes the denominator will be a product of powers of polynomials
            combined_denominator_expr = sympy.Integer(1)
            for base, power in negative_power_terms:
                 combined_denominator_expr *= base**power # Reconstruct the denominator expression

            denominator_base_sym = combined_denominator_expr
            denominator_power = 1 # Treat the combined expression as the base raised to power 1
            is_fractional_term = True

            # The remaining factors form the numerator part and constant factor
            other_factors = [arg for arg in factors if not (isinstance(arg, sympy.Pow) and isinstance(arg.args[1], (sympy.Integer, int)) and arg.args[1] < 0)]
            combined_other_factors = sympy.Mul(*other_factors) if other_factors else sympy.Integer(1)

            # Separate constant factor from the numerator expression
            if isinstance(combined_other_factors, (sympy.Rational, sympy.Integer)):
                 constant_factor_sym = combined_other_factors
                 numerator_part_sym = sympy.Integer(1) # Numerator is just 1 after extracting constant
            else: # Assume the rest is the numerator expression
                 numerator_part_sym = combined_other_factors
                 constant_factor_sym = sympy.Integer(1) # Assume constant factor is 1 if not explicit


        if is_fractional_term:
            # print(f"Debug: from_sympy_expr - Interpreting as fractional term: constant={constant_factor_sym}, numerator_part={numerator_part_sym}, denominator_base={denominator_base_sym}") # Commented out debug print
            num_poly = from_sympy_expr_to_polynomial(numerator_part_sym, symbol_name)
            den_poly = from_sympy_expr_to_polynomial(denominator_base_sym, symbol_name) # Denominator is the combined base

            if num_poly is not None and den_poly is not None:
                 # Apply the constant factor to the numerator
                 constant_poly = Polynomial({0: Fraction(str(constant_factor_sym))})
                 try:
                      num_poly = num_poly * constant_poly # Polynomial multiplication
                 except Exception as e:
                      print(f"Error during constant polynomial multiplication in Mul handling: {e}")
                      return expr # Return original SymPy expression on error


                 if den_poly.is_constant() and den_poly.terms.get(0) == Fraction(1):
                     # print("Debug: from_sympy_expr - Denominator simplified to 1, returning numerator as Polynomial") # Commented out debug print
                     return num_poly # It was a polynomial term (e.g., from 1/(x+1)^0)
                 else:
                     return FractionalPolynomial(num_poly, den_poly)
            else:
                # print(f"Warning: from_sympy_expr - Could not convert parts of fractional term {expr} to Polynomials during fractional interpretation.")
                return expr # Conversion failed

        else:
             # If it's a Mul but not a fractional term in the expected format, try converting as a polynomial
             # print(f"Debug: from_sympy_expr - Not interpreted as fractional term, trying as simple polynomial.") # Commented out debug print
             poly_conversion = from_sympy_mul_to_polynomial(expr, symbol_name)
             if poly_conversion is not None:
                  # print(f"Debug: from_sympy_expr - Successfully converted Mul to Polynomial: {poly_conversion}") # Commented out debug print
                  return poly_conversion
             else:
                  # print(f"Warning: from_sympy_expr - Could not interpret Mul expression {expr} as a fractional term or a simple polynomial.")
                  return expr

    # Handle simple Polynomials returned directly by apart
    elif isinstance(expr, sympy.Poly):
        # print("Debug: from_sympy_expr handling SymPy Poly") # Commented out debug print
        try:
            custom_terms = {int(exp): Fraction(str(coeff)) for exp, coeff in expr.as_dict().items()}
            return Polynomial(custom_terms)
        except Exception as e:
            print(f"Error converting SymPy Poly {expr} to custom Polynomial: {e}")
            return expr


    # Handle standalone Power expressions representing fractions like 1/(x+a)^n
    elif isinstance(expr, sympy.Pow):
        # print("Debug: from_sympy_expr handling SymPy Pow") # Commented out debug print
        base = expr.args[0]
        exponent = expr.args[1]

        if isinstance(exponent, (sympy.Integer, int)) and exponent < 0:
            # It's a negative power, likely representing a fractional term
            # print(f"Debug: from_sympy_expr - Pow has negative exponent, interpreting as fractional term.") # Commented out debug print
            numerator_sym = sympy.Integer(1) # Numerator is 1
            denominator_sym = base**abs(exponent) # Denominator is base to positive power

            num_poly = from_sympy_expr_to_polynomial(numerator_sym, symbol_name)
            den_poly = from_sympy_expr_to_polynomial(denominator_sym, symbol_name)

            if num_poly is not None and den_poly is not None:
                 if den_poly.is_constant() and den_poly.terms.get(0) == Fraction(1):
                     # print("Debug: from_sympy_expr - Pow denominator simplified to 1, returning numerator as Polynomial") # Commented out debug print
                     return num_poly # Should not happen for negative exponent Pow from apart
                 else:
                     return FractionalPolynomial(num_poly, den_poly)
            else:
                 # print(f"Warning: from_sympy_expr - Could not convert parts of Pow expression {expr} to Polynomials.")
                 return expr # Conversion failed

        else:
            # It's a positive or non-integer power, try converting as a polynomial (less likely from apart)
            # print(f"Debug: from_sympy_expr - Pow has non-negative/non-integer exponent, trying as simple polynomial.") # Commented out debug print
            poly_conversion = from_sympy_expr_to_polynomial(expr, symbol_name)
            if poly_conversion is not None:
                # print(f"Debug: from_sympy_expr - Successfully converted Pow to Polynomial: {poly_conversion}") # Commented out debug print
                return poly_conversion
            else:
                # print(f"Warning: from_sympy_expr - Could not interpret Pow expression {expr} as a fractional term or a simple polynomial.")
                return expr


    # Handle constants (Rational, Integer) and Symbol
    elif isinstance(expr, (sympy.Rational, sympy.Integer)):
        # print("Debug: from_sympy_expr handling SymPy Rational/Integer") # Commented out debug print
        try:
            return Polynomial({0: Fraction(str(expr))})
        except Exception as e:
            print(f"Error converting SymPy Rational/Integer {expr} to custom Polynomial: {e}")
            return expr

    # Corrected handling for SymPy singleton objects One and Zero
    elif expr is sympy.S.One:
        # print("Debug: from_sympy_expr handling SymPy One (singleton)") # Commented out debug print
        try:
            return Polynomial({0: Fraction(1)})
        except Exception as e:
            print(f"Error converting SymPy One (singleton) to custom Polynomial: {e}")
            return expr

    elif expr is sympy.S.Zero:
        # print("Debug: from_sympy_expr handling SymPy Zero (singleton)") # Commented out debug print
        try:
             return Polynomial({})
        except Exception as e:
             print(f"Error converting SymPy Zero (singleton) to custom Polynomial: {e}")
             return expr

    elif isinstance(expr, sympy.Symbol) and str(expr) == symbol_name:
        # print("Debug: from_sympy_expr handling SymPy Symbol") # Commented out debug print
        try:
            return Polynomial({1: Fraction(1)})
        except Exception as e:
             print(f"Error converting SymPy Symbol to custom Polynomial: {e}")
             return expr

    else:
        # print(f"Warning: from_sympy_expr - Encountered unhandled SymPy expression type: {type(expr)}. Expression: {expr}")
        # As a last resort, try converting the whole unhandled expression to a Polynomial
        poly_conversion_attempt = from_sympy_expr_to_polynomial(expr, symbol_name)
        if poly_conversion_attempt is not None:
            # print(f"Debug: from_sympy_expr - Successfully converted unhandled type to Polynomial: {poly_conversion_attempt}") # Commented out debug print
            return poly_conversion_attempt
        else:
             # print(f"Debug: from_sympy_expr - Could not convert unhandled type {type(expr)} to Polynomial.") # Commented out debug print
             return expr # Cannot convert, return original SymPy expression


# Helper function to convert a SymPy expression to a custom Polynomial
# This function should be robust in handling expressions that are indeed polynomials
def from_sympy_expr_to_polynomial(expr, symbol_name='x'):
    """Attempts to convert a sympy expression to a custom Polynomial object."""
    x = sympy.symbols(symbol_name)

    # print(f"Debug: from_sympy_expr_to_polynomial converting type: {type(expr)}, value: {expr}") # Commented out debug print

    # Handle simple cases directly
    if isinstance(expr, sympy.Poly):
        # print("Debug: from_sympy_expr_to_polynomial handling SymPy Poly") # Commented out debug print
        try:
            custom_terms = {int(exp): Fraction(str(coeff)) for exp, coeff in expr.as_dict().items()}
            return Polynomial(custom_terms)
        except Exception as e:
            print(f"Error converting SymPy Poly {expr} to custom Polynomial in helper: {e}")
            return None
    elif isinstance(expr, (sympy.Rational, sympy.Integer)):
        # print("Debug: from_sympy_expr_to_polynomial handling SymPy Rational/Integer") # Commented out debug print
        try:
            return Polynomial({0: Fraction(str(expr))})
        except Exception as e:
            print(f"Error converting SymPy constant {expr} to custom Polynomial in helper: {e}")
            return expr

    # Corrected handling for SymPy singleton objects One and Zero
    elif expr is sympy.S.One:
        # print("Debug: from_sympy_expr_to_polynomial handling SymPy One (singleton)") # Commented out debug print
        try:
            return Polynomial({0: Fraction(1)})
        except Exception as e:
            print(f"Error converting SymPy One (singleton) to custom Polynomial: {e}")
            return None

    elif expr is sympy.S.Zero:
        # print("Debug: from_sympy_expr_to_polynomial handling SymPy Zero (singleton)") # Commented out debug print
        try:
             return Polynomial({})
        except Exception as e:
             print(f"Error converting SymPy Zero (singleton) to custom Polynomial: {e}")
             return None


    elif isinstance(expr, sympy.Symbol) and str(expr) == symbol_name:
        # print("Debug: from_sympy_expr_to_polynomial handling SymPy Symbol") # Commented out debug print
        try:
            return Polynomial({1: Fraction(1)})
        except Exception as e:
             print(f"Error converting SymPy Symbol to custom Polynomial in helper: {e}")
             return None

    # Use sympy's functionality to convert to a polynomial if possible
    try:
        # print(f"Debug: from_sympy_expr_to_polynomial attempting sympy.Poly({expr}, {x}) conversion in helper") # Commented out debug print
        sympy_poly = sympy.Poly(expr, x)
        # print(f"Debug: from_sympy_expr_to_polynomial sympy.Poly conversion result: {sympy_poly}, generators: {sympy_poly.gens}") # Commented out debug print
        # Ensure the polynomial is indeed univariate in the target symbol and has integer exponents
        if all(isinstance(gen, sympy.Symbol) and str(gen) == symbol_name for gen in sympy_poly.gens) and \
           all(isinstance(exp, (int, sympy.Integer)) for term in sympy_poly.as_terms() for exp in term[1]):
              # print("Debug: from_sympy_expr_to_polynomial SymPy Poly is a simple univariate polynomial with integer exponents.") # Commented out debug print
              custom_terms = {int(exp): Fraction(str(coeff)) for exp, coeff in sympy_poly.as_dict().items()}
              return Polynomial(custom_terms)
        else:
             # print(f"Debug: from_sympy_expr_to_polynomial SymPy Poly is not a simple univariate polynomial as expected: {sympy_poly}") # Commented out debug print
             return None

    except Exception as e:
        # If sympy.Poly() fails, it's likely not a simple polynomial
        # print(f"Debug: from_sympy_expr_to_polynomial sympy.Poly conversion failed for {expr} in helper: {e}") # Commented out debug print
        return None # Indicate failure


# Helper function to convert a sympy Mul expression to a custom Polynomial if it represents one
def from_sympy_mul_to_polynomial(expr, symbol_name='x'):
     """Attempts to convert a sympy Mul expression to a custom Polynomial object if it represents a simple polynomial."""
     if isinstance(expr, sympy.Mul):
          # print(f"Debug: from_sympy_mul_to_polynomial converting Mul type: {type(expr)}, value: {expr}") # Commented out debug print
          # Corrected: Call expand as a method of the expression
          expanded_expr = expr.expand()
          # print(f"Debug: from_sympy_mul_to_polynomial Expanded Mul to: {expanded_expr}") # Commented out debug print
          return from_sympy_expr_to_polynomial(expanded_expr, symbol_name)
     else:
          return None # Not a Mul expression


def partial_fraction_decompose(frac_poly: FractionalPolynomial, symbol_name='x') -> list[FractionalPolynomial | Polynomial]:
    """
    对分式多项式进行分式裂项。

    Args:
        frac_poly: 需要进行裂项的分式多项式 (FractionalPolynomial 对象)。
        symbol_name: 多项式变量的名称 (默认为 'x')。

    Returns:
        一个列表，包含裂项后的项。这些项可能是 Polynomial 或 FractionalPolynomial 对象。
    """
    numerator_sym = to_sympy_poly(frac_poly.numerator, symbol_name)
    denominator_sym = to_sympy_poly(frac_poly.denominator, symbol_name)
    x = sympy.symbols(symbol_name)

    # Create a SymPy expression for the fractional polynomial
    sympy_frac_expr = numerator_sym / denominator_sym

    # Perform partial fraction decomposition using SymPy
    # SymPy's apart handles both polynomial part and true fraction decomposition
    sympy_decomposed = sympy.apart(sympy_frac_expr, x)

    # Convert the SymPy result back to a list of custom objects
    # apart can return a single expression or an Add object
    if isinstance(sympy_decomposed, sympy.Add):
         # print("Debug: partial_fraction_decompose - SymPy result is an Add object, calling from_sympy_expr") # Commented out debug print
         result_terms = from_sympy_expr(sympy_decomposed, symbol_name)
    else:
         # If not an Add, it's a single term (polynomial part or a single fraction)
         # print("Debug: partial_fraction_decompose - SymPy result is a single expression, wrapping in a list and calling from_sympy_expr") # Commented out debug print
         result_terms = [from_sympy_expr(sympy_decomposed, symbol_name)]

    # Ensure the result is a list (from_sympy_expr might return a single object for non-Add inputs)
    if not isinstance(result_terms, list):
        # print(f"Debug: partial_fraction_decompose - Result from from_sympy_expr was not a list, wrapping: {result_terms}") # Commented out debug print
        result_terms = [result_terms]

    # print(f"Debug: partial_fraction_decompose - Final result_terms: {result_terms}") # Commented out debug print

    return result_terms
