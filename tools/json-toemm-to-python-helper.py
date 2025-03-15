#!/usr/bin/env python3

import json
import argparse
import math
import re
import textwrap
import os

################################################################
# 0) We'll define the aggregator building-blocks we recognize. #
################################################################

BUILDING_BLOCKS = {
    "SHIFT": "",
    "APPLY_BARRIER": "",
    "COLLAPSE_BARRIER": "",
    "GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION": "",
    "EVOLVE": "",
}

################################################################
# 1) Mappings for recognized function calls used in aggregator  #
################################################################

# We used to define _COUNT, _SUM, etc. inline. Now we'll import them
# from your 'core_lambda_functions' module where you have COUNT, SUM, ...
# We also keep placeholders for aggregator calls that are not yet in that module.

# We'll define a check or partial map:
SUPPORTED_AGG_FUNCS = {
    "COUNT": "COUNT",  # maps to core_lambda_functions.COUNT
    "SUM": "SUM",      # maps to core_lambda_functions.SUM
    "MAX": "MAX",      # maps to core_lambda_functions.MAX
    "IF": "IF",        # maps to core_lambda_functions.IF
    # The user’s file defines these. We can add "EQUAL", "CONTAINS" if we want to handle them too
    # For advanced aggregator calls (AVG, MINBY, TOPN, etc.) we have no real code in core_lambda_functions.py
    # We'll just generate stubs for them. 
}

################################################################
#                 AGGREGATOR-TO-PYTHON REWRITING               #
################################################################

def aggregator_to_python(expr: str) -> str:
    """
    Transform aggregator expressions into Python code that references
    real aggregator calls from 'core_lambda_functions' where possible.
    """
    # Step 1: Basic lexical replacements (AND->and, etc.)
    s = basic_cleanup(expr)

    # Step 2: Detect aggregator function calls: COUNT(...), SUM(...), etc.
    s = aggregator_calls(s)

    # Step 3: Convert "IF (cond) THEN (val) ELSE (val)" => "IF(cond, val, val)"
    s = if_then_else_transform(s)

    # Step 4: Domain-specific fixes
    s = domain_specific_fixes(s)

    # Step 5: Some leftover patterns like "for x in 1" => remove them
    s = remove_for_x_in_1(s)

    # Step 6: Last pass for known function mapping (TEAM_PAYROLL => team_payroll, etc.)
    s = known_function_map(s)

    # Final tidy
    return s.strip()


def basic_cleanup(expr: str) -> str:
    """Replace common aggregator keywords with Python equivalents (AND->and, etc.)."""
    s = expr
    replacements = [
        (r"\bAND\b", " and "),
        (r"\bOR\b", " or "),
        (r"\bNOT\b", " not "),
        (r"\bNULL\b", "None"),
        (r"\btrue\b", "True"),
        (r"\bfalse\b", "False"),
        (r"\bnull\b", "None"),
        (r"\bthis\.", "self."),
        (r"\bthis\b", "self"),
    ]
    for pat, rep in replacements:
        s = re.sub(pat, rep, s, flags=re.IGNORECASE)

    # Convert single '=' to '==' if not part of '>=', '<=', '==', '!='
    s = re.sub(r"(?<![=!<>])=+(?![=>\]])", "==", s)

    # e.g. "IN [.." => " in [.."
    s = re.sub(r"\sIN\s*\[", " in [", s, flags=re.IGNORECASE)

    return s


def aggregator_calls(expr: str) -> str:
    """
    Transform recognized aggregator calls:
      COUNT(...) => COUNT(...)
      SUM(...)   => SUM(...)
      MAX(...)   => MAX(...)
      AVG(...)   => ???

    We'll produce partial stubs for aggregator calls that do not exist yet in core_lambda_functions.
    """
    s = expr
    # COUNT(...) => COUNT(...)
    s = re.sub(r"\bCOUNT\s*\(\s*(.*?)\s*\)", r"COUNT(\1)", s, flags=re.IGNORECASE)
    # SUM(...) => SUM(...)
    s = re.sub(r"\bSUM\s*\(\s*(.*?)\s*\)", r"SUM(\1)", s, flags=re.IGNORECASE)
    # MAX(...) => MAX(...)
    # We'll do that carefully to avoid messing up "MAXBY(...)" which we'll handle below.
    s = re.sub(r"\bMAX\s*\(\s*(.*?)\)", r"MAX(\1)", s, flags=re.IGNORECASE)

    # We have no real "AVG" in core_lambda_functions. We'll produce "AVG(...)"
    s = re.sub(r"\bAVERAGE\s*\(\s*(.*?)\)", r"AVG(\1)", s, flags=re.IGNORECASE)
    s = re.sub(r"\bAVG\s*\(\s*(.*?)\)", r"AVG(\1)", s, flags=re.IGNORECASE)

    # The user didn't define MINBY, MAXBY, MODE, etc. We'll produce placeholders
    s = re.sub(r"\bMINBY\s*\(\s*(.*?)\)", r"MINBY(\1)", s, flags=re.IGNORECASE)
    s = re.sub(r"\bMAXBY\s*\(\s*(.*?)\)", r"MAXBY(\1)", s, flags=re.IGNORECASE)
    s = re.sub(r"\bMODE\s*\(\s*(.*?)\)", r"MODE(\1)", s, flags=re.IGNORECASE)
    s = re.sub(r"\bTOPN\s*\(\s*(.*?)\)", r"TOPN(\1)", s, flags=re.IGNORECASE)

    # EXISTS(...) => EXISTS(...)
    s = re.sub(r"\bEXISTS\s*\(\s*(.*?)\s*\)", r"EXISTS(\1)", s, flags=re.IGNORECASE)

    # POWER(a,2) => (a**2)
    s = re.sub(r"\bPOWER\s*\(\s*(.*?),\s*2\s*\)", r"(\1**2)", s, flags=re.IGNORECASE)

    # ABS(...) => abs(...)
    s = re.sub(r"\bABS\s*\(\s*(.*?)\s*\)", r"abs(\1)", s, flags=re.IGNORECASE)

    return s


def if_then_else_transform(expr: str) -> str:
    """
    Replace "IF (cond) THEN (val) ELSE (val)" => "IF(cond, val, val)"
    We'll do repeated passes for nested usage.
    """
    s = expr
    pattern = re.compile(r"\bIF\s*\((.*?)\)\s*THEN\s*\((.*?)\)\s*ELSE\s*\((.*?)\)", re.IGNORECASE|re.DOTALL)
    while True:
        m = pattern.search(s)
        if not m:
            break
        cond = m.group(1).strip()
        val_then = m.group(2).strip()
        val_else = m.group(3).strip()
        # Replace with "IF(cond, val_then, val_else)"
        new_expr = f"IF({cond}, {val_then}, {val_else})"
        s = s[:m.start()] + new_expr + s[m.end():]
    return s


def domain_specific_fixes(expr: str) -> str:
    """
    Additional replacements like "MAX(" => "MAX(", leftover "CALCULATE_SOMETHING" => "calculate_something",
    "TEAM_PAYROLL(" => "team_payroll(" etc.
    """
    s = expr

    # Some advanced aggregator placeholders => e.g. "CALCULATE_WOBA(" => "calculate_woba("
    s = re.sub(r"\bCALCULATE_([A-Z0-9_]+)\s*\(", lambda m: f"calculate_{m.group(1).lower()}(", s)

    # e.g. "WIN_PCT_BY_STADIUM_FUNCTION(" => "win_pct_by_stadium_function("
    s = re.sub(r"\bWIN_PCT_BY_STADIUM_FUNCTION\s*\(", "win_pct_by_stadium_function(", s)

    # Example domain calls => "TEAM_PAYROLL(" => "team_payroll("
    # We'll do a quick dictionary:
    domain_map = {
        "TEAM_PAYROLL": "team_payroll",
        "LUXURY_TAX_THRESHOLD": "LUXURY_TAX_THRESHOLD",  # maybe a constant
        "allDesignatedHittersUsedUp": "all_designated_hitters_used_up",
        "CHECK_NO_OVERLAP_IN_ROOM_WITHOUT_BUFFER": "check_no_overlap_in_room_without_buffer",  # e.g.
    }
    for k,v in domain_map.items():
        s = re.sub(rf"\b{k}\s*\(", f"{v}(", s)

    return s


def remove_for_x_in_1(expr: str) -> str:
    """
    If aggregator rewriting introduced "for x in 1 for x in self.foo" etc.:
    We'll do minimal pass.
    """
    s = expr
    s = re.sub(r"\sfor\s+\w+\s+in\s+1\s+for\s+\w+\s+in\s+", " for x in ", s)
    s = s.replace("x.x for x in", "x for x in")
    return s


def known_function_map(expr: str) -> str:
    """
    If leftover references to e.g. "TEAM_PAYROLL( this.id )" or "POWER()", we fix them.
    Already done above, but let's finalize a pass.
    """
    s = expr
    return s


def parse_formula(expr, used_blocks_set):
    """
    Runs aggregator_to_python, also checks if SHIFT/EVOLVE references appear => add to used_blocks.
    """
    expr_py = aggregator_to_python(expr)
    if "SHIFT(" in expr_py:
        used_blocks_set.add("SHIFT")
    if "EVOLVE(" in expr_py:
        used_blocks_set.add("EVOLVE")
    return expr_py


def transform_formula(formula_str, used_blocks_set):
    """Convert a formula string into Python code or 'None' if empty."""
    if not formula_str:
        return "None"
    return parse_formula(formula_str, used_blocks_set)


################################################################
#   Code generator for the classes (like generate_class_code)   #
################################################################

def generate_class_code(entity, used_blocks_set):
    class_name = entity["name"]
    fields = entity.get("fields", [])
    lookups = entity.get("lookups", [])
    aggregations = entity.get("aggregations", [])

    code_lines = []
    code_lines.append(f"class {class_name}:")
    code_lines.append(f'    """Plain data container for {class_name} entities."""')
    code_lines.append("    def __init__(self, **kwargs):")

    has_non_calc = False
    # handle normal fields
    for f in fields:
        ftype = f.get("type", "scalar")
        if ftype != "calculated":
            fname = f["name"]
            code_lines.append(f"        self.{fname} = kwargs.get('{fname}')")
            has_non_calc = True

    if not has_non_calc:
        code_lines.append("        pass")

    # handle lookups of type one_to_many / many_to_many => define a CollectionWrapper
    code_lines.append("")
    code_lines.append("        # If any 'one_to_many' or 'many_to_many' lookups exist, store them as collection wrappers.")
    for lu in lookups:
        lu_type = lu.get("type")
        lu_name = lu.get("name")
        if lu_type in ("one_to_many", "many_to_many"):
            code_lines.append(f"        self.{lu_name} = CollectionWrapper(self, '{lu_name}')")

    # aggregator fields from 'fields' if type=calculated
    for f in fields:
        if f.get("type") == "calculated":
            formula = f.get("formula","")
            desc = f.get("description","")
            pyexpr = transform_formula(formula, used_blocks_set)
            prop_name = f["name"]
            code_lines.append("")
            code_lines.append("    @property")
            code_lines.append(f"    def {prop_name}(self):")
            code_lines.append(f"        \"\"\"{desc}\n        Original formula: {formula}\n        \"\"\"")
            code_lines.append(f"        return {pyexpr}")

    # aggregator fields from "aggregations"
    for agg in aggregations:
        formula = agg.get("formula","")
        desc = agg.get("description","")
        name = agg["name"]
        pyexpr = transform_formula(formula, used_blocks_set)

        code_lines.append("")
        code_lines.append("    @property")
        code_lines.append(f"    def {name}(self):")
        code_lines.append(f"        \"\"\"{desc}\n        Original formula: {formula}\n        \"\"\"")
        code_lines.append(f"        return {pyexpr}")

    return "\n".join(code_lines)


################################################################
# 2) Main CLI that reads the JSON and writes a .py file         #
################################################################

def main():
    parser = argparse.ArgumentParser(
        description="Generate Python classes from a JSON-based meta-model, referencing aggregator calls in core_lambda_functions."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to input JSON file.")
    parser.add_argument("-o", "--output", required=True, help="Path to output .py file.")
    parser.add_argument("--include-sample-main", action="store_true",
        help="If set, also inject a sample_main() function demonstration.")
    args = parser.parse_args()

    with open(args.input,"r",encoding="utf-8") as f:
        data = json.load(f)
        # We'll assume structure: data["meta-model"]["schema"]["entities"]
        entities = data["meta-model"]["schema"]["entities"]

    used_blocks = set()
    class_codes = []
    for e in entities:
        code = generate_class_code(e, used_blocks)
        class_codes.append(code)

    # Build final output
    output_lines = []
    output_lines.append('"""')
    output_lines.append("Auto-generated Python code from your domain model.")
    output_lines.append("Now with aggregator rewriting that references core_lambda_functions.")
    output_lines.append('"""')
    output_lines.append("import math")
    output_lines.append("import numpy as np")

    # We assume you have 'core_lambda_functions.py' with COUNT, SUM, MAX, etc.:
    output_lines.append("from core_lambda_functions import COUNT, SUM, MAX, IF, CONTAINS, EQUAL")

    # If SHIFT/EVOLVE were found, we import them from quantum_walk_blocks
    ext_imports = sorted(used_blocks.intersection(BUILDING_BLOCKS.keys()))
    if ext_imports:
        module_name = "quantum_walk_blocks"  # example
        i_list = ", ".join(ext_imports)
        output_lines.append(f"from {module_name} import {i_list}")

    aggregator_helpers = textwrap.dedent("""\
    import uuid
    import re

    class CollectionWrapper:
        \"\"\"A tiny helper so we can do something like: obj.someLookup.add(item).\"\"\"
        def __init__(self, parent_object, attr_name):
            self.parent_object = parent_object
            self.attr_name = attr_name
            if not hasattr(parent_object, '_collections'):
                parent_object._collections = {}
            if attr_name not in parent_object._collections:
                parent_object._collections[attr_name] = []

        def add(self, item):
            self.parent_object._collections[self.attr_name].append(item)

        def __iter__(self):
            return iter(self.parent_object._collections[self.attr_name])

        def __len__(self):
            return len(self.parent_object._collections[self.attr_name])

        def __getitem__(self, index):
            return self.parent_object._collections[self.attr_name][index]

    # Below are aggregator stubs we haven't yet implemented in core_lambda_functions:
    # e.g. 'AVG', 'EXISTS', 'MINBY', 'MODE', 'TOPN', 'MAXBY'
    def AVG(collection):
        \"\"\"Placeholder aggregator: real logic not yet implemented.\"\"\"
        # Could do: return sum(collection)/len(collection) if numeric
        return f\"/* AVG not implemented: {collection} */\"

    def EXISTS(condition_expr):
        return f\"/* EXISTS not implemented: {condition_expr} */\"

    def MINBY(expr):
        return f\"/* MINBY not implemented: {expr} */\"

    def MAXBY(expr):
        return f\"/* MAXBY not implemented: {expr} */\"

    def MODE(expr):
        return f\"/* MODE not implemented: {expr} */\"

    def TOPN(expr):
        return f\"/* TOPN not implemented: {expr} */\"
    """)

    output_lines.append("")
    output_lines.append(aggregator_helpers)
    output_lines.append("")

    # Then generate each class code
    output_lines.append("# ----- Generated classes below -----\n")
    for cc in class_codes:
        output_lines.append(cc)
        output_lines.append("")

    # If we want a sample_main
    if args.include_sample_main:
        sample_main_str = textwrap.dedent("""\
        def sample_main():
            \"\"\"
            Minimal demonstration of how to use the auto-generated classes.
            \"\"\"
            print("sample_main() not fully implemented.  You can create objects and call aggregator properties here.")

        if __name__ == "__main__":
            sample_main()
        """)
        output_lines.append(sample_main_str)
        output_lines.append("")

    final_code = "\n".join(output_lines)
    with open(args.output,"w",encoding="utf-8") as out_f:
        out_f.write(final_code)

    print(f"Generated Python code written to {args.output}")
    if ext_imports:
        print("Detected usage of building blocks:", ", ".join(ext_imports))


if __name__=="__main__":
    main()
