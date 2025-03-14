#!/usr/bin/env python3

import json
import argparse
import math
import re
import textwrap
import os

import_statistics = False  # We'll set True if aggregator_to_python sees "AVG(...)".

# For SHIFT, EVOLVE references, etc.
BUILDING_BLOCKS = {
    "SHIFT": "",
    "APPLY_BARRIER": "",
    "COLLAPSE_BARRIER": "",
    "GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION": "",
    "EVOLVE": "",
}

################################################################
#                 AGGREGATOR-TO-PYTHON REWRITING               #
################################################################

# We'll define a big multi-step transform that tries to produce
# real Python code from aggregator expressions. The goal is to
# remove leftover aggregator keywords or partial steps that cause
# syntax errors like "IF x THEN y ELSE z", "some for x in 1 for x in ...",
# "this." references, "null" => "None", "true" => "True", etc.
#
# We'll do these transformations in multiple passes.

def aggregator_to_python(expr: str) -> str:
    """High-level aggregator rewriting pipeline: run multiple sub-steps."""
    # 1) Basic cleanup replacements: "AND"->"and", "OR"->"or", etc.
    e = basic_cleanup(expr)

    # 2) Transform aggregator calls: COUNT(...), SUM(...), etc. => Pythonic
    e = aggregator_calls(e)

    # 3) Perform second-phase rewriting to fix leftover "IF" => " ( ... if ... else ...) "
    e = if_then_else_transform(e)

    # 4) Attempt to unify "this.foo" => "self.foo", "NOT" => "not", "true" => "True", etc.
    e = domain_specific_fixes(e)

    # 5) Try removing nonsense like "sum(x.x for x in 1 for x in self.Stuff...)" => "sum(1 for x in self.Stuff...)"
    e = remove_for_x_in_1(e)

    # 6) Fix leftover ephemeral placeholders like "TEAM_PAYROLL( self.id )" => "team_payroll(self.id)"
    e = known_function_map(e)

    # 7) Final pass of parentheses check or bracket spacing is optional
    e = e.strip()

    return e


def basic_cleanup(expr: str) -> str:
    """Replace common aggregator keywords with Python equivalents (AND->and, etc.)."""
    s = expr
    # "AND"-> "and", "OR"->"or", "NULL"->"None", "true"->"True", "false"->"False"
    # We'll do them carefully with regex ignoring case
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

    # Replace single '=' with '==' if not already '==', '>=', '<=', '!='
    # We'll do a small pattern that doesn't match '==', etc.
    # For example, "x=3" => "x==3"
    # We'll skip if there's a bracket after it e.g. "result in ['SINGLE',...]" is separate
    s = re.sub(r"(?<![=!<>])=+(?![=>\]])", "==", s)

    # We also handle "IN [" => " in ["
    s = re.sub(r"\sIN\s*\[", " in [", s, flags=re.IGNORECASE)

    return s


def aggregator_calls(expr: str) -> str:
    """
    Detect aggregator calls like COUNT(...), SUM(...), AVG(...), MINBY(...), MAXBY(...), MODE(...), TOPN(...).
    We'll do something akin to your earlier approach but more incremental.
    """
    global import_statistics
    s = expr

    # handle COUNT, SUM, AVG with a simple approach:
    s = re.sub(r"\bCOUNT\s*\(\s*(.*?)\s*\)", r"_COUNT(\1)", s, flags=re.IGNORECASE)
    s = re.sub(r"\bSUM\s*\(\s*(.*?)\s*\)", r"_SUM(\1)", s, flags=re.IGNORECASE)
    if re.search(r"\bAVG\s*\(", s, flags=re.IGNORECASE):
        import_statistics = True
    s = re.sub(r"\bAVG\s*\(\s*(.*?)\s*\)", r"_AVG(\1)", s, flags=re.IGNORECASE)

    # MINBY(...) => _MINBY(...)
    # MAXBY(...) => _MAXBY(...)
    s = re.sub(r"\bMINBY\s*\((.*?)\)", r"_MINBY(\1)", s, flags=re.IGNORECASE)
    s = re.sub(r"\bMAXBY\s*\((.*?)\)", r"_MAXBY(\1)", s, flags=re.IGNORECASE)

    # MODE(...) => _MODE(...)
    # TOPN(...) => _TOPN(...)
    if re.search(r"\bMODE\s*\(", s, flags=re.IGNORECASE):
        import_statistics = True
    s = re.sub(r"\bMODE\s*\((.*?)\)", r"_MODE(\1)", s, flags=re.IGNORECASE)
    s = re.sub(r"\bTOPN\s*\((.*?)\)", r"_TOPN(\1)", s, flags=re.IGNORECASE)

    # EXISTS(...) => _EXISTS(...)
    s = re.sub(r"\bEXISTS\s*\((.*?)\)", r"_EXISTS(\1)", s, flags=re.IGNORECASE)

    # POWER(a,2) => (a**2)
    s = re.sub(r"\bPOWER\s*\(\s*(.*?),\s*2\s*\)", r"(\1**2)", s, flags=re.IGNORECASE)

    # ABS(...) => abs(...)
    s = re.sub(r"\bABS\s*\(\s*(.*?)\s*\)", r"abs(\1)", s, flags=re.IGNORECASE)

    # custom aggregator calls "CALCULATE_...", "WIN_PCT_BY_STADIUM_FUNCTION", etc. we do later
    return s


def if_then_else_transform(expr: str) -> str:
    """
    Transform "IF (cond) THEN (val) ELSE (val)" => "(val if cond else val)".
    We'll do it repeatedly in a loop in case multiple nested expressions exist.
    """
    s = expr
    pattern = re.compile(r"\bIF\s*\((.*?)\)\s*THEN\s*\((.*?)\)\s*ELSE\s*\((.*?)\)", re.IGNORECASE|re.DOTALL)

    # We'll do a loop in case there are multiple occurrences
    while True:
        m = pattern.search(s)
        if not m:
            break
        cond = m.group(1).strip()
        val_then = m.group(2).strip()
        val_else = m.group(3).strip()
        # we can recursively transform them but let's do simple
        new_expr = f"(({val_then}) if ({cond}) else ({val_else}))"
        s = s[:m.start()] + new_expr + s[m.end():]
    return s


def domain_specific_fixes(expr: str) -> str:
    """
    Additional replacements: leftover "IF" => something, "MAX(" => "max(",
    "MIN(" => "min(", "TEAM_PAYROLL(" => "team_payroll(", "CALC_..." => "calc_..."
    Also "null" => "None", etc. We handle "IN" calls, "someMethod( this.id ) => some_method(self.id)" if we like
    """
    s = expr

    # Replace "MAX(" => "max("
    s = re.sub(r"\bMAX\s*\(", "max(", s)
    # Replace "MIN(" => "min("
    s = re.sub(r"\bMIN\s*\(", "min(", s)

    # If leftover "IF" occurs outside context, let's just do a naive approach. 
    # But we *did* handle "IF (cond) THEN (a) ELSE (b)" above. 
    # We'll remove any leftover "IF"? Hard to say. Let's skip for now.

    # Replace leftover "CALCULATE_.*?\(" => "calculate_...("
    # e.g. "CALCULATE_WOBA(" => "calculate_woba("
    s = re.sub(r"\bCALCULATE_([A-Z0-9_]+)\s*\(", 
               lambda m: f"calculate_{m.group(1).lower()}(", 
               s)

    # e.g. "WIN_PCT_BY_STADIUM_FUNCTION(" => "win_pct_by_stadium_function("
    s = re.sub(r"\bWIN_PCT_BY_STADIUM_FUNCTION\s*\(", "win_pct_by_stadium_function(", s)

    # Some domain calls might need a dictionary approach. We'll do a partial:
    domain_map = {
      "TEAM_PAYROLL": "team_payroll",
      "LUXURY_TAX_THRESHOLD": "LUXURY_TAX_THRESHOLD",  # might be a constant
      "allDesignatedHittersUsedUp": "all_designated_hitters_used_up",
      "POWER": "**",  # we handled in aggregator_calls though
    }
    # We'll do a small pass:
    for k,v in domain_map.items():
        s = re.sub(rf"\b{k}\s*\(", f"{v}(", s)

    # "TEAM_PAYROLL( self.id )" => "team_payroll(self.id)" done above
    # "someMethod( this.id )" => "some_method(self.id)" is guessy. 
    # We'll skip or define a general approach if we see "this.id" => "self.id"

    # "p.x for p in self.x => we keep it
    return s


def remove_for_x_in_1(expr: str) -> str:
    """
    If we see something like "sum(x.x for x in 1 for x in self.Whatever if ...)", 
    let's fix it. We'll produce "sum(1 for x in self.Whatever if ...)" or "sum(x.xxx for x in self.Whatever if ...)" 
    depending on context.

    This is extremely heuristic. We'll attempt a minimal pass:
    - replace "for x in 1 for x in self.<something>" => "for x in self.<something>"
    - if we see "x.x for x in ???" with no real field, we might do "1 for x in ???"
    """
    s = expr
    # remove " for x in 1 for x in self..."
    s = re.sub(r"\sfor\s+\w+\s+in\s+1\s+for\s+\w+\s+in\s+", " for x in ", s)
    # also if we see "sum(x.x for x in self..." we might do "sum(x for x in self..."
    # but it's not trivial to guess. We'll do a naive approach: "x.x" => "x"
    s = s.replace("x.x for x in", "x for x in")
    return s


def known_function_map(expr: str) -> str:
    """
    If leftover "IF" or "TEAM_PAYROLL" or "someMethod( this.id )" exist, 
    we fix or fallback. E.g. "IF x>0 THEN y ELSE z" might be leftover. 
    We'll do minimal. We already handled if-then-else. We'll also handle "calc_*" references. 
    """
    s = expr

    # "IF(...) THEN(...) ELSE(...)" we handled. If any remain, fallback to ...
    # "TEAM_PAYROLL(" => "team_payroll("
    # Already replaced above. 
    # "POWER" => we replaced. 
    return s


################################################################
#   The aggregator placeholders we'll define as Python calls   #
#   _COUNT, _SUM, _AVG, _MINBY, _MAXBY, _MODE, _TOPN, _EXISTS  #
################################################################

def parse_formula(expr, used_blocks_set):
    # aggregator_to_python is main
    expr_py = aggregator_to_python(expr)
    # SHIFT(...) => used_blocks_set.add("SHIFT")
    if "SHIFT(" in expr_py:
        used_blocks_set.add("SHIFT")
    if "EVOLVE(" in expr_py:
        used_blocks_set.add("EVOLVE")
    return expr_py


def transform_formula(formula_str, used_blocks_set):
    if not formula_str:
        return "None"
    return parse_formula(formula_str, used_blocks_set)


################################################################
#   Code for "generate_class_code" and "main" mostly unchanged #
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
        if ftype not in ("calculated",):
            fname = f["name"]
            code_lines.append(f"        self.{fname} = kwargs.get('{fname}')")
            has_non_calc = True

    if not has_non_calc:
        code_lines.append("        pass")

    # Build collection for one_to_many or many_to_many
    for lu in lookups:
        lu_type = lu.get("type")
        lu_name = lu.get("name")
        if lu_type in ("one_to_many", "many_to_many"):
            code_lines.append("")
            code_lines.append(f"        self.{lu_name} = CollectionWrapper(self, '{lu_name}')")

    # aggregator fields from "fields" with "type=calculated"
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


def main():
    parser = argparse.ArgumentParser(
        description="Generate Python classes from a JSON-based meta-model, with aggregator transformations."
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

    output_lines = []
    output_lines.append('"""')
    output_lines.append("Auto-generated Python code from your domain model.")
    output_lines.append("Now with advanced aggregator rewriting to reduce syntax errors.")
    output_lines.append('"""')
    output_lines.append("import math")
    output_lines.append("import numpy as np")

    global import_statistics
    if import_statistics:
        output_lines.append("import statistics")

    ext_imports = sorted(used_blocks.intersection(BUILDING_BLOCKS.keys()))
    if ext_imports:
        module_name = "quantum_walk_blocks"
        i_list = ", ".join(ext_imports)
        output_lines.append(f"from {module_name} import {i_list}")

    # We'll define the aggregator placeholders for _COUNT(...), _SUM(...), etc.
    aggregator_helpers = textwrap.dedent("""\
    import uuid

    # A tiny helper so we can do object.some_collection.add(item).
    class CollectionWrapper:
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


    def _auto_id():
        return str(uuid.uuid4())

    # aggregator placeholders:
    def _COUNT(expr):
        # We'll guess if there's a 'WHERE' in expr, it was already replaced. 
        # In practice we'd parse it properly, but let's fallback:
        return f\"/* _COUNT({expr}) not fully implemented */\"

    def _SUM(expr):
        return f\"/* _SUM({expr}) not fully implemented */\"

    def _AVG(expr):
        return f\"/* _AVG({expr}) not fully implemented */\"

    def _MINBY(expr):
        return f\"/* _MINBY({expr}) not fully implemented */\"

    def _MAXBY(expr):
        return f\"/* _MAXBY({expr}) not fully implemented */\"

    def _MODE(expr):
        return f\"/* _MODE({expr}) not fully implemented */\"

    def _TOPN(expr):
        return f\"/* _TOPN({expr}) not fully implemented */\"

    def _EXISTS(expr):
        return f\"/* _EXISTS({expr}) not fully implemented */\"
    """)

    output_lines.append("")
    output_lines.append(aggregator_helpers)
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
            Minimal demonstration of how to use the auto-generated classes.
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
    if ext_imports:
        print("Detected usage of building blocks:", ", ".join(ext_imports))


####################################
# The script ends here
####################################

if __name__=="__main__":
    main()
