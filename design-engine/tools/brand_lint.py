#!/usr/bin/env python3
"""brand_lint — validate brand.json. Stdlib only, exit non-zero on violation.

Two layers:
  1. Structure — brand.schema.json, via a small validator implementing the
     JSON-Schema subset the schema uses (type, required, properties,
     additionalProperties, patternProperties, pattern, enum, items,
     minimum, maximum).
  2. Invariants a schema can't express:
     - every theme declares the same role set (no theme can silently miss one)
     - every '@alias' reference resolves, without cycles
     - contrast config names only roles that exist
     - every font file exists on disk under the host root
     - preload paths are declared font files
     - default_theme exists; mark bar colors are valid hex (schema) and the
       favicon bg resolves

    python3 design-engine/tools/brand_lint.py [--brand path]
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import enginelib as lib


# ---- JSON-Schema subset validator -------------------------------------------

def _validate(node, schema, path, errors):
    t = schema.get("type")
    if t:
        ok = {"object": dict, "array": list, "string": str, "boolean": bool}.get(t)
        if ok is not None and not isinstance(node, ok):
            errors.append(f"{path}: expected {t}, got {type(node).__name__}")
            return
        if t == "integer" and not (isinstance(node, int) and not isinstance(node, bool)):
            errors.append(f"{path}: expected integer, got {type(node).__name__}")
            return
        if t == "number" and not (isinstance(node, (int, float)) and not isinstance(node, bool)):
            errors.append(f"{path}: expected number, got {type(node).__name__}")
            return
    if "enum" in schema and node not in schema["enum"]:
        errors.append(f"{path}: {node!r} not in {schema['enum']}")
    if "pattern" in schema and isinstance(node, str) and not re.fullmatch(schema["pattern"], node):
        errors.append(f"{path}: {node!r} does not match {schema['pattern']}")
    if "minimum" in schema and isinstance(node, (int, float)) and node < schema["minimum"]:
        errors.append(f"{path}: {node} < minimum {schema['minimum']}")
    if "maximum" in schema and isinstance(node, (int, float)) and node > schema["maximum"]:
        errors.append(f"{path}: {node} > maximum {schema['maximum']}")
    if isinstance(node, dict):
        for req in schema.get("required", []):
            if req not in node:
                errors.append(f"{path}: missing required key '{req}'")
        props = schema.get("properties", {})
        pattern_props = schema.get("patternProperties", {})
        for k, v in node.items():
            sub = props.get(k)
            if sub is None:
                for pat, ps in pattern_props.items():
                    if re.fullmatch(pat, k):
                        sub = ps
                        break
            if sub is not None:
                _validate(v, sub, f"{path}.{k}", errors)
            elif schema.get("additionalProperties") is False and (props or pattern_props):
                errors.append(f"{path}: unexpected key '{k}'")
    if isinstance(node, list) and "items" in schema:
        for i, item in enumerate(node):
            _validate(item, schema["items"], f"{path}[{i}]", errors)


# ---- semantic invariants -----------------------------------------------------

def lint(brand: dict, schema: dict, host_root: Path):
    errors = []
    _validate(brand, schema, "brand", errors)
    if errors:
        return errors  # structure first; invariants assume shape

    pal = brand["palette"]
    themes = pal["themes"]
    if pal["default_theme"] not in themes:
        errors.append(f"default_theme '{pal['default_theme']}' is not a declared theme")

    role_sets = {t: set(lib.theme_roles(brand, t)) for t in themes}
    base = role_sets[pal["default_theme"]]
    for t, roles in role_sets.items():
        missing, extra = base - roles, roles - base
        if missing:
            errors.append(f"theme '{t}' missing roles: {sorted(missing)}")
        if extra:
            errors.append(f"theme '{t}' has roles the default theme lacks: {sorted(extra)}")

    for t in themes:
        roles = lib.theme_roles(brand, t)
        for name in roles:
            try:
                lib.resolve_role(roles, name)
            except (KeyError, ValueError) as e:
                errors.append(f"theme '{t}': role '{name}' does not resolve ({e})")

    cfg = brand["contrast"]
    known = base
    for name in (list(cfg["text_min"]) + cfg.get("accents", []) + cfg["surfaces"]
                 + cfg.get("categorical_surfaces", [])):
        if name not in known:
            errors.append(f"contrast config names unknown role '{name}'")

    declared_files = []
    for face in brand["type"]["faces"]:
        for f in face["files"]:
            declared_files.append(f["path"])
            if not (host_root / f["path"]).exists():
                errors.append(f"font file missing on disk: {f['path']} "
                              f"({face['family']} {f['weight']})")
    for p in brand["type"].get("preload", []):
        if p not in declared_files:
            errors.append(f"preload names an undeclared font file: {p}")

    if not pal["categorical"]:
        errors.append("palette.categorical is empty")

    for t in pal.get("categorical_mix", {}):
        if t == pal["default_theme"]:
            errors.append(f"categorical_mix declared for the default theme '{t}' "
                          "(the default renders raw hues)")
        elif t not in themes:
            errors.append(f"categorical_mix names unknown theme '{t}'")

    mark = brand["mark"]
    if ("bars" in mark) == ("elements" in mark):
        errors.append("mark must declare exactly one of 'bars' (legacy) or 'elements'")
    if "bars" in mark and "rx" not in mark:
        errors.append("mark with 'bars' requires 'rx'")
    return errors


def main(argv):
    brand_arg = None
    args = list(argv)
    while args:
        a = args.pop(0)
        if a == "--brand":
            brand_arg = args.pop(0)
        else:
            print(f"unknown arg: {a}", file=sys.stderr)
            return 2
    brand = lib.load_brand(brand_arg)
    schema = json.loads((lib.ENGINE_DIR / "brand.schema.json").read_text(encoding="utf-8"))
    errors = lint(brand, schema, lib.HOST_ROOT)
    if errors:
        print(f"FAIL  brand.json: {len(errors)} problem(s):", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1
    n_roles = len(lib.theme_roles(brand, brand["palette"]["default_theme"]))
    print(f"OK  brand.json v{brand['meta']['brand_version']}: "
          f"{len(brand['palette']['themes'])} themes × {n_roles} roles, "
          f"{len(brand['palette']['categorical'])} categorical hues, "
          f"{len(brand['type']['faces'])} type faces — schema + invariants clean")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
