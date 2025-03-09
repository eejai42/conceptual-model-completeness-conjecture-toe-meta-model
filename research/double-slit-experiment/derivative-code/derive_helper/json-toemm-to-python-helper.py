#!/usr/bin/env python3

import json
import argparse
import math
import re
import textwrap

"""
A CLI tool that reads a "rulebook" JSON file describing quantum-walk entities
and attempts to generate Python class stubs with valid expressions for
calculated fields, referencing typical quantum-walk building blocks.

Usage:
  python json_toemm_to_python_helper.py -i my-experiment.json -o my-exp-helper.py
"""

# ------------------------------------------------------------------------
# 1) Mappings for recognized function calls used in quantum-walk contexts
# ------------------------------------------------------------------------
# A dictionary of known function calls -> Python code templates
# The key is the uppercase function name, the value is a tuple:
#   (minimum_args, maximum_args, python_template_string)
#
# The python_template_string can use {0}, {1}, etc. for positional arguments
# from the parsed sub-expressions.
#
# If max_args == None, it means unlimited or we won't enforce strict max.
#
# Example: SHIFT(a,b) => SHIFT({0}, {1}) -> "SHIFT(self.a, self.b)" if it were that literal
#
FUNCTION_MAP = {
    # Basic math
    "ADD":      (2, 2, "({0} + {1})"),
    "SUBTRACT": (2, 2, "({0} - {1})"),
    "MULTIPLY": (2, 2, "np.matmul({0}, {1})"),   # for matrix multiply (if appropriate)
    "DIVIDE":   (2, 2, "({0} / {1})"),
    "FLOOR":    (1, 1, "math.floor({0})"),
    "ABS":      (1, 1, "np.abs({0})"),
    # For checking unitarity, we might do EQUAL => np.allclose, but let's keep it simple:
    "EQUAL":    (2, 2, "np.allclose({0}, {1})"),

    # More specialized quantum/physics calls:
    "IDENTITY": (1, 1, "np.eye({0}, dtype=np.complex128)"),  # IDENTITY(8) => np.eye(8)
    "TRANSPOSE": (1, 1, "{0}.T"),
    "CONJUGATE_TRANSPOSE": (1, 1, "{0}.conj().T"),

    "GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION": (5, 5,
        "GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION({0}, {1}, {2}, {3}, {4})"
    ),

    # SHIFT(psi_in, offsets)
    "SHIFT": (2, 2, "SHIFT({0}, {1})"),
    # MATMUL(psi_in, coin_matrix) => "np.matmul({0}, {1})"
    "MATMUL": (2, 2, "np.matmul({0}, {1})"),

    # APPLY_BARRIER(...) or COLLAPSE_BARRIER(...) if needed
    "APPLY_BARRIER": (6, 6, "APPLY_BARRIER({0}, {1}, {2}, {3}, {4}, {5})"),
    "COLLAPSE_BARRIER": (6, 6, "COLLAPSE_BARRIER({0}, {1}, {2}, {3}, {4}, {5})"),

    # SUM( X, axis=-1 ) => "np.sum(X, axis=-1)" or similar
    # We'll handle the possibility of an optional named arg: axis=...
    "SUM": (1, 2, "np.sum({0}{extra})"),

    # We'll handle "POWER(x,2)" if needed, or we interpret x^2 as x**2 in a separate step
}

# Regex to see if there's an axis specification like: SUM(foo, axis=-1)
AXIS_SPEC_REGEX = re.compile(r"^axis\s*=\s*(.*)$", re.IGNORECASE)

# We'll also detect if we have something like "ABS(row_amp)^2" by searching for ^2
# This is ad-hoc; a more robust approach is to parse the entire expression properly.
POWER2_REGEX = re.compile(r"^(.*)\^2$")

# Detect "FUNCTION(...)" 
FUNC_CALL_REGEX = re.compile(r"^([A-Z_]+)\((.*)\)$", re.IGNORECASE)


def parse_formula(expr):
    """
    Recursive parser to convert an expression like
        'DIVIDE(Lx,nx)' => '(self.Lx / self.nx)'
    or
        'MATMUL(psi_in,TRANSPOSE(coin_matrix))'
    into
        'np.matmul(self.psi_in, self.coin_matrix.T)'

    Also attempts to handle partial nesting, e.g.
        'FLOOR(DIVIDE(ADD(barrier_y_phys,DIVIDE(Ly,2)),dy))'
    We do a naive approach: split on top-level commas, parse function name, etc.
    """

    expr = expr.strip()

    # Special check for something like "xxx^2"
    # naive approach: if expr ends with "^2", parse "xxx" separately
    pow_match = POWER2_REGEX.match(expr)
    if pow_match:
        sub_expr = pow_match.group(1).strip()
        # parse that sub_expr, then return "({parsed_sub_expr}**2)"
        parsed_sub = parse_formula(sub_expr)
        return f"({parsed_sub}**2)"

    # If it doesn't look like "FUNC(...)", it might be a literal or identifier
    match = FUNC_CALL_REGEX.match(expr)
    if not match:
        # Could be a numeric literal or a variable name like "Lx"
        # If it's numeric, just return it
        if re.match(r"^[0-9.+-]+$", expr):
            return expr  # numeric literal
        # else treat it as a variable
        return f"self.{expr}"

    # We do have a function call
    func_name = match.group(1).upper()
    args_str = match.group(2).strip()

    # We'll parse the arguments, respecting parentheses depth
    args = []
    current = []
    depth = 0
    for char in args_str:
        if char == "(":
            depth += 1
            current.append(char)
        elif char == ")":
            depth -= 1
            current.append(char)
        elif char == "," and depth == 0:
            # top-level comma => split
            arg_str = "".join(current).strip()
            if arg_str:
                args.append(arg_str)
            current = []
        else:
            current.append(char)
    # leftover
    if current:
        arg_str = "".join(current).strip()
        if arg_str:
            args.append(arg_str)

    parsed_args = [parse_formula(a) for a in args]

    # Now see if we have a known function in FUNCTION_MAP
    info = FUNCTION_MAP.get(func_name)
    if not info:
        return f"# ERROR: Unknown function {func_name}"

    (min_args, max_args, template) = info
    if max_args is None:
        max_args = 99999  # allow "unlimited"

    if not (min_args <= len(parsed_args) <= max_args):
        return f"# ERROR: {func_name} expects {min_args}..{max_args} args, got {len(parsed_args)}"

    # Special-case: SUM(...) might have an axis argument
    # e.g. SUM( (some_expr), axis=-1 )
    if func_name == "SUM" and len(parsed_args) == 2:
        # second arg might be "axis=-1" or something
        axis_match = AXIS_SPEC_REGEX.match(args[1].strip())
        if axis_match:
            axis_val = axis_match.group(1).strip()
            # e.g. "-1"
            # then we do: np.sum(parsed_args[0], axis=-1)
            # We'll fill {0} with parsed_args[0], and add {extra} with ", axis=-1"
            return template.format(parsed_args[0], extra=f", axis={axis_val}")
        else:
            # if it's not an axis=... argument, we just fail
            return "# ERROR: SUM(...) second arg not recognized"

    # If it's a normal function with no named axis, fill in the template
    # e.g. for SHIFT => SHIFT({0}, {1})
    # for MATMUL => np.matmul({0}, {1}), etc.
    try:
        return template.format(*parsed_args, extra="")
    except IndexError:
        # if the user used fewer placeholders
        return f"# ERROR: mismatch placeholders in {func_name}"


def transform_formula(formula_str):
    """
    Attempt to parse the formula string into a Python expression.
    """
    if not formula_str:
        return "None"
    return parse_formula(formula_str)


def generate_class_code(entity):
    """
    Given one entity from the JSON, generate Python class code.

    For "calculated" fields, produce a read-only @property that returns the parsed formula.
    """
    class_name = entity["name"]
    fields = entity.get("fields", [])

    code_lines = []
    code_lines.append(f"class {class_name}:")
    code_lines.append("    def __init__(self, **kwargs):")

    has_non_calculated = False
    for f in fields:
        f_name = f["name"]
        f_type = f.get("type")
        if f_type != "calculated":
            has_non_calculated = True
            code_lines.append(f"        self.{f_name} = kwargs.get('{f_name}')")

    if not has_non_calculated:
        code_lines.append("        pass")

    # Now properties for calculated
    for f in fields:
        if f.get("type") == "calculated":
            prop_name = f["name"]
            formula = f.get("formula", "")
            python_expr = transform_formula(formula)

            code_lines.append("")
            code_lines.append("    @property")
            code_lines.append(f"    def {prop_name}(self):")
            code_lines.append(f"        \"\"\"")
            code_lines.append(f"        Original formula: {formula}")
            code_lines.append(f"        \"\"\"")
            if python_expr.startswith("# ERROR"):
                code_lines.append(f"        # Parser error for formula: {formula}")
                code_lines.append("        return None")
            else:
                code_lines.append(f"        return {python_expr}")

    return "\n".join(code_lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate Python classes from a JSON rulebook, with a parser "
                    "for typical quantum-walk formulas like SHIFT, MATMUL, etc."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to input JSON file.")
    parser.add_argument("-o", "--output", required=True, help="Path to output .py file.")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        entities = json.load(f)

    output_lines = []
    output_lines.append('"""')
    output_lines.append("Auto-generated Python classes from your JSON rulebook.")
    output_lines.append("Now including partial formula parsing for quantum-walk ops.")
    output_lines.append('"""')
    output_lines.append("import math")
    output_lines.append("import numpy as np")
    output_lines.append("")
    output_lines.append("# In your actual runtime, you'll need to define or import these:")
    output_lines.append("#   SHIFT, APPLY_BARRIER, COLLAPSE_BARRIER, GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION, etc.")
    output_lines.append("#   For example, from my_physics_lib import SHIFT, MATMUL, ...")
    output_lines.append("")
    output_lines.append("# ----- Generated classes below -----")
    output_lines.append("")

    for e in entities:
        class_code = generate_class_code(e)
        output_lines.append(class_code)
        output_lines.append("")

    final_code = "\n".join(output_lines)
    with open(args.output, "w", encoding="utf-8") as out_f:
        out_f.write(final_code)

    print(f"Generated Python code written to {args.output}")


if __name__ == "__main__":
    main()
