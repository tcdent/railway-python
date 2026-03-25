# railway-python

A fully typed Python client for the [Railway](https://railway.com) GraphQL API.

Railway doesn't publish an official Python SDK, but they do expose a complete GraphQL schema via introspection. This library is auto-generated from that schema, giving you a typed Python wrapper around every query and mutation in the Railway API — no manual maintenance required.

## Install

```bash
uv add railway-client
```

## Quick Start

```python
from railway import RailwayClient

client = RailwayClient(api_token="your-api-token")

# Get current user — returns a Pydantic model, not a raw dict
user = client.me()
print(user.name, user.email)

# List all projects
projects = client.projects()
for edge in projects.edges:
    print(edge.node.name)

# Create a project — input fields are expanded as kwargs
project = client.project_create(name="my-app", workspace_id="your-workspace-id")
print(project.id, project.name)

# Get variables for a service
vars = client.variables(
    environment_id="env-id",
    project_id="project-id",
    service_id="service-id",
)
```

All response types are [Pydantic](https://docs.pydantic.dev/) models with snake_case field names. The camelCase↔snake_case mapping is handled declaratively via `alias_generator` — no runtime string conversion.

### Project Token Authentication

```python
client = RailwayClient(project_token="your-project-token")
```

### Context Manager

```python
with RailwayClient(api_token="token") as client:
    me = client.me()
    print(me.name)
```

### Raw GraphQL

```python
data = client._execute("""
    query {
        me { name email }
    }
""")
```

---

## API Reference

Every query and mutation in the Railway GraphQL API has a corresponding method on `RailwayClient`. All methods return fully typed Pydantic models with snake_case attributes. Input fields are expanded as kwargs — no need to import input types.

Use your editor's autocomplete to explore the full API. Here are some common operations:

### Projects

```python
# List projects
projects = client.projects()
for edge in projects.edges:
    print(edge.node.name)

# Create a project
project = client.project_create(name="my-app", workspace_id="...")

# Update a project
client.project_update(id="proj-id", name="new-name")

# Delete a project
client.project_delete(id="proj-id")
```

### Services

```python
# Create a service
service = client.service_create(project_id="proj-id", name="api")

# Update a service
client.service_update(id="svc-id", name="new-name", icon="🚀")

# Get service instance
instance = client.service_instance(environment_id="env-id", service_id="svc-id")
print(instance.start_command, instance.num_replicas)
```

### Deployments

```python
# List deployments
deps = client.deployments(project_id="proj-id", environment_id="env-id", service_id="svc-id")

# Get build/deploy logs
logs = client.build_logs(deployment_id="dep-id")
for log in logs:
    print(log.timestamp, log.message)

# Restart / rollback / cancel
client.deployment_restart(id="dep-id")
client.deployment_rollback(id="dep-id")
```

### Variables

```python
# Get variables
vars = client.variables(
    environment_id="env-id",
    project_id="proj-id",
    service_id="svc-id",
)

# Set a variable
client.variable_upsert(
    project_id="proj-id",
    environment_id="env-id",
    service_id="svc-id",
    name="DATABASE_URL",
    value="postgres://...",
)
```

### Environments

```python
# Create an environment
env = client.environment_create(project_id="proj-id", name="staging")

# List environments
envs = client.environments(project_id="proj-id")
```

### Domains

```python
# Get all domains for a service
domains = client.domains(
    environment_id="env-id",
    project_id="proj-id",
    service_id="svc-id",
)

# Create a service domain
domain = client.service_domain_create(
    environment_id="env-id",
    service_id="svc-id",
)
```

### Volumes

```python
# Create a volume
volume = client.volume_create(project_id="proj-id")

# Update mount path
client.volume_instance_update(
    volume_id="vol-id",
    environment_id="env-id",
    mount_path="/data",
    service_id="svc-id",
)
```

---

## Development

Generated from the Railway GraphQL schema using `scripts/generate.py`:

```bash
# Fetch the schema and regenerate
curl -s -X POST https://backboard.railway.com/graphql/v2 \
  -H "Content-Type: application/json" \
  -d '{"query":"{ __schema { types { name kind description fields { name description type { name kind ofType { name kind ofType { name kind ofType { name kind } } } } args { name description type { name kind ofType { name kind ofType { name kind ofType { name kind } } } } defaultValue } } inputFields { name description type { name kind ofType { name kind ofType { name kind ofType { name kind } } } } defaultValue } enumValues { name description } possibleTypes { name } } directives { name description locations args { name description type { name kind ofType { name kind } } defaultValue } } queryType { name } mutationType { name } subscriptionType { name } } }"}' \
  > schema.json

python scripts/generate.py schema.json
```

## License

MIT
