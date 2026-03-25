#!/usr/bin/env python3
"""
Code generator that reads the Railway GraphQL introspection schema
and produces fully-typed Pydantic models + a thin client wrapper.
"""

from __future__ import annotations

import json
import keyword
import re
import sys
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
    "Date": "str",
    "JSON": "Any",
    "Upload": "Any",
    "BigInt": "int",
    "Void": "None",
    # Custom Railway scalars — all opaque JSON values
    "CanvasConfig": "Any",
    "DeploymentDiagnosis": "Any",
    "DeploymentMeta": "Any",
    "DisplayConfig": "Any",
    "EnvironmentConfig": "Any",
    "EnvironmentVariables": "Any",
    "HelpStationFormFields": "Any",
    "NotificationChannelConfig": "Any",
    "NotificationPayload": "Any",
    "RailpackInfo": "Any",
    "SerializedTemplateConfig": "Any",
    "ServiceInstanceLimit": "Any",
    "ServiceVariables": "Any",
    "SkippedResourceIds": "Any",
    "SpendCommitmentFeatureId": "Any",
    "SubscriptionPlanLimit": "Any",
    "SupportHealthMetrics": "Any",
    "TemplateConfig": "Any",
    "TemplateMetadata": "Any",
    "TemplateServiceConfig": "Any",
    "TemplateVolume": "Any",
}


def snake(name: str) -> str:
    """camelCase / PascalCase → snake_case"""
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    return s.lower()


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
        "from typing import Any, Optional",
        "",
        "from pydantic import BaseModel, ConfigDict",
        "from pydantic.alias_generators import to_camel",
        "",
        "from .enums import *  # noqa: F401,F403",
        "",
        "",
        "class _Base(BaseModel):",
        "    model_config = ConfigDict(",
        "        alias_generator=to_camel,",
        "        populate_by_name=True,",
        "    )",
        "",
        "",
    ]
    inputs = sorted(
        [t for t in types if t["kind"] == "INPUT_OBJECT" and not t["name"].startswith("__")],
        key=lambda t: t["name"],
    )
    class_names = []
    for t in inputs:
        class_names.append(t["name"])
        lines.append(f"class {t['name']}(_Base):")
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

    return "\n".join(lines), class_names


def gen_object_types(types: list[dict]) -> str:
    lines = [
        "from __future__ import annotations",
        "",
        "from typing import Any, Optional",
        "",
        "from pydantic import BaseModel, ConfigDict",
        "from pydantic.alias_generators import to_camel",
        "",
        "from .enums import *  # noqa: F401,F403",
        "",
        "",
        "class _Base(BaseModel):",
        "    model_config = ConfigDict(",
        "        alias_generator=to_camel,",
        "        populate_by_name=True,",
        "    )",
        "",
        "",
    ]
    # Generate type aliases for unions and interfaces (resolved as Any)
    unions_interfaces = sorted(
        [t for t in types if t["kind"] in ("UNION", "INTERFACE") and not t["name"].startswith("__")],
        key=lambda t: t["name"],
    )
    for t in unions_interfaces:
        possible = t.get("possibleTypes") or []
        if possible:
            type_names = ", ".join(f'"{p["name"]}"' for p in possible)
            lines.append(f"# {t['kind']}: {t['name']} = {type_names}")
        lines.append(f"{t['name']} = Any")
        lines.append("")

    if unions_interfaces:
        lines.append("")

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
    class_names = []
    for t in objects:
        class_names.append(t["name"])
        lines.append(f"class {t['name']}(_Base):")
        if t.get("description"):
            lines.append(f'    """{t["description"]}"""')
        fields = t.get("fields") or []
        if not fields:
            lines.append("    pass")
            lines.append("")
            lines.append("")
            continue
        # All response fields are Optional — GraphQL only returns selected fields
        all_fields = []
        for f in fields:
            py_type, _ = resolve_type(f["type"])
            fname = safe_name(f["name"])
            all_fields.append((fname, py_type))
        if not all_fields:
            lines.append("    pass")
        for fname, py_type in all_fields:
            lines.append(f"    {fname}: Optional[{py_type}] = None")
        lines.append("")
        lines.append("")

    return "\n".join(lines), class_names


def _build_default_fields(types_by_name: dict, type_ref: dict, depth: int = 0, visited: set | None = None) -> str:
    """Build a default selection set string for a given return type (for generating queries)."""
    if visited is None:
        visited = set()

    kind = type_ref["kind"]
    if kind == "NON_NULL" or kind == "LIST":
        return _build_default_fields(types_by_name, type_ref["ofType"], depth, visited)

    name = type_ref["name"]
    if name in SCALAR_MAP:
        return ""

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


def _unwrap_type_name(type_ref: dict) -> str | None:
    """Unwrap NON_NULL/LIST wrappers to get the base type name."""
    while type_ref["kind"] in ("NON_NULL", "LIST"):
        type_ref = type_ref["ofType"]
    return type_ref.get("name")


def _is_scalar_return(type_ref: dict) -> bool:
    """Check if the return type is a scalar (not a model)."""
    name = _unwrap_type_name(type_ref)
    return name in SCALAR_MAP if name else True


def _is_list_return(type_ref: dict) -> bool:
    """Check if the return type is a list (unwrapping NON_NULL)."""
    kind = type_ref["kind"]
    if kind == "NON_NULL":
        return _is_list_return(type_ref["ofType"])
    return kind == "LIST"


def gen_client(types: list[dict], schema: dict) -> str:
    types_by_name = {t["name"]: t for t in types}
    query_type = types_by_name.get("Query")
    mutation_type = types_by_name.get("Mutation")

    lines = [
        "from __future__ import annotations",
        "",
        "from typing import Any, Optional",
        "",
        "import httpx",
        "from pydantic import BaseModel, TypeAdapter",
        "",
        "from .enums import *  # noqa: F401,F403",
        "from .inputs import *  # noqa: F401,F403",
        "from .types import *  # noqa: F401,F403",
        "",
        "",
        "def _prepare_input(obj: Any) -> Any:",
        '    """Recursively serialize inputs for GraphQL variables."""',
        "    if isinstance(obj, BaseModel):",
        "        return obj.model_dump(by_alias=True, exclude_none=True)",
        "    if isinstance(obj, dict):",
        "        return {k: _prepare_input(v) for k, v in obj.items() if v is not None}",
        "    if isinstance(obj, list):",
        "        return [_prepare_input(v) for v in obj]",
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
        '    ENDPOINT = "https://backboard.railway.com/graphql/v2"',
        "",
        "    def __init__(",
        "        self,",
        "        *,",
        "        api_token: str | None = None,",
        "        project_token: str | None = None,",
        "        endpoint: str | None = None,",
        "        timeout: float = 30.0,",
        "    ):",
        '        """',
        "        Create a new Railway API client.",
        "",
        "        Provide exactly one of api_token or project_token.",
        "",
        "        Args:",
        "            api_token: Railway API token (account or workspace scope).",
        "            project_token: Railway project-scoped token.",
        "            endpoint: Override the default API endpoint.",
        "            timeout: Request timeout in seconds.",
        '        """',
        "        if api_token and project_token:",
        '            raise ValueError("Provide exactly one of api_token or project_token, not both.")',
        "        if not api_token and not project_token:",
        '            raise ValueError("Provide either api_token or project_token.")',
        "        self._endpoint = endpoint or self.ENDPOINT",
        "        self._timeout = timeout",
        "        if project_token:",
        '            self._headers = {"Content-Type": "application/json", "Project-Access-Token": project_token}',
        "        else:",
        '            self._headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_token}"}',
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
        '        payload: dict[str, Any] = {"query": query}',
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


def _is_input_object(type_ref: dict, types_by_name: dict) -> str | None:
    """If type_ref resolves to an INPUT_OBJECT, return its name; else None."""
    name = _unwrap_type_name(type_ref)
    if name and name in types_by_name and types_by_name[name]["kind"] == "INPUT_OBJECT":
        return name
    return None


def _gen_method(lines: list[str], f: dict, op_type: str, types_by_name: dict) -> None:
    name = f["name"]  # original camelCase GraphQL name
    method_name = safe_name(name)
    args = f.get("args") or []
    ret_type, ret_nullable = resolve_type(f["type"])

    # Build default field selection for the return type
    selection = _build_default_fields(types_by_name, f["type"])

    # Classify args: expand INPUT_OBJECT args into kwargs, keep scalars as-is
    required_params: list[tuple[str, str, str, str | None]] = []  # (py, gql, type, input_cls)
    optional_params: list[tuple[str, str, str, str | None]] = []
    # Track which GraphQL args are expanded inputs so we can construct them in the body
    expanded_inputs: dict[str, tuple[str, list]] = {}  # gql_arg_name -> (InputClassName, [(py_name, gql_field_name, is_optional)])

    # First pass: collect all input field names to detect collisions
    input_field_names: set[str] = set()
    for a in args:
        input_cls = _is_input_object(a["type"], types_by_name)
        if input_cls:
            input_type = types_by_name[input_cls]
            for inf in input_type.get("inputFields") or []:
                input_field_names.add(safe_name(inf["name"]))

    for a in args:
        aname = safe_name(a["name"])
        atype, anullable = resolve_type(a["type"])
        input_cls = _is_input_object(a["type"], types_by_name)

        if input_cls:
            # Expand input fields as kwargs (they keep their natural names)
            input_type = types_by_name[input_cls]
            input_fields = input_type.get("inputFields") or []
            expanded_fields = []
            for inf in input_fields:
                inf_name = safe_name(inf["name"])
                inf_type, inf_nullable = resolve_type(inf["type"])
                expanded_fields.append((inf_name, inf["name"], inf_nullable))
                if inf_nullable:
                    optional_params.append((inf_name, inf["name"], inf_type, input_cls))
                else:
                    required_params.append((inf_name, inf["name"], inf_type, input_cls))
            expanded_inputs[a["name"]] = (input_cls, expanded_fields)
        else:
            # Prefix direct args with _ if they collide with expanded input fields
            param_name = f"_{aname}" if aname in input_field_names else aname
            if anullable:
                optional_params.append((param_name, a["name"], atype, None))
            else:
                required_params.append((param_name, a["name"], atype, None))

    # Build method signature
    params = ["self"]
    for py_name, gql_name, py_type, _ in required_params:
        params.append(f"{py_name}: {py_type}")
    if optional_params:
        params.append("*")
        for py_name, gql_name, py_type, _ in optional_params:
            params.append(f"{py_name}: Optional[{py_type}] = None")

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

    lines.append(f'        query = """{gql}"""')

    # Build variables dict
    var_entries = []
    for a in args:
        if a["name"] in expanded_inputs:
            # Construct the input object from expanded kwargs
            input_cls, fields = expanded_inputs[a["name"]]
            field_assignments = ", ".join(f"{safe_name(gql_f)}={param_name}" for param_name, gql_f, _ in fields)
            var_entries.append(f'"{a["name"]}": _prepare_input({input_cls}({field_assignments}))')
        else:
            aname = safe_name(a["name"])
            param_name = f"_{aname}" if aname in input_field_names else aname
            var_entries.append(f'"{a["name"]}": _prepare_input({param_name})')

    # Determine how to handle the return value
    is_scalar = _is_scalar_return(f["type"])
    is_list = _is_list_return(f["type"])
    base_type_name = _unwrap_type_name(f["type"])

    if var_entries:
        lines.append("        variables: dict[str, Any] = {")
        for v in var_entries:
            lines.append(f"            {v},")
        lines.append("        }")
        lines.append("        variables = {k: v for k, v in variables.items() if v is not None}")
        data_expr = f'self._execute(query, variables).get("{name}")'
    else:
        data_expr = f'self._execute(query).get("{name}")'

    if is_scalar or base_type_name in SCALAR_MAP or ret_type in ("Any", "None", "bool", "str", "int", "float"):
        # Scalar returns — no model parsing needed
        lines.append(f"        return {data_expr}")
    elif is_list:
        # List of models — use TypeAdapter for validation
        # Strip the list[] wrapper to get the inner type for display
        inner_type = ret_type
        if inner_type.startswith("list[") and inner_type.endswith("]"):
            inner_type = inner_type[5:-1]
        lines.append(f"        _data = {data_expr}")
        lines.append(f"        return TypeAdapter(list[{inner_type}]).validate_python(_data) if _data else []")
    else:
        # Single model — use model_validate
        # ret_type might be quoted like '"Project"', unquote for the validate call
        model_name = ret_type.strip('"')
        if ret_nullable:
            lines.append(f"        _data = {data_expr}")
            lines.append(f"        return {model_name}.model_validate(_data) if _data else None")
        else:
            lines.append(f"        return {model_name}.model_validate({data_expr})")

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

def gen_init(input_classes: list[str], type_classes: list[str]) -> str:
    lines = [
        '"""Railway Python SDK \u2013 A fully typed client for the Railway GraphQL API."""',
        "",
        "from .client import RailwayClient, RailwayError",
        "from .enums import *  # noqa: F401,F403",
        "from .inputs import *  # noqa: F401,F403",
        "from .types import *  # noqa: F401,F403",
        "",
        '__all__ = ["RailwayClient", "RailwayError"]',
        "",
        "# Resolve forward references now that all models are in scope",
    ]
    for name in input_classes + type_classes:
        lines.append(f"{name}.model_rebuild()")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: generate.py <introspection.json>")
        sys.exit(1)

    schema = load_schema(sys.argv[1])
    types = schema["types"]

    out = Path(__file__).resolve().parent.parent / "railway"

    (out / "enums.py").write_text(gen_enums(types))
    print("✓ enums.py")

    inputs_code, input_classes = gen_input_types(types)
    (out / "inputs.py").write_text(inputs_code)
    print("✓ inputs.py")

    types_code, type_classes = gen_object_types(types)
    (out / "types.py").write_text(types_code)
    print("✓ types.py")

    (out / "client.py").write_text(gen_client(types, schema))
    print("✓ client.py")

    (out / "__init__.py").write_text(gen_init(input_classes, type_classes))
    print("✓ __init__.py")

    print("Done – generated Railway SDK.")


if __name__ == "__main__":
    main()
