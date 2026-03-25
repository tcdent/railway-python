#!/usr/bin/env python3
"""
Code generator that reads the Railway GraphQL introspection schema
and produces fully-typed Python dataclasses + a thin client wrapper.
"""

from __future__ import annotations

import json
import keyword
import re
import sys
import textwrap
from pathlib import Path
from typing import Any

# ── helpers ──────────────────────────────────────────────────────────

SCALAR_MAP: dict[str, str] = {
    "String": "str",
    "Int": "int",
    "Float": "float",
    "Boolean": "bool",
    "ID": "str",
    "DateTime": "str",
    "JSON": "Any",
    "Date": "str",
    "Upload": "Any",
    "BigInt": "int",
    "Void": "None",
    "CanvasConfig": "Any",
    "ServiceVariables": "Any",
    "SubscriptionPlanLimit": "Any",
    "EnvironmentVariables": "Any",
    "HelpStationFormFields": "Any",
}


def snake(name: str) -> str:
    """camelCase / PascalCase → snake_case"""
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    s = s.lower()
    if keyword.iskeyword(s) or s in ("id", "type", "from", "input"):
        pass  # keep as-is; we'll handle at call-sites
    return s


def safe_name(name: str) -> str:
    s = snake(name)
    if keyword.iskeyword(s) or s == "from":
        return s + "_"
    return s


def resolve_type(t: dict, nullable: bool = True) -> tuple[str, bool]:
    """Return (python_type_str, is_nullable)."""
    kind = t["kind"]
    if kind == "NON_NULL":
        inner, _ = resolve_type(t["ofType"], nullable=False)
        return inner, False
    if kind == "LIST":
        inner, _ = resolve_type(t["ofType"])
        return f"list[{inner}]", nullable
    name = t["name"]
    if name in SCALAR_MAP:
        py = SCALAR_MAP[name]
    else:
        py = f'"{name}"'
    return py, nullable


# ── schema loading ───────────────────────────────────────────────────

def load_schema(path: str) -> dict:
    with open(path) as f:
        data = json.load(f)
    if "data" in data:
        return data["data"]["__schema"]
    return data["__schema"] if "__schema" in data else data


# ── generators ───────────────────────────────────────────────────────

def gen_enums(types: list[dict]) -> str:
    lines = [
        "from __future__ import annotations",
        "",
        "from enum import Enum",
        "",
    ]
    enums = sorted(
        [t for t in types if t["kind"] == "ENUM" and not t["name"].startswith("__")],
        key=lambda t: t["name"],
    )
    for t in enums:
        lines.append(f"class {t['name']}(str, Enum):")
        if t.get("description"):
            lines.append(f'    """{t["description"]}"""')
        for v in t["enumValues"]:
            lines.append(f'    {v["name"]} = "{v["name"]}"')
        lines.append("")
        lines.append("")
    return "\n".join(lines)


def gen_input_types(types: list[dict]) -> str:
    lines = [
        "from __future__ import annotations",
        "",
        "from dataclasses import dataclass, field",
        "from typing import Any, Optional",
        "",
        "from .enums import *  # noqa: F401,F403",
        "",
    ]
    inputs = sorted(
        [t for t in types if t["kind"] == "INPUT_OBJECT" and not t["name"].startswith("__")],
        key=lambda t: t["name"],
    )
    for t in inputs:
        lines.append("@dataclass")
        lines.append(f"class {t['name']}:")
        if t.get("description"):
            lines.append(f'    """{t["description"]}"""')
        required_fields = []
        optional_fields = []
        for f in t.get("inputFields") or []:
            py_type, nullable = resolve_type(f["type"])
            fname = safe_name(f["name"])
            if nullable:
                optional_fields.append((fname, f["name"], py_type, f.get("description")))
            else:
                required_fields.append((fname, f["name"], py_type, f.get("description")))
        if not required_fields and not optional_fields:
            lines.append("    pass")
        for fname, orig, py_type, desc in required_fields:
            lines.append(f"    {fname}: {py_type}")
        for fname, orig, py_type, desc in optional_fields:
            lines.append(f"    {fname}: Optional[{py_type}] = None")
        lines.append("")
        lines.append("")
    return "\n".join(lines)


def gen_object_types(types: list[dict]) -> str:
    lines = [
        "from __future__ import annotations",
        "",
        "from dataclasses import dataclass, field",
        "from typing import Any, Optional",
        "",
        "from .enums import *  # noqa: F401,F403",
        "",
    ]
    objects = sorted(
        [
            t
            for t in types
            if t["kind"] == "OBJECT"
            and not t["name"].startswith("__")
            and t["name"] not in ("Query", "Mutation", "Subscription")
        ],
        key=lambda t: t["name"],
    )
    for t in objects:
        lines.append("@dataclass")
        lines.append(f"class {t['name']}:")
        if t.get("description"):
            lines.append(f'    """{t["description"]}"""')
        fields = t.get("fields") or []
        if not fields:
            lines.append("    pass")
            lines.append("")
            lines.append("")
            continue
        required_fields = []
        optional_fields = []
        for f in fields:
            if f.get("args"):
                # Skip fields that require arguments (sub-queries / connections with args)
                # We'll treat these as optional
                py_type, _ = resolve_type(f["type"])
                optional_fields.append((safe_name(f["name"]), f["name"], py_type, f.get("description")))
                continue
            py_type, nullable = resolve_type(f["type"])
            fname = safe_name(f["name"])
            if nullable:
                optional_fields.append((fname, f["name"], py_type, f.get("description")))
            else:
                required_fields.append((fname, f["name"], py_type, f.get("description")))
        for fname, orig, py_type, desc in required_fields:
            lines.append(f"    {fname}: {py_type}")
        for fname, orig, py_type, desc in optional_fields:
            lines.append(f"    {fname}: Optional[{py_type}] = None")
        lines.append("")
        lines.append("")
    return "\n".join(lines)


def _build_default_fields(types_by_name: dict, type_ref: dict, depth: int = 0, visited: set | None = None) -> str:
    """Build a default selection set string for a given return type (for generating queries)."""
    if visited is None:
        visited = set()

    kind = type_ref["kind"]
    if kind == "NON_NULL" or kind == "LIST":
        return _build_default_fields(types_by_name, type_ref["ofType"], depth, visited)

    name = type_ref["name"]
    if name in SCALAR_MAP:
        return ""  # scalar field - selected by name at parent level

    t = types_by_name.get(name)
    if not t or t["kind"] == "UNION" or t["kind"] == "INTERFACE":
        return ""

    if name in visited or depth > 1:
        return ""
    visited = visited | {name}

    fields = t.get("fields") or []
    scalar_fields = []
    nested_fields = []
    for f in fields:
        if f.get("args"):
            continue
        ftype = f["type"]
        # Unwrap NON_NULL / LIST
        inner = ftype
        while inner["kind"] in ("NON_NULL", "LIST"):
            inner = inner["ofType"]
        if inner["name"] in SCALAR_MAP:
            scalar_fields.append(f["name"])
        elif depth < 1:
            sub = _build_default_fields(types_by_name, ftype, depth + 1, visited)
            if sub:
                nested_fields.append(f'{f["name"]} {{ {sub} }}')

    all_fields = scalar_fields + nested_fields
    return " ".join(all_fields)


def gen_client(types: list[dict], schema: dict) -> str:
    types_by_name = {t["name"]: t for t in types}
    query_type = types_by_name.get("Query")
    mutation_type = types_by_name.get("Mutation")

    lines = [
        "from __future__ import annotations",
        "",
        "import json",
        "from dataclasses import asdict, dataclass",
        "from typing import Any, Optional, overload",
        "",
        "import httpx",
        "",
        "from .enums import *  # noqa: F401,F403",
        "from .inputs import *  # noqa: F401,F403",
        "from .types import *  # noqa: F401,F403",
        "",
        "",
        "def _clean_input(obj: Any) -> Any:",
        '    """Recursively convert dataclasses to dicts and strip None values."""',
        "    if hasattr(obj, '__dataclass_fields__'):",
        "        return {k: _clean_input(v) for k, v in asdict(obj).items() if v is not None}",
        "    if isinstance(obj, dict):",
        "        return {k: _clean_input(v) for k, v in obj.items() if v is not None}",
        "    if isinstance(obj, list):",
        "        return [_clean_input(v) for v in obj]",
        "    if isinstance(obj, Enum):",
        "        return obj.value",
        "    return obj",
        "",
        "",
        "class RailwayError(Exception):",
        '    """Raised when the Railway GraphQL API returns errors."""',
        "",
        "    def __init__(self, errors: list[dict], data: Any = None):",
        "        self.errors = errors",
        "        self.data = data",
        '        messages = "; ".join(e.get("message", str(e)) for e in errors)',
        "        super().__init__(messages)",
        "",
        "",
        "class RailwayClient:",
        '    """Typed Python client for the Railway GraphQL API (v2)."""',
        "",
        "    ENDPOINT = \"https://backboard.railway.com/graphql/v2\"",
        "",
        "    def __init__(",
        "        self,",
        "        token: str,",
        "        *,",
        "        endpoint: str | None = None,",
        "        timeout: float = 30.0,",
        "        is_project_token: bool = False,",
        "    ):",
        '        """',
        "        Create a new Railway API client.",
        "",
        "        Args:",
        "            token: Railway API token (account, workspace, or project token).",
        "            endpoint: Override the default API endpoint.",
        "            timeout: Request timeout in seconds.",
        "            is_project_token: Set True when using a project-scoped token.",
        '        """',
        "        self._endpoint = endpoint or self.ENDPOINT",
        "        self._timeout = timeout",
        "        if is_project_token:",
        '            self._headers = {"Content-Type": "application/json", "Project-Access-Token": token}',
        "        else:",
        '            self._headers = {"Content-Type": "application/json", "Authorization": f"Bearer {token}"}',
        "        self._client = httpx.Client(timeout=timeout)",
        "",
        "    def close(self) -> None:",
        '        """Close the underlying HTTP client."""',
        "        self._client.close()",
        "",
        "    def __enter__(self) -> RailwayClient:",
        "        return self",
        "",
        "    def __exit__(self, *args: Any) -> None:",
        "        self.close()",
        "",
        "    def _execute(self, query: str, variables: dict[str, Any] | None = None) -> Any:",
        '        """Execute a raw GraphQL query and return the data dict."""',
        "        payload: dict[str, Any] = {\"query\": query}",
        "        if variables:",
        '            payload["variables"] = variables',
        "        resp = self._client.post(self._endpoint, headers=self._headers, json=payload)",
        "        resp.raise_for_status()",
        "        body = resp.json()",
        '        if "errors" in body:',
        '            raise RailwayError(body["errors"], body.get("data"))',
        '        return body.get("data")',
        "",
    ]

    # Generate query methods
    if query_type:
        lines.append("    # ── Queries ────────────────────────────────────────────")
        lines.append("")
        for f in sorted(query_type["fields"], key=lambda x: x["name"]):
            _gen_method(lines, f, "query", types_by_name)

    # Generate mutation methods
    if mutation_type:
        lines.append("    # ── Mutations ──────────────────────────────────────────")
        lines.append("")
        for f in sorted(mutation_type["fields"], key=lambda x: x["name"]):
            _gen_method(lines, f, "mutation", types_by_name)

    return "\n".join(lines)


def _gen_method(lines: list[str], f: dict, op_type: str, types_by_name: dict) -> None:
    name = f["name"]
    method_name = safe_name(name)
    args = f.get("args") or []
    ret_type, ret_nullable = resolve_type(f["type"])

    # Build default field selection for the return type
    selection = _build_default_fields(types_by_name, f["type"])

    # Build method signature
    params = ["self"]
    param_docs = []
    required_args = []
    optional_args = []
    for a in args:
        aname = safe_name(a["name"])
        atype, anullable = resolve_type(a["type"])
        if anullable:
            optional_args.append((aname, a["name"], atype, a.get("description")))
        else:
            required_args.append((aname, a["name"], atype, a.get("description")))

    for aname, orig, atype, desc in required_args:
        params.append(f"{aname}: {atype}")
    if optional_args:
        params.append("*")
        for aname, orig, atype, desc in optional_args:
            params.append(f"{aname}: Optional[{atype}] = None")

    sig = ", ".join(params)
    if ret_nullable:
        ret_annotation = f"Optional[{ret_type}]"
    else:
        ret_annotation = ret_type

    lines.append(f"    def {method_name}({sig}) -> {ret_annotation}:")

    # Build GraphQL query string
    gql_args_def = []
    gql_args_pass = []
    for a in args:
        atype_gql = _gql_type_str(a["type"])
        gql_args_def.append(f"${a['name']}: {atype_gql}")
        gql_args_pass.append(f"{a['name']}: ${a['name']}")

    if gql_args_def:
        args_def_str = "(" + ", ".join(gql_args_def) + ")"
        args_pass_str = "(" + ", ".join(gql_args_pass) + ")"
    else:
        args_def_str = ""
        args_pass_str = ""

    if selection:
        field_str = f"{name}{args_pass_str} {{ {selection} }}"
    else:
        field_str = f"{name}{args_pass_str}"

    gql = f"{op_type}{args_def_str} {{ {field_str} }}"

    # Build variables dict
    lines.append(f'        query = """{gql}"""')

    var_entries = []
    for a in args:
        aname = safe_name(a["name"])
        var_entries.append(f'"{a["name"]}": _clean_input({aname})')

    if var_entries:
        lines.append("        variables: dict[str, Any] = {")
        for v in var_entries:
            lines.append(f"            {v},")
        lines.append("        }")
        lines.append("        variables = {k: v for k, v in variables.items() if v is not None}")
        lines.append(f'        return self._execute(query, variables).get("{name}")')
    else:
        lines.append(f'        return self._execute(query).get("{name}")')

    lines.append("")


def _gql_type_str(t: dict) -> str:
    """Convert type ref back to GraphQL type notation."""
    kind = t["kind"]
    if kind == "NON_NULL":
        return _gql_type_str(t["ofType"]) + "!"
    if kind == "LIST":
        return "[" + _gql_type_str(t["ofType"]) + "]"
    return t["name"]


# ── main ─────────────────────────────────────────────────────────────

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: generate.py <introspection.json>")
        sys.exit(1)

    schema = load_schema(sys.argv[1])
    types = schema["types"]

    out = Path(__file__).resolve().parent.parent / "railway"

    (out / "enums.py").write_text(gen_enums(types))
    print("✓ enums.py")

    (out / "inputs.py").write_text(gen_input_types(types))
    print("✓ inputs.py")

    (out / "types.py").write_text(gen_object_types(types))
    print("✓ types.py")

    (out / "client.py").write_text(gen_client(types, schema))
    print("✓ client.py")

    print("Done – generated Railway SDK.")


if __name__ == "__main__":
    main()
