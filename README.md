# railway-python

A fully typed Python client for the [Railway](https://railway.com) GraphQL API.

Railway doesn't publish an official Python SDK, but they do expose a complete GraphQL schema via introspection. This library is auto-generated from that schema, giving you a typed Python wrapper around every query and mutation in the Railway API — no manual maintenance required.

## Install

```bash
pip install railway-python
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

All methods return fully typed Pydantic models. Response fields are accessed via snake_case attributes (e.g. `project.base_environment_id`). Mutations that take an `input` argument have their fields expanded as kwargs — no need to import input types.

### Queries

#### Authentication & User

```python
# Get current authenticated user
me() -> User

# Get current API token context
api_token() -> ApiTokenContext

# List API tokens
api_tokens(after, before, first, last) -> QueryApiTokensConnection

# Get current project token
project_token() -> ProjectToken

# List project tokens
project_tokens(project_id, after, before, first, last) -> QueryProjectTokensConnection

# Get two-factor auth info
two_factor_info() -> TwoFactorInfo

# List passkeys
passkeys(after, before, first, last) -> QueryPasskeysConnection

# List sessions
sessions(after, before, first, last) -> QuerySessionsConnection

# Get user preferences
preferences(token) -> Preferences

# Get user profile by username
user_profile(username) -> UserProfileResponse
```

#### Projects

```python
# Get a single project
project(id) -> Project

# List projects
projects(after, before, first, include_deleted, last, user_id, workspace_id) -> QueryProjectsConnection

# Get project members
project_members(project_id) -> list[ProjectMember]

# Get project workspace members
project_workspace_members(project_id) -> ProjectWorkspaceMembersResponse

# Get project invitations
project_invitations(id) -> list[ProjectInvitation]

# Get a project invitation by code
project_invitation(code) -> PublicProjectInvitation

# Get a project invite code
project_invite_code(project_id, role) -> InviteCode

# Get project resource access
project_resource_access(project_id) -> ProjectResourceAccess

# Get project compliance info
project_compliance(project_id) -> ProjectComplianceInfo
```

#### Services

```python
# Get a single service
service(id) -> Service

# Get service instance configuration
service_instance(environment_id, service_id) -> ServiceInstance

# Check if a service instance is updatable
service_instance_is_updatable(environment_id, service_id) -> bool

# Get service instance resource limits
service_instance_limits(environment_id, service_id) -> ServiceInstanceLimit

# Get service instance limit overrides
service_instance_limit_override(environment_id, service_id) -> ServiceInstanceLimit | None

# Check if a service domain is available
service_domain_available(domain) -> DomainAvailable
```

#### Environments

```python
# Get a single environment
environment(id, project_id) -> Environment

# List environments for a project
environments(project_id, after, before, first, is_ephemeral, last) -> QueryEnvironmentsConnection

# Get environment logs
environment_logs(environment_id, after_date, after_limit, anchor_date, before_date, before_limit, filter) -> list[Log]

# Get environment patch
environment_patch(id) -> EnvironmentPatch

# List environment patches
environment_patches(environment_id, after, before, first, last) -> QueryEnvironmentPatchesConnection

# Get staged changes
environment_staged_changes(environment_id) -> EnvironmentPatch
```

#### Deployments

```python
# Get a single deployment
deployment(id) -> Deployment

# List deployments
deployments(input, after, before, first, last) -> QueryDeploymentsConnection

# Get deployment events
deployment_events(id, after, before, first, last) -> QueryDeploymentEventsConnection

# Get build logs
build_logs(deployment_id, end_date, filter, limit, start_date) -> list[Log]

# Get deployment logs
deployment_logs(deployment_id, end_date, filter, limit, start_date) -> list[Log]

# Get deployment snapshot
deployment_snapshot(deployment_id) -> DeploymentSnapshot | None

# Get deployment triggers
deployment_triggers(environment_id, project_id, service_id, after, before, first, last) -> QueryDeploymentTriggersConnection

# Get deployment instance executions
deployment_instance_executions(input, after, before, first, last) -> QueryDeploymentInstanceExecutionsConnection
```

#### Domains & Networking

```python
# Get all domains for a service
domains(environment_id, project_id, service_id) -> AllDomains

# Get a custom domain
custom_domain(id, project_id) -> CustomDomain

# Check custom domain availability
custom_domain_available(domain) -> DomainAvailable

# Get TCP proxies
tcp_proxies(environment_id, service_id) -> list[TCPProxy]

# Get private networks
private_networks(environment_id) -> list[PrivateNetwork]

# Get a private network endpoint
private_network_endpoint(environment_id, private_network_id, service_id) -> PrivateNetworkEndpoint | None

# Check private network endpoint name availability
private_network_endpoint_name_available(environment_id, prefix, private_network_id) -> bool

# Get egress gateways
egress_gateways(environment_id, service_id) -> list[EgressGateway]
```

#### Variables

```python
# Get variables for a service/environment
variables(environment_id, project_id, service_id, unrendered) -> Any

# Get variables for a service deployment
variables_for_service_deployment(environment_id, project_id, service_id) -> Any
```

#### Metrics & Usage

```python
# Get metrics
metrics(measurements, start_date, averaging_window_seconds, end_date, environment_id, group_by, include_deleted, project_id, sample_rate_seconds, service_id, volume_id, volume_instance_external_id, workspace_id) -> list[MetricsResult]

# Get aggregated usage
usage(measurements, end_date, group_by, include_deleted, project_id, start_date, workspace_id) -> list[AggregatedUsage]

# Get estimated usage
estimated_usage(measurements, include_deleted, project_id, workspace_id) -> list[EstimatedUsage]

# Get HTTP metrics
http_metrics(end_date, environment_id, service_id, start_date, method, path, status_code, step_seconds) -> HttpMetricsResult

# Get HTTP duration metrics
http_duration_metrics(end_date, environment_id, service_id, start_date, method, path, status_code, step_seconds) -> HttpDurationMetricsResult

# Get HTTP metrics grouped by status code
http_metrics_grouped_by_status(end_date, environment_id, service_id, start_date, method, path, step_seconds) -> list[HttpMetricsByStatusResult]

# Get HTTP logs
http_logs(deployment_id, after_date, after_limit, anchor_date, before_date, before_limit, end_date, filter, limit, start_date) -> list[HttpLog]
```

#### Volumes

```python
# Get a volume instance
volume_instance(id) -> VolumeInstance

# List volume instance backups
volume_instance_backup_list(volume_instance_id) -> list[VolumeInstanceBackup]

# List volume instance backup schedules
volume_instance_backup_schedule_list(volume_instance_id) -> list[VolumeInstanceBackupSchedule]
```

#### Workspaces

```python
# Get a workspace
workspace(workspace_id) -> Workspace

# Get a workspace by invite code
workspace_by_code(code) -> Workspace

# Get workspace policy
workspace_policy(workspace_id) -> WorkspacePolicy | None

# Get workspace identity providers
workspace_identity_providers(workspace_id, after, before, first, last) -> QueryWorkspaceIdentityProvidersConnection

# Get workspace templates
workspace_templates(workspace_id, after, before, first, last) -> QueryWorkspaceTemplatesConnection

# Get trusted domains
trusted_domains(workspace_id, after, before, first, last) -> QueryTrustedDomainsConnection

# Get external workspaces
external_workspaces(project_id) -> list[ExternalWorkspace]
```

#### Templates

```python
# Get a template
template(code, id, owner, repo) -> Template

# Get template metrics
template_metrics(id) -> TemplateMetrics

# Get template source for a project
template_source_for_project(project_id) -> Template | None

# List templates
templates(after, before, first, last, recommended, verified) -> QueryTemplatesConnection

# Get templates count
templates_count() -> int
```

#### GitHub Integration

```python
# List GitHub repos
github_repos() -> list[GitHubRepo]

# Get a GitHub repo
github_repo(full_repo_name) -> GitHubRepoWithoutInstallation

# List branches for a GitHub repo
github_repo_branches(owner, repo) -> list[GitHubBranch]

# Check GitHub repo access
git_hub_repo_access_available(full_repo_name) -> GitHubAccess

# Check if a GitHub repo name is available
github_is_repo_name_available(full_repo_name) -> bool

# Get GitHub PR info
github_pr_info(pr_number, service_id) -> GitHubPRInfo | None

# Get GitHub writable scopes
github_writable_scopes() -> list[str]

# Get GitHub SSH keys
git_hub_ssh_keys() -> list[GitHubSshKey]
```

#### Integrations

```python
# Get an integration auth
integration_auth(provider, provider_id) -> IntegrationAuth

# List integration auths
integration_auths(after, before, first, last) -> QueryIntegrationAuthsConnection

# List integrations
integrations(project_id, after, before, first, last) -> QueryIntegrationsConnection

# Get Vercel info
vercel_info() -> VercelInfo

# List Heroku apps
heroku_apps() -> list[HerokuApp]
```

#### Audit Logs

```python
# Get an audit log
audit_log(id, workspace_id) -> AuditLog

# List audit logs
audit_logs(workspace_id, after, before, filter, first, last, sort) -> QueryAuditLogsConnection

# Get audit log event type info
audit_log_event_type_info() -> list[AuditLogEventTypeInfo]
```

#### Observability

```python
# List observability dashboards
observability_dashboards(environment_id, after, before, first, last) -> QueryObservabilityDashboardsConnection
```

#### Buckets

```python
# Get bucket instance details
bucket_instance_details(bucket_id, environment_id) -> BucketInstanceDetails | None

# Get bucket S3 credentials
bucket_s3_credentials(bucket_id, environment_id, project_id) -> list[BucketS3CompatibleCredentials]
```

#### Notifications

```python
# List notification deliveries
notification_deliveries(after, before, filter, first, last) -> QueryNotificationDeliveriesConnection

# List notification rules
notification_rules(workspace_id, project_id) -> list[NotificationRule]
```

#### Other

```python
# Get events
events(project_id, after, before, environment_id, filter, first, last) -> QueryEventsConnection

# Get platform status
platform_status() -> PlatformStatus

# Get public stats
public_stats() -> PublicStats

# Get available regions
regions(project_id) -> list[Region]

# Get resource access
resource_access(explicit_resource_owner) -> ResourceAccess

# Get referral info
referral_info(workspace_id) -> ReferralInfo

# Get invite code
invite_code(code) -> InviteCode

# Get compliance agreements
compliance_agreements(workspace_id) -> ComplianceAgreementsInfo

# Get SSH public keys
ssh_public_keys(after, before, first, last) -> QuerySshPublicKeysConnection

# Get workflow status
workflow_status(workflow_id) -> WorkflowResult

# Canvas view merge preview
canvas_view_merge_preview(source_environment_id, target_environment_id) -> CanvasViewMergePreview

# Get function runtimes
function_runtimes() -> list[FunctionRuntime]

# Get a function runtime
function_runtime(name) -> FunctionRuntime
```

### Mutations

#### API Tokens

```python
# Create an API token
api_token_create(input: ApiTokenCreateInput) -> str

# Delete an API token
api_token_delete(id) -> bool
```

#### Projects

```python
# Create a project
project_create(input: ProjectCreateInput) -> Project

# Update a project
project_update(id, input: ProjectUpdateInput) -> Project

# Delete a project
project_delete(id) -> bool

# Claim a project
project_claim(id, workspace_id) -> Project

# Transfer a project
project_transfer(input: ProjectTransferInput, project_id) -> bool
project_transfer_initiate(input: ProjectTransferInitiateInput) -> bool
project_transfer_confirm(input: ProjectTransferConfirmInput) -> bool

# Leave a project
project_leave(id) -> bool

# Schedule/cancel project deletion
project_schedule_delete(id) -> bool
project_schedule_delete_cancel(id) -> bool
project_schedule_delete_force(id) -> bool

# Manage project tokens
project_token_create(input: ProjectTokenCreateInput) -> str
project_token_delete(id) -> bool

# Manage project members
project_member_add(input: ProjectMemberAddInput) -> ProjectMember
project_member_remove(input: ProjectMemberRemoveInput) -> list[ProjectMember]
project_member_update(input: ProjectMemberUpdateInput) -> ProjectMember

# Manage project invitations
project_invitation_accept(code) -> ProjectPermission
project_invitation_create(id, input: ProjectInvitee) -> ProjectInvitation
project_invitation_delete(id) -> bool
project_invitation_resend(id) -> ProjectInvitation
project_invite_user(id, input: ProjectInviteUserInput) -> bool

# Project feature flags
project_feature_flag_add(input: ProjectFeatureFlagToggleInput) -> bool
project_feature_flag_remove(input: ProjectFeatureFlagToggleInput) -> bool
```

#### Services

```python
# Create a service
service_create(input: ServiceCreateInput) -> Service

# Update a service
service_update(id, input: ServiceUpdateInput) -> Service

# Delete a service
service_delete(id, environment_id) -> bool

# Connect/disconnect a service to a repo
service_connect(id, input: ServiceConnectInput) -> Service
service_disconnect(id) -> Service

# Remove upstream URL
service_remove_upstream_url(id) -> Service

# Deploy a service instance
service_instance_deploy(environment_id, service_id, commit_sha, latest_commit) -> bool
service_instance_deploy_v2(environment_id, service_id, commit_sha) -> str

# Redeploy a service instance
service_instance_redeploy(environment_id, service_id) -> bool

# Update service instance configuration
service_instance_update(input: ServiceInstanceUpdateInput, service_id, environment_id) -> bool

# Update service instance resource limits
service_instance_limits_update(input: ServiceInstanceLimitsUpdateInput) -> bool

# Service feature flags
service_feature_flag_add(input: ServiceFeatureFlagToggleInput) -> bool
service_feature_flag_remove(input: ServiceFeatureFlagToggleInput) -> bool
```

#### Environments

```python
# Create an environment
environment_create(input: EnvironmentCreateInput) -> Environment

# Delete an environment
environment_delete(id) -> bool

# Rename an environment
environment_rename(id, input: EnvironmentRenameInput) -> Environment

# Commit environment patches
environment_patch_commit(environment_id, commit_message, patch) -> str
environment_patch_commit_staged(environment_id, commit_message, skip_deploys) -> str

# Stage changes
environment_stage_changes(environment_id, input: EnvironmentConfig, merge) -> EnvironmentPatch

# Trigger deploys
environment_triggers_deploy(input: EnvironmentTriggersDeployInput) -> bool

# Unskip a service in an environment
environment_unskip_service(environment_id, service_id) -> bool
```

#### Deployments

```python
# Approve a deployment
deployment_approve(id) -> bool

# Cancel a deployment
deployment_cancel(id) -> bool

# Redeploy
deployment_redeploy(id, use_previous_image_tag) -> Deployment

# Remove a deployment
deployment_remove(id) -> bool

# Restart a deployment
deployment_restart(id) -> bool

# Rollback a deployment
deployment_rollback(id) -> bool

# Stop a deployment
deployment_stop(id) -> bool

# Manage deployment triggers
deployment_trigger_create(input: DeploymentTriggerCreateInput) -> DeploymentTrigger
deployment_trigger_delete(id) -> bool
deployment_trigger_update(id, input: DeploymentTriggerUpdateInput) -> DeploymentTrigger

# Create deployment instance execution
deployment_instance_execution_create(input: DeploymentInstanceExecutionCreateInput) -> bool
```

#### Domains

```python
# Create a custom domain
custom_domain_create(input: CustomDomainCreateInput) -> CustomDomain

# Delete a custom domain
custom_domain_delete(id) -> bool

# Update a custom domain
custom_domain_update(environment_id, id, target_port) -> bool

# Create a service domain
service_domain_create(input: ServiceDomainCreateInput) -> ServiceDomain

# Delete a service domain
service_domain_delete(id) -> bool

# Update a service domain
service_domain_update(input: ServiceDomainUpdateInput) -> bool

# Delete a TCP proxy
tcp_proxy_delete(id) -> bool
```

#### Networking

```python
# Create or get a private network
private_network_create_or_get(input: PrivateNetworkCreateOrGetInput) -> PrivateNetwork

# Create or get a private network endpoint
private_network_endpoint_create_or_get(input: PrivateNetworkEndpointCreateOrGetInput) -> PrivateNetworkEndpoint

# Delete a private network endpoint
private_network_endpoint_delete(id) -> bool

# Rename a private network endpoint
private_network_endpoint_rename(dns_name, id, private_network_id) -> bool

# Delete all private networks for an environment
private_networks_for_environment_delete(environment_id) -> bool

# Create an egress gateway association
egress_gateway_association_create(input: EgressGatewayCreateInput) -> list[EgressGateway]

# Clear egress gateway associations
egress_gateway_associations_clear(input: EgressGatewayServiceTargetInput) -> bool
```

#### Variables

```python
# Upsert a variable
variable_upsert(input: VariableUpsertInput) -> bool

# Delete a variable
variable_delete(input: VariableDeleteInput) -> bool

# Upsert a collection of variables
variable_collection_upsert(input: VariableCollectionUpsertInput) -> bool

# Configure a shared variable
shared_variable_configure(input: SharedVariableConfigureInput) -> Variable
```

#### Volumes

```python
# Create a volume
volume_create(input: VolumeCreateInput) -> Volume

# Delete a volume
volume_delete(volume_id) -> bool

# Update a volume
volume_update(input: VolumeUpdateInput, volume_id) -> Volume

# Update a volume instance
volume_instance_update(input: VolumeInstanceUpdateInput, volume_id, environment_id) -> bool

# Manage volume backups
volume_instance_backup_create(volume_instance_id, name) -> WorkflowId
volume_instance_backup_delete(volume_instance_backup_id, volume_instance_id) -> WorkflowId
volume_instance_backup_lock(volume_instance_backup_id, volume_instance_id) -> bool
volume_instance_backup_restore(volume_instance_backup_id, volume_instance_id) -> WorkflowId

# Update backup schedule
volume_instance_backup_schedule_update(kinds, volume_instance_id) -> bool
```

#### Buckets

```python
# Create a bucket
bucket_create(input: BucketCreateInput) -> Bucket

# Update a bucket
bucket_update(id, input: BucketUpdateInput) -> Bucket

# Reset bucket credentials
bucket_credentials_reset(bucket_id, environment_id, project_id) -> BucketS3CompatibleCredentials
```

#### Workspaces

```python
# Update a workspace
workspace_update(id, input: WorkspaceUpdateInput) -> bool

# Delete a workspace
workspace_delete(id) -> bool

# Leave a workspace
workspace_leave(id) -> bool

# Invite a user to a workspace
workspace_user_invite(input: WorkspaceUserInviteInput, workspace_id) -> bool

# Remove a user from a workspace
workspace_user_remove(input: WorkspaceUserRemoveInput, workspace_id) -> bool

# Change workspace permissions
workspace_permission_change(input: WorkspacePermissionChangeInput) -> bool

# Create a workspace invite code
workspace_invite_code_create(input: WorkspaceInviteCodeCreateInput, workspace_id) -> str

# Use a workspace invite code
workspace_invite_code_use(code) -> Workspace

# Manage workspace policies
workspace_policy_item_update(workspace_id, enabled, input, policy) -> bool

# Manage workspace 2FA enforcement
workspace_two_factor_enforcement_update(enabled, workspace_id) -> bool

# Upsert Slack channel
workspace_upsert_slack_channel(id) -> bool
```

#### Templates

```python
# Clone a template
template_clone(input: TemplateCloneInput) -> Template

# Deploy a template
template_deploy_v2(input: TemplateDeployV2Input) -> TemplateDeployPayload

# Generate a template
template_generate(input: TemplateGenerateInput) -> Template

# Publish a template
template_publish(id, input: TemplatePublishInput) -> Template

# Unpublish a template
template_unpublish(id) -> bool

# Delete a template
template_delete(id, input: TemplateDeleteInput) -> bool

# Eject a template service source
template_service_source_eject(input: TemplateServiceSourceEjectInput) -> bool
```

#### Docker Compose

```python
# Import a Docker Compose file
docker_compose_import(environment_id, project_id, yaml, skip_staging_patch) -> DockerComposeImport
```

#### Integrations

```python
# Create an integration
integration_create(input: IntegrationCreateInput) -> Integration

# Update an integration
integration_update(id, input: IntegrationUpdateInput) -> Integration

# Delete an integration
integration_delete(id) -> bool

# Remove a provider auth
provider_auth_remove(id) -> bool

# Deploy from GitHub repo
github_repo_deploy(input: GitHubRepoDeployInput) -> str

# Update GitHub repo connection
github_repo_update(input: GitHubRepoUpdateInput) -> bool

# Import variables from Heroku
heroku_import_variables(input: HerokuImportVariablesInput) -> int

# Canvas view merge
canvas_view_merge(source_environment_id, target_environment_id) -> bool
```

#### Notifications

```python
# Mark notification deliveries as read
notification_deliveries_mark_as_read(delivery_ids) -> bool

# Create a notification rule
notification_rule_create(input: CreateNotificationRuleInput) -> NotificationRule

# Update a notification rule
notification_rule_update(id, input: UpdateNotificationRuleInput) -> NotificationRule

# Delete a notification rule
notification_rule_delete(id) -> bool
```

#### Observability

```python
# Create an observability dashboard
observability_dashboard_create(input: ObservabilityDashboardCreateInput) -> bool

# Update an observability dashboard
observability_dashboard_update(id, input) -> bool

# Reset an observability dashboard
observability_dashboard_reset(id) -> bool
```

#### Trusted Domains

```python
# Create a trusted domain
trusted_domain_create(input: WorkspaceTrustedDomainCreateInput) -> TrustedDomain

# Delete a trusted domain
trusted_domain_delete(id) -> bool

# Retrigger trusted domain verification
trusted_domain_retrigger_verification(id) -> TrustedDomain | None
```

#### User Account

```python
# Update user preferences
preferences_update(input: PreferencesUpdateData) -> Preferences

# Update user profile
user_profile_update(input: UserProfileUpdateInput) -> bool

# Update user terms
user_terms_update() -> User | None

# Delete user account
user_delete() -> bool

# Agree to fair use
fair_use_agree(agree) -> bool

# Set/remove user flags
user_flags_set(input: UserFlagsSetInput) -> bool
user_flags_remove(input: UserFlagsRemoveInput) -> bool

# Leave beta
user_beta_leave() -> bool

# Disconnect Discord
user_discord_disconnect() -> bool

# Initiate/confirm email change
email_change_initiate(new_email) -> bool
email_change_confirm(nonce) -> bool

# Two-factor auth management
two_factor_info_create(input: TwoFactorInfoCreateInput) -> RecoveryCodes
two_factor_info_validate(input: TwoFactorInfoValidateInput) -> bool
two_factor_info_secret() -> TwoFactorInfoSecret
two_factor_info_delete() -> bool

# Recovery codes
recovery_code_generate() -> RecoveryCodes
recovery_code_validate(input: RecoveryCodeValidateInput) -> bool

# SSH keys
ssh_public_key_create(input: SshPublicKeyCreateInput) -> SshPublicKey
ssh_public_key_delete(id) -> bool

# Passkeys
passkey_delete(id) -> bool

# Sessions
session_delete(id) -> bool
```

#### Usage Limits

```python
# Set a usage limit
usage_limit_set(input: UsageLimitSetInput) -> bool

# Remove a usage limit
usage_limit_remove(input: UsageLimitRemoveInput) -> bool
```

#### Referrals

```python
# Update referral info
referral_info_update(input: ReferralInfoUpdateInput) -> ReferralInfo

# Use an invite code
invite_code_use(code) -> Project

# Upsert Slack channel
upsert_slack_channel(workspace_id) -> bool
```

#### Webhooks

```python
# Test a webhook
webhook_test(payload, url) -> int
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
