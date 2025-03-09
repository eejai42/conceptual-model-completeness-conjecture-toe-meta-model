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
- It also injects the reusable function definitions (SHIFT, APPLY_BARRIER, etc.)
  directly into the generated output, so we have a single self-contained .py file.

Usage:
  python json_toemm_to_python_helper.py -i my-experiment.json -o my-exp-helper.py
"""

# ------------------------------------------------------------------------
# 0) Some sample "building block" functions we might embed in the output
# ------------------------------------------------------------------------
# We'll keep them as strings. Our code will inject them at the top of the final file
# if we see references to SHIFT, APPLY_BARRIER, etc. in your JSON formulas.

BUILDING_BLOCKS = {
    "SHIFT": textwrap.dedent("""\
        def SHIFT(psi_in, offsets):
            \"\"\"
            SHIFT each spin component by the specified (dy,dx).
            psi_in: shape=(ny,nx,8) (or something similar)
            offsets: list of (ofy,ofx)
            \"\"\"
            import numpy as np
            ny, nx, spin_dim = psi_in.shape
            psi_out = np.zeros_like(psi_in)
            for d,(dy,dx) in enumerate(offsets):
                rolled = np.roll(psi_in[:,:,d], shift=dy, axis=0)
                rolled = np.roll(rolled, shift=dx, axis=1)
                psi_out[:,:,d] = rolled
            return psi_out
    """),
    "APPLY_BARRIER": textwrap.dedent("""\
        def APPLY_BARRIER(psi_in, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend):
            \"\"\"
            Zero out wavefunction in barrier_row except for the slit columns.
            \"\"\"
            import numpy as np
            psi_out = psi_in.copy()
            psi_out[barrier_row,:,:] = 0
            psi_out[barrier_row, slit1_xstart:slit1_xend, :] = psi_in[barrier_row, slit1_xstart:slit1_xend, :]
            psi_out[barrier_row, slit2_xstart:slit2_xend, :] = psi_in[barrier_row, slit2_xstart:slit2_xend, :]
            return psi_out
    """),
    "COLLAPSE_BARRIER": textwrap.dedent("""\
        def COLLAPSE_BARRIER(psi_in, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend):
            \"\"\"
            Example barrier measurement: amplitude outside the slits is lost.
            \"\"\"
            import numpy as np
            psi_out = np.zeros_like(psi_in)
            # sum intensities across directions
            row_intens = np.sum(np.abs(psi_in[barrier_row,:,:])**2, axis=-1)
            keep = np.zeros_like(row_intens)
            keep[slit1_xstart:slit1_xend] = row_intens[slit1_xstart:slit1_xend]
            keep[slit2_xstart:slit2_xend] = row_intens[slit2_xstart:slit2_xend]
            amps = np.sqrt(keep)
            # place them in direction=0 (say "up")
            d_up = 0
            psi_out[barrier_row, :, d_up] = amps
            return psi_out
    """),
    "GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION": textwrap.dedent("""\
        def GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION(src_y, sigma_y, ny, nx, spin_dim):
            \"\"\"
            Returns a np array (ny,nx,spin_dim) that is Gaussian in y, uniform in x & directions.
            \"\"\"
            import numpy as np
            arr = np.zeros((ny, nx, spin_dim), dtype=np.complex128)
            ycoords = np.arange(ny)
            gauss_y = np.exp(-0.5*((ycoords - src_y)/sigma_y)**2)
            # normalize in y
            norm_factor = np.sqrt(np.sum(np.abs(gauss_y)**2))
            gauss_y /= norm_factor

            # fill across x & directions
            for d in range(spin_dim):
                for x in range(nx):
                    arr[:, x, d] = gauss_y
            return arr
    """),
    # If you want others (e.g. MATMUL, etc.), define them here
}


# ------------------------------------------------------------------------
# 1) Mappings for recognized function calls used in quantum-walk contexts
# ------------------------------------------------------------------------
# A dictionary of known function calls -> Python code templates
# The key is the uppercase function name, the value is a tuple:
#   (minimum_args, maximum_args, python_template_string)
#
FUNCTION_MAP = {
    # Basic math
    "ADD":      (2, 2, "({0} + {1})"),
    "SUBTRACT": (2, 2, "({0} - {1})"),
    "MULTIPLY": (2, 2, "np.matmul({0}, {1})"),   # for matrix multiply (if appropriate)
    "DIVIDE":   (2, 2, "({0} / {1})"),
    "FLOOR":    (1, 1, "math.floor({0})"),
    "ABS":      (1, 1, "np.abs({0})"),
    # For checking unitarity, might do EQUAL => np.allclose
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

    # APPLY_BARRIER(...) or COLLAPSE_BARRIER(...)
    "APPLY_BARRIER": (6, 6, "APPLY_BARRIER({0}, {1}, {2}, {3}, {4}, {5})"),
    "COLLAPSE_BARRIER": (6, 6, "COLLAPSE_BARRIER({0}, {1}, {2}, {3}, {4}, {5})"),

    # SUM( X, axis=-1 ) => "np.sum(X, axis=-1)" or similar
    "SUM": (1, 2, "np.sum({0}{extra})"),
}

# Regex to see if there's an axis specification like: SUM(foo, axis=-1)
AXIS_SPEC_REGEX = re.compile(r"^axis\s*=\s*(.*)$", re.IGNORECASE)

# We'll also detect if we have something like "ABS(row_amp)^2" by searching for ^2
POWER2_REGEX = re.compile(r"^(.*)\^2$")
FUNC_CALL_REGEX = re.compile(r"^([A-Z_]+)\((.*)\)$", re.IGNORECASE)

def parse_formula(expr, used_blocks_set):
    """
    Recursive parser to convert an expression like
        'DIVIDE(Lx,nx)' => '(self.Lx / self.nx)'
    or
        'MATMUL(psi_in,TRANSPOSE(coin_matrix))'
    into
        'np.matmul(self.psi_in, self.coin_matrix.T)'

    We'll track which building-block calls are used (SHIFT, APPLY_BARRIER, etc.)
    by adding them to used_blocks_set.
    """

    expr = expr.strip()

    # Special check for something like "xxx^2"
    pow_match = POWER2_REGEX.match(expr)
    if pow_match:
        sub_expr = pow_match.group(1).strip()
        parsed_sub = parse_formula(sub_expr, used_blocks_set)
        return f"({parsed_sub}**2)"

    # If it doesn't look like "FUNC(...)", it might be a numeric or variable
    match = FUNC_CALL_REGEX.match(expr)
    if not match:
        if re.match(r"^[0-9.+-]+$", expr):
            # numeric literal
            return expr
        else:
            # treat as a variable => prefix with self.
            return f"self.{expr}"

    # We do have a function call
    func_name = match.group(1).upper()
    args_str = match.group(2).strip()

    # track usage
    used_blocks_set.add(func_name)

    # parse arguments (respect parentheses)
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
    if current:
        arg_str = "".join(current).strip()
        if arg_str:
            args.append(arg_str)

    parsed_args = [parse_formula(a, used_blocks_set) for a in args]

    # see if we have a known function
    info = FUNCTION_MAP.get(func_name)
    if not info:
        return f"# ERROR: Unknown function {func_name}"

    (min_args, max_args, template) = info
    if max_args is None:
        max_args = 99999

    if not (min_args <= len(parsed_args) <= max_args):
        return f"# ERROR: {func_name} expects {min_args}..{max_args} args, got {len(parsed_args)}"

    # handle special case: SUM(..., axis=-1)
    if func_name == "SUM" and len(parsed_args) == 2:
        axis_str = args[1].strip()
        axis_match = AXIS_SPEC_REGEX.match(axis_str)
        if axis_match:
            axis_val = axis_match.group(1).strip()
            return template.format(parsed_args[0], extra=f", axis={axis_val}")
        else:
            return "# ERROR: SUM(...) second arg not recognized"

    # normal function
    try:
        return template.format(*parsed_args, extra="")
    except IndexError:
        return f"# ERROR: mismatch placeholders in {func_name}"


def transform_formula(formula_str, used_blocks_set):
    """
    Attempt to parse the formula string into a Python expression.
    We also track which building-block function calls appear in formula_str
    by updating used_blocks_set.
    """
    if not formula_str:
        return "None"
    return parse_formula(formula_str, used_blocks_set)


def generate_class_code(entity, used_blocks_set):
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
            python_expr = transform_formula(formula, used_blocks_set)

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
        description="Generate Python classes from a JSON experiment rulebook. "
                    "Inject building-block function defs (SHIFT, BARRIER, etc.) into the output."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to input JSON file.")
    parser.add_argument("-o", "--output", required=True, help="Path to output .py file.")
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        entities = json.load(f)

    # We'll gather references to SHIFT, APPLY_BARRIER, etc.
    used_blocks = set()

    # Generate code for each entity
    classes_code = []
    for e in entities:
        class_code = generate_class_code(e, used_blocks)
        classes_code.append(class_code)

    # The lines that define the building blocks we used
    # We'll see which building blocks appear in used_blocks, then embed them
    required_defs = []
    for block_name in sorted(used_blocks):
        # only embed if we have a known block definition for it
        if block_name in BUILDING_BLOCKS:
            required_defs.append(BUILDING_BLOCKS[block_name])

    # If we want to be thorough, we might see references to e.g. "MATMUL" => we do a minimal def
    # but for now, let's assume SHIFT, BARRIER, GAUSSIAN_IN_Y, etc. are the main references.

    output_lines = []
    output_lines.append('"""')
    output_lines.append("Auto-generated Python code from your quantum-walk rulebook.")
    output_lines.append("It includes both the building-block definitions (SHIFT, BARRIER, etc.)")
    output_lines.append("and the classes with calculated fields referencing them.")
    output_lines.append('"""')
    output_lines.append("import math")
    output_lines.append("import numpy as np")
    output_lines.append("")
    output_lines.append("# ----- Building Block Lambdas (auto-injected) -----")
    output_lines.append("")

    # Insert required building blocks
    for block_def in required_defs:
        output_lines.append(block_def.strip())
        output_lines.append("")  # blank line

    output_lines.append("")
    output_lines.append("# ----- Generated classes below -----")
    output_lines.append("")

    for ccode in classes_code:
        output_lines.append(ccode)
        output_lines.append("")

    final_code = "\n".join(output_lines)
    with open(args.output, "w", encoding="utf-8") as out_f:
        out_f.write(final_code)

    print(f"Generated Python code written to {args.output}")
    if used_blocks:
        print("Detected usage of building blocks:", ", ".join(sorted(used_blocks)))


if __name__ == "__main__":
    main()
