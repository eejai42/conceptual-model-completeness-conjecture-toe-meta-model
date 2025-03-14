#!/usr/bin/env python3

import json
import argparse
import math
import re
import textwrap
import os

"""
A CLI tool that reads a "rulebook" JSON file describing an entity-based meta-model
and attempts to generate Python class stubs with valid expressions for
calculated fields (aggregators, constraints, etc.).

IMPROVED:
- We handle aggregator-like syntax such as IF( cond ) THEN ( expr ) ELSE ( expr ),
  COUNT(...), SUM(...), AVG(...), and so forth, rewriting them into Pythonic code
  to avoid raw parser errors or syntax issues.
- We create 'CollectionWrapper' for one_to_many or many_to_many lookups,
  matching your final "SDK" style.

Usage:
  python json-toemm-to-python-helper.py -i my-experiment.json -o my-exp-helper.py
"""

import_statistics = False  # We'll set True if aggregator_to_python sees "AVG(...)".


BUILDING_BLOCKS = {
    "SHIFT": "",
    "APPLY_BARRIER": "",
    "COLLAPSE_BARRIER": "",
    "GAUSSIAN_IN_Y_AND_UNIFORM_IN_X_AND_DIRECTION": "",
    "EVOLVE": "",
}

# We keep some specialized function mappings if we want them, but aggregator parsing
# is done separately below
FUNCTION_MAP = {}

POWER2_REGEX = re.compile(r"^(.*)\^2$")
FUNC_CALL_REGEX = re.compile(r"^([A-Z_]+)\((.*)\)$", re.IGNORECASE)
STRING_LITERAL_RE = re.compile(r"^(['\"])(.*)\1$")
CONDITION_RE = re.compile(r"\((.*)\)\s*THEN\s*\((.*)\)\s*ELSE\s*\((.*)\)", re.IGNORECASE)


def aggregator_to_python(expr: str) -> str:
    """
    Attempt to do minimal aggregator-based rewriting:
      - IF (cond) THEN (val) ELSE (val) => (val if cond else val)
      - COUNT(...), SUM(...), AVG(...), MINBY(...), MAXBY(...), TOPN(...)
      - Replace '=' with '==' in many contexts, AND->'and', OR->'or', etc.
      - "->" => "."
      - "someCollection WHERE ..." => comprehension if we see COUNT, SUM, etc.
      - attempt to produce valid Python code
    """
    global import_statistics
    e = expr

    # 1) rewrite "IF (cond) THEN (a) ELSE (b)"
    if re.search(r"\bIF\s*\(.*\)\s*THEN\s*\(.*\)\s*ELSE\s*\(.*\)", e, re.IGNORECASE):
        match = re.search(CONDITION_RE, e)
        if match:
            cond_str = match.group(1).strip()
            then_str = match.group(2).strip()
            else_str = match.group(3).strip()
            cond_py = aggregator_to_python(cond_str)
            then_py = aggregator_to_python(then_str)
            else_py = aggregator_to_python(else_str)
            e = f"(({then_py}) if ({cond_py}) else ({else_py}))"

    # 2) Common aggregator patterns:
    #    COUNT(...), SUM(...), AVG(...), MINBY, MAXBY, TOPN, MODE, EXISTS, etc.
    # We'll do them with re.sub so we can handle partial syntax

    # Regex for COUNT( ... )
    def handle_count(m):
        inside = m.group(1).strip()
        # check if there's "WHERE"
        if "WHERE" in inside.upper():
            # e.g. "AtBat WHERE batterId=this.id"
            parts = re.split(r"(?i)\bwhere\b", inside, 1)
            coll = parts[0].strip()
            cond = parts[1].strip()
            cond_py = aggregator_to_python(cond)
            coll_py = aggregator_to_python(coll)
            if "." not in coll_py:
                coll_py = f"self.{coll_py}"
            return f"sum(1 for x in {coll_py} if {cond_py})"
        else:
            # just COUNT(AtBat) => len(self.AtBat)
            coll_py = aggregator_to_python(inside)
            if "." not in coll_py:
                coll_py = f"self.{coll_py}"
            return f"len({coll_py})"

    e = re.sub(r"\bCOUNT\s*\(\s*(.*?)\s*\)", handle_count, e, flags=re.IGNORECASE)

    # SUM(...)
    def handle_sum(m):
        inside = m.group(1).strip()
        # "roster => careerHomeRuns" or "roster WHERE cond => field"
        field = None
        cond = None
        coll = inside
        if "=>" in inside:
            before, field = inside.split("=>",1)
            field = field.strip()
            if "WHERE" in before.upper():
                bits = re.split(r"(?i)where", before, 1)
                coll = bits[0].strip()
                cond = bits[1].strip()
            else:
                coll = before.strip()
        coll_py = aggregator_to_python(coll)
        if "." not in coll_py:
            coll_py = f"self.{coll_py}"
        field_py = aggregator_to_python(field) if field else "x"
        cond_py = aggregator_to_python(cond) if cond else None
        if cond_py:
            return f"sum(x.{field_py} for x in {coll_py} if {cond_py})"
        else:
            return f"sum(x.{field_py} for x in {coll_py})"

    e = re.sub(r"\bSUM\s*\(\s*(.*?)\s*\)", handle_sum, e, flags=re.IGNORECASE)

    # AVG(...)
    def handle_avg(m):
        global import_statistics
        import_statistics = True
        inside = m.group(1).strip()
        field = None
        cond = None
        coll = inside
        if "=>" in inside:
            before, field = inside.split("=>",1)
            field = field.strip()
            if "WHERE" in before.upper():
                bits = re.split(r"(?i)where", before, 1)
                coll = bits[0].strip()
                cond = bits[1].strip()
            else:
                coll = before.strip()
        coll_py = aggregator_to_python(coll)
        if "." not in coll_py:
            coll_py = f"self.{coll_py}"
        field_py = aggregator_to_python(field) if field else "x"
        cond_py = aggregator_to_python(cond) if cond else None
        if cond_py:
            return f"statistics.mean(x.{field_py} for x in {coll_py} if {cond_py})"
        else:
            return f"statistics.mean(x.{field_py} for x in {coll_py})"

    e = re.sub(r"\bAVG\s*\(\s*(.*?)\s*\)", handle_avg, e, flags=re.IGNORECASE)

    # MINBY(...) / MAXBY(...)
    def handle_minmaxby(m):
        func = m.group(1).upper()  # MINBY or MAXBY
        inside = m.group(2).strip()
        # e.g. "roster where playerIsPitcher=true, p => p.careerERA"
        cond = None
        coll = None
        key_expr = None
        if "," in inside:
            left, right = inside.split(",",1)
            left = left.strip()
            right = right.strip()
            # right might be "p => p.careerERA"
            if "=>" in right:
                after_arrow = right.split("=>",1)[1].strip()
                key_expr = aggregator_to_python(after_arrow)
            # left might have "where"
            if "WHERE" in left.upper():
                bits = re.split(r"(?i)where", left, 1)
                coll = bits[0].strip()
                cond = bits[1].strip()
            else:
                coll = left
        else:
            coll = inside
        coll_py = aggregator_to_python(coll) or "self.someList"
        if "." not in coll_py:
            coll_py = f"self.{coll_py}"
        cond_py = aggregator_to_python(cond) if cond else None
        if not key_expr:
            key_expr = "x"

        if func == "MINBY":
            if cond_py:
                return f"min((x for x in {coll_py} if {cond_py}), key=lambda x: {key_expr})"
            else:
                return f"min({coll_py}, key=lambda x: {key_expr})"
        else:
            # MAXBY
            if cond_py:
                return f"max((x for x in {coll_py} if {cond_py}), key=lambda x: {key_expr})"
            else:
                return f"max({coll_py}, key=lambda x: {key_expr})"

    e = re.sub(r"\b(MINBY|MAXBY)\s*\(\s*(.*?)\s*\)", handle_minmaxby, e, flags=re.IGNORECASE)

    # MODE(...) => statistics.multimode(...)
    def handle_mode(m):
        global import_statistics
        import_statistics = True
        inside = m.group(1).strip()
        inside_py = aggregator_to_python(inside)
        if "." not in inside_py:
            inside_py = f"self.{inside_py}"
        return f"statistics.multimode({inside_py})"

    e = re.sub(r"\bMODE\s*\(\s*(.*?)\)", handle_mode, e, flags=re.IGNORECASE)

    # TOPN( 3, coll, p => p.ops )
    def handle_topn(m):
        # fix the group indexing => group(1)
        inside = m.group(1).strip()
        # e.g. "3, teams.roster, p => p.ops"
        bits = [x.strip() for x in inside.split(",",2)]
        if len(bits) < 3:
            return "# Could not parse TOPN properly"
        n_str, coll_str, key_str = bits
        coll_py = aggregator_to_python(coll_str)
        if "." not in coll_py:
            coll_py = f"self.{coll_py}"
        # parse "p => p.ops"
        if "=>" in key_str:
            after = key_str.split("=>",1)[1].strip()
            keyfield = aggregator_to_python(after)
        else:
            keyfield = "x"

        return f"sorted({coll_py}, key=lambda x: {keyfield})[:{n_str}]"

    e = re.sub(r"\bTOPN\s*\(\s*(.*?)\)", handle_topn, e, flags=re.IGNORECASE)

    # EXISTS(...)
    def handle_exists(m):
        inside = m.group(1).strip()
        # "Game WHERE something"
        if "WHERE" in inside.upper():
            bits = re.split(r"(?i)where", inside, 1)
            coll = bits[0].strip()
            cond = bits[1].strip()
            coll_py = aggregator_to_python(coll)
            if "." not in coll_py:
                coll_py = f"self.{coll_py}"
            cond_py = aggregator_to_python(cond)
            return f"any(x for x in {coll_py} if {cond_py})"
        else:
            # just "Game"
            coll_py = aggregator_to_python(inside)
            if "." not in coll_py:
                coll_py = f"self.{coll_py}"
            return f"len({coll_py}) > 0"

    e = re.sub(r"\bEXISTS\s*\(\s*(.*?)\)", handle_exists, e, flags=re.IGNORECASE)

    # Replace "->" with "."
    e = e.replace("->", ".")

    # Replace "AND" => "and", "OR" => "or", single "=", etc.
    # We'll do a simpler pass of re/ or .replace
    def replacer_basic(s):
        s = re.sub(r"\bAND\b", " and ", s, flags=re.IGNORECASE)
        s = re.sub(r"\bOR\b", " or ", s, flags=re.IGNORECASE)
        # '=' with strings can be replaced with '==' but we must skip '==' that is already correct
        # We'll do a naive approach: only if it's something like "==?" do we skip
        # Actually we did some partial steps earlier. We'll do a final pass to fix "X = Y" => "X == Y"
        # ignoring "==" or ">=" or "<=" etc. We'll do a small custom re for that:
        s = re.sub(r"(?<![=!<>])=+(?![=])", "==", s)
        # Replace '==true' => '== True'
        # Replace '==false' => '== False'
        s = re.sub(r"==\s*true\b", "== True", s, flags=re.IGNORECASE)
        s = re.sub(r"==\s*false\b", "== False", s, flags=re.IGNORECASE)
        s = re.sub(r"==\s*null\b", "is None", s, flags=re.IGNORECASE)
        return s

    e = replacer_basic(e)

    return e.strip()


def parse_formula(expr, used_blocks_set):
    # We feed the entire aggregator logic to aggregator_to_python
    expr_py = aggregator_to_python(expr)
    # check SHIFT, EVOLVE, etc.
    if "SHIFT(" in expr_py:
        used_blocks_set.add("SHIFT")
    if "EVOLVE(" in expr_py:
        used_blocks_set.add("EVOLVE")
    return expr_py


def transform_formula(formula_str, used_blocks_set):
    if not formula_str:
        return "None"
    return parse_formula(formula_str, used_blocks_set)


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
    output_lines.append("Now includes aggregator rewriting and CollectionWrapper for relationships.")
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

    helper_code = textwrap.dedent("""\
    import uuid

    # A tiny helper so we can do object.some_collection.add(item).
    # We'll keep this for convenience. It's purely data structure code—no domain logic here.
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
        \"\"\"Simple helper to generate an ID if none is provided.\"\"\"
        return str(uuid.uuid4())
    """)
    output_lines.append("")
    output_lines.append(helper_code)
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


if __name__=="__main__":
    main()
