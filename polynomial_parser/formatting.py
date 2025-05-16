# polynomial_parser/formatting.py

from .polynomial import Polynomial
from .fractional_polynomial import FractionalPolynomial
import sympy

# Import get_sort_key from partial_fraction for sorting
from .partial_fraction import get_sort_key

# Function to sort and print decomposed terms
def print_decomposed_terms(terms_list, symbol):
    # Sort the terms using the custom key (descending overall)
    sorted_terms = sorted(terms_list, key=lambda term: get_sort_key(term, symbol), reverse=True)

    # Print each term, adding '+' before subsequent terms if they are positive
    for i, term in enumerate(sorted_terms):
       # print(f"Debug: Processing term {i}, type: {type(term)}, value: {term}") # Print type and value of each term

        # Get the string representation based on type
        if isinstance(term, (Polynomial, FractionalPolynomial)):
            # Use the custom object's __str__ method which should handle ^ and implicit mul
            term_str = str(term)
        elif isinstance(term, sympy.Expr):
            # Use SymPy's default string representation, then replace ** with ^
            try:
                # Use SymPy's default string representation
                term_str = str(term)
                # Manually replace SymPy's default ** with ^
                term_str = term_str.replace('**', '^')
            except Exception as e:
                # Fallback if str fails
                print(f"警告: 格式化 SymPy 项时出错 ({term}), error: {e}")
                term_str = str(term) # Use default SymPy string if str fails
        else:
            # For any other unexpected types
            print(f"警告: 遇到未知类型的项 ({type(term)}): {term}")
            term_str = str(term)

        # Add separator before terms after the first one
        if i > 0:
            # If the term string starts with '-', add a space before the '-'
            if term_str.strip().startswith('-'):
                print(" ", end="")
            else:
                # Otherwise, add " + "
                print(" + ", end="")

        # Print the term string, adding a space after the '-' if it starts with one
        if term_str.strip().startswith('-'):
            print("- ", end="")
            print(term_str.strip()[1:], end="") # Print the rest of the string after the '-'
        else:
         # Print the term's string representation
            print(term_str, end="")

    # Print a final newline after all terms
    print()
    