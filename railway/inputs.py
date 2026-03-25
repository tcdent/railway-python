from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from .enums import *  # noqa: F401,F403


class _Base(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class ApiTokenCreateInput(_Base):
    name: str
    workspace_id: Optional[str] = None


class AuditLogFilterInput(_Base):
    end_date: Optional[str] = None
    environment_id: Optional[str] = None
    event_types: Optional[list[str]] = None
    project_id: Optional[str] = None
    start_date: Optional[str] = None


class BaseEnvironmentOverrideInput(_Base):
    base_environment_override_id: Optional[str] = None


class BucketCreateInput(_Base):
    project_id: str
    environment_id: Optional[str] = None
    name: Optional[str] = None


class BucketUpdateInput(_Base):
    name: str


class CliEventTrackInput(_Base):
    arch: str
    cli_version: str
    command: str
    duration_ms: int
    is_ci: bool
    os: str
    success: bool
    error_message: Optional[str] = None
    sub_command: Optional[str] = None


class CreateNotificationRuleInput(_Base):
    channel_configs: list[Any]
    event_types: list[str]
    workspace_id: str
    ephemeral_environments: Optional[bool] = None
    project_id: Optional[str] = None
    severities: Optional[list["NotificationSeverity"]] = None


class CustomDomainCreateInput(_Base):
    domain: str
    environment_id: str
    project_id: str
    service_id: str
    target_port: Optional[int] = None


class DeploymentInstanceExecutionCreateInput(_Base):
    service_instance_id: str


class DeploymentInstanceExecutionInput(_Base):
    deployment_id: str


class DeploymentInstanceExecutionListInput(_Base):
    environment_id: str
    service_id: str


class DeploymentListInput(_Base):
    environment_id: Optional[str] = None
    include_deleted: Optional[bool] = None
    project_id: Optional[str] = None
    service_id: Optional[str] = None
    status: Optional["DeploymentStatusInput"] = None


class DeploymentStatusInput(_Base):
    in_: Optional[list["DeploymentStatus"]] = None
    not_in: Optional[list["DeploymentStatus"]] = None


class DeploymentTriggerCreateInput(_Base):
    branch: str
    environment_id: str
    project_id: str
    provider: str
    repository: str
    service_id: str
    check_suites: Optional[bool] = None
    root_directory: Optional[str] = None


class DeploymentTriggerUpdateInput(_Base):
    branch: Optional[str] = None
    check_suites: Optional[bool] = None
    repository: Optional[str] = None
    root_directory: Optional[str] = None


class EgressGatewayCreateInput(_Base):
    environment_id: str
    service_id: str
    region: Optional[str] = None


class EgressGatewayServiceTargetInput(_Base):
    environment_id: str
    service_id: str


class EnvironmentCreateInput(_Base):
    name: str
    project_id: str
    apply_changes_in_background: Optional[bool] = None
    ephemeral: Optional[bool] = None
    skip_initial_deploys: Optional[bool] = None
    source_environment_id: Optional[str] = None
    stage_initial_changes: Optional[bool] = None


class EnvironmentRenameInput(_Base):
    name: str


class EnvironmentTriggersDeployInput(_Base):
    environment_id: str
    project_id: str
    service_id: str


class EventFilterInput(_Base):
    action: Optional["EventStringListFilter"] = None
    object: Optional["EventStringListFilter"] = None
    service_id: Optional["EventStringListFilter"] = None


class EventStringListFilter(_Base):
    in_: Optional[list[str]] = None
    not_in: Optional[list[str]] = None


class ExplicitOwnerInput(_Base):
    id: str
    type: Optional["ResourceOwnerType"] = None


class FeatureFlagToggleInput(_Base):
    flag: "ActiveFeatureFlag"


class GitHubRepoDeployInput(_Base):
    project_id: str
    repo: str
    branch: Optional[str] = None
    environment_id: Optional[str] = None


class GitHubRepoUpdateInput(_Base):
    environment_id: str
    project_id: str
    service_id: str


class HerokuImportVariablesInput(_Base):
    environment_id: str
    heroku_app_id: str
    project_id: str
    service_id: str


class IntegrationCreateInput(_Base):
    config: Any
    name: str
    project_id: str
    integration_auth_id: Optional[str] = None


class IntegrationUpdateInput(_Base):
    config: Any
    name: str
    project_id: str
    integration_auth_id: Optional[str] = None


class JobApplicationCreateInput(_Base):
    email: str
    job_id: str
    name: str
    why: str


class LoginSessionAuthInput(_Base):
    code: str
    hostname: Optional[str] = None


class NotificationDeliveryFilterInput(_Base):
    environment_id: Optional[str] = None
    only_unread: Optional[bool] = None
    project_id: Optional[str] = None
    status: Optional["NotificationStatus"] = None
    type: Optional["NotificationDeliveryType"] = None
    workspace_id: Optional[str] = None


class ObservabilityDashboardCreateInput(_Base):
    environment_id: str
    items: Optional[list["ObservabilityDashboardUpdateInput"]] = None


class ObservabilityDashboardItemConfigInput(_Base):
    logs_filter: Optional[str] = None
    measurements: Optional[list["MetricMeasurement"]] = None
    project_usage_properties: Optional[list["ProjectUsageProperty"]] = None
    resource_ids: Optional[list[str]] = None


class ObservabilityDashboardItemCreateInput(_Base):
    config: "ObservabilityDashboardItemConfigInput"
    id: str
    name: str
    type: "ObservabilityDashboardItemType"
    description: Optional[str] = None


class ObservabilityDashboardUpdateInput(_Base):
    dashboard_item: "ObservabilityDashboardItemCreateInput"
    display_config: Any
    id: str


class PluginCreateInput(_Base):
    name: str
    project_id: str
    environment_id: Optional[str] = None
    friendly_name: Optional[str] = None


class PluginRestartInput(_Base):
    environment_id: Optional[str] = None


class PluginUpdateInput(_Base):
    friendly_name: str


class PreferencesUpdateData(_Base):
    build_failed_email: Optional[bool] = None
    changelog_email: Optional[bool] = None
    community_email: Optional[bool] = None
    deploy_crashed_email: Optional[bool] = None
    ephemeral_environment_email: Optional[bool] = None
    marketing_email: Optional[bool] = None
    subprocessor_updates_email: Optional[bool] = None
    template_queue_email: Optional[bool] = None
    token: Optional[str] = None
    usage_email: Optional[bool] = None


class PrivateNetworkCreateOrGetInput(_Base):
    environment_id: str
    name: str
    project_id: str
    tags: list[str]


class PrivateNetworkEndpointCreateOrGetInput(_Base):
    environment_id: str
    private_network_id: str
    service_id: str
    service_name: str
    tags: list[str]


class ProjectCreateInput(_Base):
    default_environment_name: Optional[str] = None
    description: Optional[str] = None
    is_monorepo: Optional[bool] = None
    is_public: Optional[bool] = None
    name: Optional[str] = None
    pr_deploys: Optional[bool] = None
    repo: Optional["ProjectCreateRepo"] = None
    runtime: Optional["PublicRuntime"] = None
    workspace_id: Optional[str] = None


class ProjectCreateRepo(_Base):
    branch: str
    full_repo_name: str


class ProjectFeatureFlagToggleInput(_Base):
    flag: "ActiveProjectFeatureFlag"
    project_id: str


class ProjectInviteUserInput(_Base):
    email: str
    link: str


class ProjectInvitee(_Base):
    email: str
    role: "ProjectRole"


class ProjectMemberAddInput(_Base):
    project_id: str
    role: "ProjectRole"
    user_id: str


class ProjectMemberRemoveInput(_Base):
    project_id: str
    user_id: str


class ProjectMemberUpdateInput(_Base):
    project_id: str
    role: "ProjectRole"
    user_id: str


class ProjectTokenCreateInput(_Base):
    environment_id: str
    name: str
    project_id: str


class ProjectTransferConfirmInput(_Base):
    ownership_transfer_id: str
    project_id: str
    destination_workspace_id: Optional[str] = None


class ProjectTransferInitiateInput(_Base):
    member_id: str
    project_id: str


class ProjectTransferInput(_Base):
    workspace_id: str


class ProjectTransferToTeamInput(_Base):
    team_id: str


class ProjectUpdateInput(_Base):
    base_environment_id: Optional[str] = None
    bot_pr_environments: Optional[bool] = None
    description: Optional[str] = None
    focused_pr_environments: Optional[bool] = None
    is_public: Optional[bool] = None
    name: Optional[str] = None
    pr_deploys: Optional[bool] = None


class RecoveryCodeValidateInput(_Base):
    code: str
    two_factor_linking_key: Optional[str] = None


class ReferralInfoUpdateInput(_Base):
    code: str
    workspace_id: str


class RegistryCredentialsInput(_Base):
    """Private Docker registry credentials. Only available for Pro plan deployments."""
    password: str
    username: str


class ResetPluginCredentialsInput(_Base):
    environment_id: str


class ResetPluginInput(_Base):
    environment_id: str


class ServiceConnectInput(_Base):
    branch: Optional[str] = None
    image: Optional[str] = None
    repo: Optional[str] = None


class ServiceCreateInput(_Base):
    project_id: str
    branch: Optional[str] = None
    environment_id: Optional[str] = None
    icon: Optional[str] = None
    name: Optional[str] = None
    registry_credentials: Optional["RegistryCredentialsInput"] = None
    source: Optional["ServiceSourceInput"] = None
    template_id: Optional[str] = None
    template_service_id: Optional[str] = None
    variables: Optional[Any] = None


class ServiceDomainCreateInput(_Base):
    environment_id: str
    service_id: str
    target_port: Optional[int] = None


class ServiceDomainUpdateInput(_Base):
    domain: str
    environment_id: str
    service_domain_id: str
    service_id: str
    target_port: Optional[int] = None


class ServiceFeatureFlagToggleInput(_Base):
    flag: "ActiveServiceFeatureFlag"
    service_id: str


class ServiceInstanceLimitsUpdateInput(_Base):
    environment_id: str
    service_id: str
    memory_gb: Optional[float] = None
    v_cp_us: Optional[float] = None


class ServiceInstanceUpdateInput(_Base):
    build_command: Optional[str] = None
    builder: Optional["Builder"] = None
    cron_schedule: Optional[str] = None
    dockerfile_path: Optional[str] = None
    draining_seconds: Optional[int] = None
    healthcheck_path: Optional[str] = None
    healthcheck_timeout: Optional[int] = None
    ipv6_egress_enabled: Optional[bool] = None
    multi_region_config: Optional[Any] = None
    nixpacks_plan: Optional[Any] = None
    num_replicas: Optional[int] = None
    overlap_seconds: Optional[int] = None
    pre_deploy_command: Optional[list[str]] = None
    railway_config_file: Optional[str] = None
    region: Optional[str] = None
    registry_credentials: Optional["RegistryCredentialsInput"] = None
    restart_policy_max_retries: Optional[int] = None
    restart_policy_type: Optional["RestartPolicyType"] = None
    root_directory: Optional[str] = None
    sleep_application: Optional[bool] = None
    source: Optional["ServiceSourceInput"] = None
    start_command: Optional[str] = None
    watch_patterns: Optional[list[str]] = None


class ServiceSourceInput(_Base):
    image: Optional[str] = None
    repo: Optional[str] = None


class ServiceUpdateInput(_Base):
    icon: Optional[str] = None
    name: Optional[str] = None


class SharedVariableConfigureInput(_Base):
    disabled_service_ids: list[str]
    enabled_service_ids: list[str]
    environment_id: str
    name: str
    project_id: str


class SshPublicKeyCreateInput(_Base):
    name: str
    public_key: str


class TCPProxyCreateInput(_Base):
    application_port: int
    environment_id: str
    service_id: str


class TemplateCloneInput(_Base):
    code: str
    workspace_id: Optional[str] = None


class TemplateDeleteInput(_Base):
    workspace_id: Optional[str] = None


class TemplateDeployInput(_Base):
    services: list["TemplateDeployService"]
    environment_id: Optional[str] = None
    project_id: Optional[str] = None
    template_code: Optional[str] = None
    workspace_id: Optional[str] = None


class TemplateDeployService(_Base):
    id: str
    service_name: str
    template: str
    commit: Optional[str] = None
    has_domain: Optional[bool] = None
    healthcheck_path: Optional[str] = None
    is_private: Optional[bool] = None
    name: Optional[str] = None
    owner: Optional[str] = None
    pre_deploy_command: Optional[list[str]] = None
    root_directory: Optional[str] = None
    service_icon: Optional[str] = None
    start_command: Optional[str] = None
    tcp_proxy_application_port: Optional[int] = None
    variables: Optional[Any] = None
    volumes: Optional[list[Any]] = None


class TemplateDeployV2Input(_Base):
    serialized_config: Any
    template_id: str
    environment_id: Optional[str] = None
    project_id: Optional[str] = None
    workspace_id: Optional[str] = None


class TemplateGenerateInput(_Base):
    project_id: str
    environment_id: Optional[str] = None


class TemplatePublishInput(_Base):
    category: str
    description: str
    readme: str
    demo_project_id: Optional[str] = None
    image: Optional[str] = None
    workspace_id: Optional[str] = None


class TemplateServiceSourceEjectInput(_Base):
    project_id: str
    repo_name: str
    repo_owner: str
    service_ids: list[str]
    upstream_url: str


class TwoFactorInfoCreateInput(_Base):
    token: str


class TwoFactorInfoValidateInput(_Base):
    token: str
    two_factor_linking_key: Optional[str] = None


class UpdateNotificationRuleInput(_Base):
    channel_configs: Optional[list[Any]] = None
    ephemeral_environments: Optional[bool] = None
    event_types: Optional[list[str]] = None
    severities: Optional[list["NotificationSeverity"]] = None


class UsageLimitRemoveInput(_Base):
    customer_id: str


class UsageLimitSetInput(_Base):
    customer_id: str
    soft_limit_dollars: int
    hard_limit_dollars: Optional[int] = None


class UserFlagsRemoveInput(_Base):
    flags: list["UserFlag"]
    user_id: Optional[str] = None


class UserFlagsSetInput(_Base):
    flags: list["UserFlag"]
    user_id: Optional[str] = None


class UserProfileUpdateInput(_Base):
    is_public: bool
    bio: Optional[str] = None
    website: Optional[str] = None


class VariableCollectionUpsertInput(_Base):
    environment_id: str
    project_id: str
    variables: Any
    replace: Optional[bool] = None
    service_id: Optional[str] = None
    skip_deploys: Optional[bool] = None


class VariableDeleteInput(_Base):
    environment_id: str
    name: str
    project_id: str
    service_id: Optional[str] = None


class VariableUpsertInput(_Base):
    environment_id: str
    name: str
    project_id: str
    value: str
    service_id: Optional[str] = None
    skip_deploys: Optional[bool] = None


class VolumeCreateInput(_Base):
    mount_path: str
    project_id: str
    environment_id: Optional[str] = None
    region: Optional[str] = None
    service_id: Optional[str] = None


class VolumeInstanceUpdateInput(_Base):
    mount_path: Optional[str] = None
    service_id: Optional[str] = None
    state: Optional["VolumeState"] = None


class VolumeUpdateInput(_Base):
    name: Optional[str] = None


class WorkspaceInviteCodeCreateInput(_Base):
    role: str


class WorkspacePermissionChangeInput(_Base):
    role: "TeamRole"
    user_id: str
    workspace_id: str


class WorkspacePolicyItemUpdateInput(_Base):
    enabled: bool
    policy: "WorkspacePolicyName"


class WorkspaceTrustedDomainCreateInput(_Base):
    domain_name: str
    role: str
    workspace_id: str


class WorkspaceUpdateInput(_Base):
    avatar: Optional[str] = None
    name: Optional[str] = None
    preferred_region: Optional[str] = None


class WorkspaceUserInviteInput(_Base):
    code: str
    email: str


class WorkspaceUserRemoveInput(_Base):
    user_id: str


class customerTogglePayoutsToCreditsInput(_Base):
    is_withdrawing_to_credits: bool

