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

SUPPORTED_AGG_FUNCS = {
    "COUNT": "COUNT",
    "SUM": "SUM",
    "MAX": "MAX",
    "IF": "IF",
    # You can add more here as needed (AVG, MINBY, etc.).
}

################################################################
#                 AGGREGATOR-TO-PYTHON REWRITING               #
################################################################

def aggregator_to_python(expr: str) -> str:
    """
    Transform aggregator expressions into Python code that references
    real aggregator calls from 'core_lambda_functions' where possible,
    including rewriting one-level-dot references like self.foo.bar
    into [x.bar for x in self.foo].
    """
    s = basic_cleanup(expr)
    s = aggregator_calls(s)           # e.g. MAX(...) => MAX(...)
    s = aggregator_subfield_rewrite(s)# rewrite self.foo.bar => [x.bar for x in self.foo]
    s = if_then_else_transform(s)
    s = domain_specific_fixes(s)
    s = remove_for_x_in_1(s)
    s = known_function_map(s)
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
        (r"\bthis\.", "self."),  # 'this.' => 'self.'
        (r"\bthis\b", "self"),   # standalone 'this' => 'self'
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
      AVG(...)   => ...
    etc.
    """
    s = expr
    # COUNT(...) => COUNT(...)
    s = re.sub(r"\bCOUNT\s*\(\s*(.*?)\s*\)", r"COUNT(\1)", s, flags=re.IGNORECASE)
    # SUM(...) => SUM(...)
    s = re.sub(r"\bSUM\s*\(\s*(.*?)\s*\)", r"SUM(\1)", s, flags=re.IGNORECASE)
    # MAX(...) => MAX(...)
    # Careful to avoid messing up "MAXBY(...)" (handled below), so we anchor carefully:
    s = re.sub(r"\bMAX\s*\(\s*(.*?)\)", r"MAX(\1)", s, flags=re.IGNORECASE)

    # AVERAGE(...) or AVG(...) => produce "AVG(...)"
    s = re.sub(r"\bAVERAGE\s*\(\s*(.*?)\)", r"AVG(\1)", s, flags=re.IGNORECASE)
    s = re.sub(r"\bAVG\s*\(\s*(.*?)\)", r"AVG(\1)", s, flags=re.IGNORECASE)

    # Placeholders for advanced aggregator calls not in core_lambda_functions
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


def aggregator_subfield_rewrite(expr: str) -> str:
    """
    Scans for aggregator calls like:
        COUNT(self.xyz.whatever)  => COUNT([x.whatever for x in self.xyz])
    Only if there's exactly one dot after 'self':
        self.foo           => no rewrite
        self.foo.bar       => rewrite to [x.bar for x in self.foo]
        self.foo.bar.baz   => produce # ERROR multiple-dot references...
    """
    pattern = re.compile(
        r"(COUNT|SUM|MAX|AVG|MINBY|MAXBY|MODE|TOPN|EXISTS)\(\s*(self\.[a-zA-Z_]\w*(?:\.[a-zA-Z_]\w*)?)\s*\)",
        re.IGNORECASE
    )

    def subfield_replacer(m):
        agg_func = m.group(1).upper()   # e.g. "MAX"
        param_expr = m.group(2)         # e.g. "self.angles.angle_degrees"

        parts = param_expr.split(".")    # e.g. ["self","angles","angle_degrees"]
        if len(parts) == 2:
            # aggregator(self.something)
            return f"{agg_func}({param_expr})"
        elif len(parts) == 3:
            # aggregator(self.something.somethingElse)
            coll_name = parts[1]
            field_name = parts[2]
            return f"{agg_func}([x.{field_name} for x in self.{coll_name}])"
        else:
            # More than one dot after 'self' => produce an error comment or skip rewriting
            return f"# ERROR multiple-dot references not supported: {m.group(0)}"

    return pattern.sub(subfield_replacer, expr)


def if_then_else_transform(expr: str) -> str:
    """
    Replace "IF (cond) THEN (val) ELSE (val)" => "IF(cond, val, val)"
    We'll do repeated passes for nested usage.
    """
    s = expr
    pattern = re.compile(r"\bIF\s*\((.*?)\)\s*THEN\s*\((.*?)\)\s*ELSE\s*\((.*?)\)",
                         re.IGNORECASE | re.DOTALL)
    while True:
        m = pattern.search(s)
        if not m:
            break
        cond = m.group(1).strip()
        val_then = m.group(2).strip()
        val_else = m.group(3).strip()
        new_expr = f"IF({cond}, {val_then}, {val_else})"
        s = s[:m.start()] + new_expr + s[m.end():]
    return s


def domain_specific_fixes(expr: str) -> str:
    """
    Additional replacements for domain-specific placeholders, e.g.
    CALCULATE_FOO(...) => calculate_foo(...), TEAM_PAYROLL(...) => team_payroll(...), etc.
    """
    s = expr

    # "CALCULATE_WOBA(" => "calculate_woba("
    s = re.sub(r"\bCALCULATE_([A-Z0-9_]+)\s*\(", lambda m: f"calculate_{m.group(1).lower()}(", s)

    # "WIN_PCT_BY_STADIUM_FUNCTION(" => "win_pct_by_stadium_function("
    s = re.sub(r"\bWIN_PCT_BY_STADIUM_FUNCTION\s*\(", "win_pct_by_stadium_function(", s)

    domain_map = {
        "TEAM_PAYROLL": "team_payroll",
        "LUXURY_TAX_THRESHOLD": "LUXURY_TAX_THRESHOLD",
        "allDesignatedHittersUsedUp": "all_designated_hitters_used_up",
        "CHECK_NO_OVERLAP_IN_ROOM_WITHOUT_BUFFER": "check_no_overlap_in_room_without_buffer",
    }
    for k,v in domain_map.items():
        s = re.sub(rf"\b{k}\s*\(", f"{v}(", s)

    return s


def remove_for_x_in_1(expr: str) -> str:
    """
    If aggregator rewriting introduced weird artifacts like:
        "for x in 1 for x in self.foo" => minimal cleanup.
    """
    s = expr
    s = re.sub(r"\sfor\s+\w+\s+in\s+1\s+for\s+\w+\s+in\s+", " for x in ", s)
    s = s.replace("x.x for x in", "x for x in")
    return s


def known_function_map(expr: str) -> str:
    """Optional final pass for leftover references."""
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
    for f in fields:
        ftype = f.get("type", "scalar")
        if ftype != "calculated":
            fname = f["name"]
            code_lines.append(f"        self.{fname} = kwargs.get('{fname}')")
            has_non_calc = True

    if not has_non_calc:
        code_lines.append("        pass")

    code_lines.append("")
    code_lines.append("        # If any 'one_to_many' or 'many_to_many' lookups exist, store them as collection wrappers.")

    # We might collect property methods for "target_entity": "this" in a list,
    # then append them at the bottom of the class.
    derived_properties = []

    for lu in lookups:
        lu_type = lu.get("type")
        lu_name = lu.get("name")
        lu_target = lu.get("target_entity", "")
        join_cond = lu.get("join_condition", "")
        lu_desc = lu.get("description", "")

        # If target_entity is NOT "this", do normal one_to_many
        if lu_target.lower() != "this":
            if lu_type in ("one_to_many", "many_to_many"):
                code_lines.append(f"        self.{lu_name} = CollectionWrapper(self, '{lu_name}')")
        else:
            # "target_entity": "this" => interpret as "derived property"
            # e.g. join_condition = "this.angles.angle_degrees"
            parts = join_cond.split(".")  # e.g. ["this", "angles", "angle_degrees"]
            if len(parts) == 3 and parts[0].lower() == "this":
                collection_name = parts[1]
                field_name = parts[2]
                # Generate a Python property that returns `[x.field_name for x in self.collection_name]`
                # We'll store in derived_properties and add them later
                prop_def = textwrap.dedent(f"""
                @property
                def {lu_name}(self):
                    \"\"\"{lu_desc}\"\"\"
                    return [x.{field_name} for x in self.{collection_name}]
                """).strip("\n")
                derived_properties.append(prop_def)
            else:
                # If the join_condition doesn't match "this.foo.bar" pattern, skip or handle differently
                # We'll just put a comment for now:
                code_lines.append(f"        # Skipping unusual 'target_entity=this' lookup: {lu_name}, {join_cond}")

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

    # Finally, append any derived properties for "target_entity": "this"
    if derived_properties:
        code_lines.append("")
        code_lines.append("    # Derived properties for 'target_entity': 'this'")
        for dp in derived_properties:
            for line in dp.splitlines():
                code_lines.append("    " + line)

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

    # If SHIFT/EVOLVE were found, import them:
    ext_imports = sorted(used_blocks.intersection(BUILDING_BLOCKS.keys()))
    if ext_imports:
        module_name = "quantum_walk_blocks"  # or whatever your module is called
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

    # Below are aggregator stubs not yet in core_lambda_functions:
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

    # Optional sample_main
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
