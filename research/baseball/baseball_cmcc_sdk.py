#!/usr/bin/env python3

import json
import argparse
import math
import re
import textwrap
import os

"""
A CLI tool that reads a "rulebook" JSON file describing quantum-walk entities
and attempts to generate Python class stubs with valid expressions for
calculated fields, referencing typical quantum-walk building blocks.

NEW FEATURE:
- Instead of embedding SHIFT, APPLY_BARRIER, EVOLVE, etc. directly, we assume
  they live in a separate Python module (e.g., 'quantum_walk_blocks.py').
- This script just generates code that imports those symbols.

We also:
1) Support both 4-arg and 10-arg EVOLVE calls.
2) Handle SLICE(...) expressions to produce array slicing code.
3) Optionally parse 'ABS(...)^2' if still in the JSON.

Usage:
  python json-toemm-to-python-helper.py -i my-experiment.json -o my-exp-helper.py
"""

# ------------------------------------------------------------------------
# 0) We're no longer storing big building-block code in BUILDING_BLOCKS.
#    Instead, we keep references here only for the parser to detect usage.
# ------------------------------------------------------------------------
BUILDING_BLOCKS = {
    # We'll store only empty or minimal placeholders, so the parse_formula
    # logic sees them as recognized calls. We won't actually inject the code.
    "SHIFT": "",
    "APPLY_BARRIER": "",
    "COLLAPSE_BARRIER": "",
    "GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION": "",
    "EVOLVE": "",
    # If you have others (MATMUL, etc.), add them similarly
}

# ------------------------------------------------------------------------
# 1) Mappings for recognized function calls used in quantum-walk contexts
# ------------------------------------------------------------------------
FUNCTION_MAP = {
    # Basic math
    "SQRT": (1, 1, "math.sqrt({0})"),
    "LEN": (1, 1, "len({0})"),
    "ADD": (2, 2, "({0} + {1})"),
    "SUBTRACT": (2, 2, "({0} - {1})"),
    "MULTIPLY": (2, 2, "np.matmul({0}, {1})"),   # for matrix multiply
    "DIVIDE": (2, 2, "({0} / {1})"),
    "POWER": (2, 2, "({0} ** {1})"),
    "FLOOR": (1, 1, "math.floor({0})"),
    "ABS": (1, 1, "np.abs({0})"),
    "SUM_OVER": (2, 2, "sum(getattr(item, '{1}') for item in self.{0})"),
    "MAX_OVER": (2, 2, "max(getattr(item, '{1}') for item in self.{0})"),
    "EQUAL": (2, 2, "np.allclose({0}, {1})"),
    "IF": (3, 3, "({1} if {0} else {2})"),

    # SHIFT(psi_in, offsets) => SHIFT({0}, {1})
    "SHIFT": (2, 2, "SHIFT({0}, {1})"),
    "APPLY_BARRIER": (6, 6, "APPLY_BARRIER({0}, {1}, {2}, {3}, {4}, {5})"),
    "COLLAPSE_BARRIER": (6, 6, "COLLAPSE_BARRIER({0}, {1}, {2}, {3}, {4}, {5})"),
    "GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION": (5, 5,
        "GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION({0}, {1}, {2}, {3}, {4})"
    ),
    "CONJUGATE_TRANSPOSE": (1, 1, "{0}.conj().T"),
    "IDENTITY": (1, 1, "np.eye({0}, dtype=np.complex128)"),
    # We handle EVOLVE calls ourselves
    "EVOLVE": (4, 10, ""),
    # Also handle SLICE ourselves
    "SLICE": (3, 3, ""),

    # "SUM" -> e.g. SUM(..., axis=-1)
    "SUM": (1, 2, "np.sum({0}{extra})"),
    # Possibly more specialized calls
}

AXIS_SPEC_REGEX = re.compile(r"^axis\\s*=\\s*(.*)$", re.IGNORECASE)
INDEX_SPEC_REGEX = re.compile(r"^index\\s*=\\s*(.*)$", re.IGNORECASE)
POWER2_REGEX = re.compile(r"^(.*)\\^2$")
FUNC_CALL_REGEX = re.compile(r"^([A-Z_]+)\((.*)\)$", re.IGNORECASE)
STRING_LITERAL_RE = re.compile(r"^(['\"])(.*)\1$")  # Captures 'something' or "something"


def parse_token(token: str) -> str:
    token = token.strip()

    # If it's a string literal like 'Triangle'
    match = STRING_LITERAL_RE.match(token)
    if match:
        return token

    # If it's numeric
    if re.match(r"^[0-9.+-]+$", token):
        return token

    # Otherwise assume variable => 'self.<variable>'
    return f"self.{token}"


def parse_formula(expr, used_blocks_set):
    """
    Recursive parser for the formulas. Minimally updated:
      - Allows EVOLVE with 4 or 10 arguments
      - Slices via SLICE(psi_in, axis=0, index=detector_row)
      - aggregator calls skip self. for the first 2 args
    """
    expr = expr.strip()

    # 1) exponent ^2 => **2
    pow_match = POWER2_REGEX.match(expr)
    if pow_match:
        sub_expr = pow_match.group(1).strip()
        parsed_sub = parse_formula(sub_expr, used_blocks_set)
        return f"({parsed_sub}**2)"

    # 2) function call or single token
    match = FUNC_CALL_REGEX.match(expr)
    if not match:
        # single token
        return parse_token(expr)

    func_name = match.group(1).upper()
    args_str = match.group(2).strip()
    used_blocks_set.add(func_name)

    # parse args
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
            arg_str = "".join(current).strip()
            if arg_str:
                args.append(arg_str)
            current = []
        else:
            current.append(char)
    if current:
        arg_str = "".join(current).strip()
        if arg_str:
            args.append(arg_str)

    aggregator_funcs = {"SUM_OVER", "MAX_OVER"}
    parsed_args = []
    if func_name in aggregator_funcs:
        # skip "self." prefix for the first 2 aggregator args
        for arg in args:
            submatch = FUNC_CALL_REGEX.match(arg) or POWER2_REGEX.match(arg)
            if submatch:
                parsed_args.append(parse_formula(arg, used_blocks_set))
            else:
                # no sub-func => raw or literal
                lit = STRING_LITERAL_RE.match(arg)
                if lit:
                    parsed_args.append(arg)
                elif re.match(r"^[0-9.+-]+$", arg):
                    parsed_args.append(arg)
                else:
                    parsed_args.append(arg)
    else:
        # normal
        parsed_args = [parse_formula(a, used_blocks_set) for a in args]

    # special-case EVOLVE
    if func_name == "EVOLVE":
        # 4-arg or 10-arg
        narg = len(parsed_args)
        if narg == 4:
            return f"EVOLVE({parsed_args[0]}, {parsed_args[1]}, {parsed_args[2]}, {parsed_args[3]})"
        elif narg == 10:
            return (
                f"EVOLVE({parsed_args[0]}, {parsed_args[1]}, {parsed_args[2]}, {parsed_args[3]}, "
                f"{parsed_args[4]}, {parsed_args[5]}, {parsed_args[6]}, {parsed_args[7]}, "
                f"{parsed_args[8]}, {parsed_args[9]})"
            )
        else:
            return f"# ERROR: EVOLVE expects 4 or 10 args, got {narg}"

    # special-case SLICE
    if func_name == "SLICE":
        if len(parsed_args) != 3:
            return f"# ERROR: SLICE expects 3 args, got {len(parsed_args)}"
        arr_name = parsed_args[0]
        axis_arg = args[1].strip()
        index_arg = args[2].strip()

        axis_match = AXIS_SPEC_REGEX.match(axis_arg)
        if not axis_match:
            return "# ERROR: SLICE second arg must be axis=N"
        axis_val = axis_match.group(1).strip()

        idx_match = INDEX_SPEC_REGEX.match(index_arg)
        if not idx_match:
            return "# ERROR: SLICE third arg must be index=?"
        idx_val = idx_match.group(1).strip()

        # convert axis_val => int
        try:
            axis_i = int(axis_val)
        except ValueError:
            return "# ERROR: SLICE axis must be int"

        # convert idx_val => numeric or self.<var>
        try:
            float(idx_val)
            row_str = idx_val
        except ValueError:
            row_str = f"self.{idx_val}"

        if axis_i == 0:
            return f"{arr_name}[{row_str}, :, :]"
        elif axis_i == 1:
            return f"{arr_name}[:, {row_str}, :]"
        elif axis_i == 2:
            return f"{arr_name}[:, :, {row_str}]"
        else:
            return "# ERROR: SLICE axis must be 0,1,2"

    # fallback
    info = FUNCTION_MAP.get(func_name)
    if not info:
        return f"# ERROR: Unknown function {func_name}"
    min_args, max_args, template = info
    if not (min_args <= len(parsed_args) <= max_args):
        return f"# ERROR: {func_name} expects {min_args}..{max_args} args, got {len(parsed_args)}"

    try:
        return template.format(*parsed_args, extra="")
    except KeyError as e:
        return f"# ERROR: Missing key {str(e)} in {func_name} template"
    except IndexError:
        return f"# ERROR: mismatch placeholders in {func_name}"


def transform_formula(formula_str, used_blocks_set):
    if not formula_str:
        return "None"
    return parse_formula(formula_str, used_blocks_set)


def generate_class_code(entity, used_blocks_set):
    class_name = entity["name"]
    fields = entity.get("fields", [])

    code_lines = []
    code_lines.append(f"class {class_name}:")
    code_lines.append("    def __init__(self, **kwargs):")

    has_non_calc = False
    for f in fields:
        if f.get("type") != "calculated":
            code_lines.append(f"        self.{f['name']} = kwargs.get('{f['name']}')")
            has_non_calc = True

    if not has_non_calc:
        code_lines.append("        pass")

    for f in fields:
        if f.get("type") == "calculated":
            formula = f.get("formula","")
            pyexpr = transform_formula(formula, used_blocks_set)
            prop_name = f["name"]

            code_lines.append("")
            code_lines.append("    @property")
            code_lines.append(f"    def {prop_name}(self):")
            code_lines.append(f"        \"\"\"")
            code_lines.append(f"        Original formula: {formula}")
            code_lines.append("        \"\"\"")
            if pyexpr.startswith("# ERROR"):
                code_lines.append(f"        # Parser error for formula: {formula}")
                code_lines.append("        return None")
            else:
                code_lines.append(f"        return {pyexpr}")

    return "\n".join(code_lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate Python classes from a JSON experiment rulebook. "
                    "No building-block injection, but references an external module."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to input JSON file.")
    parser.add_argument("-o", "--output", required=True, help="Path to output .py file.")
    parser.add_argument("--include-sample-main", action="store_true",
        help="If set, also inject a sample_main() function demonstration.")
    args = parser.parse_args()

    with open(args.input,"r",encoding="utf-8") as f:
        entities = json.load(f)["meta-model"]["schema"]["entities"]

    used_blocks = set()
    class_codes = []
    for e in entities:
        code = generate_class_code(e, used_blocks)
        class_codes.append(code)

    # We'll not embed big code blocks, just import from an external module:
    # e.g. "from quantum_walk_blocks import SHIFT, APPLY_BARRIER, COLLAPSE_BARRIER, EVOLVE, GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION"
    # We'll build a sorted list from used_blocks that appear in BUILDING_BLOCKS
    external_imports = []
    for block_name in sorted(used_blocks):
        if block_name in BUILDING_BLOCKS:
            external_imports.append(block_name)
    # e.g. ["APPLY_BARRIER","COLLAPSE_BARRIER", ...]

    output_lines = []
    output_lines.append('"""')
    output_lines.append("Auto-generated Python code from your quantum-walk rulebook.")
    output_lines.append("References SHIFT, APPLY_BARRIER, EVOLVE, etc. from an external python file.")
    output_lines.append('"""')
    output_lines.append("import math")
    output_lines.append("import numpy as np")
    output_lines.append("")
    if external_imports:
        # e.g. from quantum_walk_blocks import SHIFT, APPLY_BARRIER
        # We can let you define the module name if needed:
        module_name = "quantum_walk_blocks"  # or "physics_blocks", etc.
        import_list = ", ".join(sorted(external_imports))
        output_lines.append(f"from {module_name} import {import_list}")
        output_lines.append("")

    output_lines.append("# ----- Generated classes below -----")
    output_lines.append("")
    for cc in class_codes:
        output_lines.append(cc)
        output_lines.append("")

    if args.include_sample_main:
        sample_main_str = textwrap.dedent("""\
        def sample_main():
            \"\"\"
            Minimal demonstration of how to use the auto-generated classes and building blocks.
            You must have quantum_walk_blocks.py with SHIFT, EVOLVE, etc.
            \"\"\"
            print("sample_main() not fully implemented. Please fill in your usage.")
        
        if __name__ == "__main__":
            sample_main()
        """)
        output_lines.append(sample_main_str)
        output_lines.append("")

    final_code = "\n".join(output_lines)
    with open(args.output,"w",encoding="utf-8") as out_f:
        out_f.write(final_code)

    print(f"Generated Python code written to {args.output}")
    if external_imports:
        print("Detected usage of building blocks:", ", ".join(sorted(external_imports)))


if __name__=="__main__":
    main()

