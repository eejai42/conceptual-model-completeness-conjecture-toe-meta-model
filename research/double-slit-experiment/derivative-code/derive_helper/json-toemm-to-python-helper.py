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
- It also injects the reusable function definitions (SHIFT, APPLY_BARRIER, EVOLVE, etc.)
  directly into the generated output, so we have a single self-contained .py file.
- The EVOLVE function can contain that single time-loop over steps, but is
  included the same way SHIFT or BARRIER are included: as a "building block."

Usage:
  python json-toemm-to-python-helper.py -i my-experiment.json -o my-exp-helper.py
"""

# ------------------------------------------------------------------------
# 0) Some sample "building block" functions we might embed in the output
# ------------------------------------------------------------------------
# We'll keep them as strings. Our code will inject them at the top of the final file
# if we see references to SHIFT, APPLY_BARRIER, EVOLVE, etc. in your JSON formulas.

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
    "EVOLVE": textwrap.dedent("""\
        def EVOLVE(psi_init, steps_to_barrier, steps_after_barrier, collapse_barrier,
                   coin_matrix, offsets,
                   barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend):
            \"\"\"
            Example function to do a quantum-walk evolution with a single time loop.
            coin -> shift -> barrier, repeated 'steps_to_barrier' times,
            optional measurement,
            then repeated 'steps_after_barrier' times.
            \"\"\"
            import numpy as np

            psi = psi_init
            for _ in range(steps_to_barrier):
                # coin step
                ny, nx, spin_dim = psi.shape
                psi_flat = psi.reshape(ny*nx, spin_dim)
                out_flat = psi_flat @ coin_matrix.T
                psi_coin = out_flat.reshape((ny,nx,spin_dim))

                # shift step
                psi_shift = SHIFT(psi_coin, offsets)

                # barrier step
                psi = APPLY_BARRIER(psi_shift, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend)

            if collapse_barrier:
                psi = COLLAPSE_BARRIER(psi, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend)

            for _ in range(steps_after_barrier):
                ny, nx, spin_dim = psi.shape
                psi_flat = psi.reshape(ny*nx, spin_dim)
                out_flat = psi_flat @ coin_matrix.T
                psi_coin = out_flat.reshape((ny,nx,spin_dim))

                psi_shift = SHIFT(psi_coin, offsets)
                psi = APPLY_BARRIER(psi_shift, barrier_row, slit1_xstart, slit1_xend, slit2_xstart, slit2_xend)

            return psi
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
    "SQRT": (1, 1, "math.sqrt({0})"),
    "LEN": (1, 1, "len({0})"),
    "ADD":      (2, 2, "({0} + {1})"),
    "SUBTRACT": (2, 2, "({0} - {1})"),
    "MULTIPLY": (2, 2, "np.matmul({0}, {1})"),   # for matrix multiply (if appropriate)
    "DIVIDE":   (2, 2, "({0} / {1})"),
    "POWER":   (2, 2, "({0} ** {1})"),
    "FLOOR":    (1, 1, "math.floor({0})"),
    "ABS":      (1, 1, "np.abs({0})"),
    "SUM_OVER": (2, 2, "sum(getattr(item, '{1}') for item in self.{0})"),
    "MAX_OVER": (2, 2, "max(getattr(item, '{1}') for item in self.{0})"),
    # For checking unitarity, might do EQUAL => np.allclose
    "EQUAL":    (2, 2, "np.allclose({0}, {1})"),
    "IF": (3, 3, "({1} if {0} else {2})"),
    
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

    # EVOLVE(...) => "EVOLVE(psi_init, steps_to_barrier, steps_after_barrier, collapse_barrier, coin_matrix, offsets, barrier_row, ...)"
    # We'll assume exactly 10 args for demonstration, or you can refine:
    "EVOLVE": (10, 10, "EVOLVE({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9})"),

    # SUM( X, axis=-1 ) => "np.sum(X, axis=-1)" or similar
    "SUM": (1, 2, "np.sum({0}{extra})"),
}

AXIS_SPEC_REGEX = re.compile(r"^axis\\s*=\\s*(.*)$", re.IGNORECASE)
POWER2_REGEX = re.compile(r"^(.*)\\^2$")
#POWER2_REGEX = re.compile(r"^(.*)\^2$")  # Ensures it captures "X^2"
FUNC_CALL_REGEX = re.compile(r"^([A-Z_]+)\((.*)\)$", re.IGNORECASE)


def parse_formula(expr, used_blocks_set):
    """
    Recursive parser to convert expressions into Python code.
    Also tracks which building block names appear.
    """
    expr = expr.strip()

    # Fix: Parse exponentiation (^2) properly
    pow_match = POWER2_REGEX.match(expr)
    if pow_match:
        sub_expr = pow_match.group(1).strip()
        parsed_sub = parse_formula(sub_expr, used_blocks_set)  # Ensure SUBTRACT inside is handled first
        return f"({parsed_sub}**2)"  # Correct Python exponentiation

    # Check for function calls
    match = FUNC_CALL_REGEX.match(expr)
    if not match:
        # numeric literal?
        if re.match(r"^[0-9.+-]+$", expr):
            return expr
        # variable => prefix with self.
        return f"self.{expr}"

    func_name = match.group(1).upper()
    args_str = match.group(2).strip()

    # Track usage
    used_blocks_set.add(func_name)

    # Parse function arguments (respect parentheses)
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

    parsed_args = [parse_formula(a, used_blocks_set) for a in args]

    # Lookup function in FUNCTION_MAP
    info = FUNCTION_MAP.get(func_name)
    if not info:
        return f"# ERROR: Unknown function {func_name}"

    min_args, max_args, template = info
    if not (min_args <= len(parsed_args) <= max_args):
        return f"# ERROR: {func_name} expects {min_args}..{max_args} args, got {len(parsed_args)}"

    # Normal function fill
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

    # produce read-only @property for any "calculated" fields
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
            code_lines.append(f"        \"\"\"")
            if pyexpr.startswith("# ERROR"):
                code_lines.append(f"        # Parser error for formula: {formula}")
                code_lines.append("        return None")
            else:
                code_lines.append(f"        return {pyexpr}")

    return "\n".join(code_lines)

###############################
# The main code generation
###############################
def main():
    parser = argparse.ArgumentParser(
        description="Generate Python classes from a JSON experiment rulebook. "
                    "Inject building-block function defs (SHIFT, BARRIER, EVOLVE, etc.) into the output."
    )
    parser.add_argument("-i","--input",required=True,help="Path to input JSON file.")
    parser.add_argument("-o","--output",required=True,help="Path to output .py file.")
    parser.add_argument("--include-sample-main",action="store_true",
        help="If set, also inject a sample_main() function demonstration.")
    args = parser.parse_args()

    with open(args.input,"r",encoding="utf-8") as f:
        entities = json.load(f)

    used_blocks = set()
    class_codes = []
    for e in entities:
        code = generate_class_code(e, used_blocks)
        class_codes.append(code)

    # figure out which building block function definitions to embed
    required_defs = []
    for block_name in sorted(used_blocks):
        if block_name in BUILDING_BLOCKS:
            required_defs.append(BUILDING_BLOCKS[block_name])

    output_lines = []
    output_lines.append('"""')
    output_lines.append("Auto-generated Python code from your quantum-walk rulebook.")
    output_lines.append("It includes building-block definitions (SHIFT, BARRIER, EVOLVE, etc.)")
    output_lines.append("and the classes with calculated fields referencing them.")
    output_lines.append('"""')
    output_lines.append("import math")
    output_lines.append("import numpy as np")
    output_lines.append("")

    output_lines.append("# ----- Building Block Lambdas (auto-injected) -----")
    output_lines.append("")
    for block_def in required_defs:
        output_lines.append(block_def.strip())
        output_lines.append("")

    output_lines.append("# ----- Generated classes below -----")
    output_lines.append("")
    for cc in class_codes:
        output_lines.append(cc)
        output_lines.append("")

    if args.include_sample_main:
        # We'll embed a minimal sample_main
        sample_main_str = textwrap.dedent("""\
        def sample_main():
            \"\"\"
            Minimal demonstration of how to use the auto-generated classes and building blocks.
            Adjust parameters as desired (201x201, step counts, etc.).
            \"\"\"
            # Typically you'd do something like:
            # 1) Instantiate your Grid
            # 2) Instantiate your initial wavefunction
            # 3) Possibly define a coin matrix
            # 4) If you have an entity with formula = EVOLVE(...), then create that entity
            #    and read its final_wavefunction, etc.
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
    if used_blocks:
        print("Detected usage of building blocks:", ", ".join(sorted(used_blocks)))


if __name__=="__main__":
    main()
