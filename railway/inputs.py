from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .enums import *  # noqa: F401,F403

@dataclass
class ApiTokenCreateInput:
    name: str
    workspace_id: Optional[str] = None


@dataclass
class AuditLogFilterInput:
    end_date: Optional[str] = None
    environment_id: Optional[str] = None
    event_types: Optional[list[str]] = None
    project_id: Optional[str] = None
    start_date: Optional[str] = None


@dataclass
class BaseEnvironmentOverrideInput:
    base_environment_override_id: Optional[str] = None


@dataclass
class BucketCreateInput:
    project_id: str
    environment_id: Optional[str] = None
    name: Optional[str] = None


@dataclass
class BucketUpdateInput:
    name: str


@dataclass
class CliEventTrackInput:
    arch: str
    cli_version: str
    command: str
    duration_ms: int
    is_ci: bool
    os: str
    success: bool
    error_message: Optional[str] = None
    sub_command: Optional[str] = None


@dataclass
class CreateNotificationRuleInput:
    channel_configs: list["NotificationChannelConfig"]
    event_types: list[str]
    workspace_id: str
    ephemeral_environments: Optional[bool] = None
    project_id: Optional[str] = None
    severities: Optional[list["NotificationSeverity"]] = None


@dataclass
class CustomDomainCreateInput:
    domain: str
    environment_id: str
    project_id: str
    service_id: str
    target_port: Optional[int] = None


@dataclass
class DeploymentInstanceExecutionCreateInput:
    service_instance_id: str


@dataclass
class DeploymentInstanceExecutionInput:
    deployment_id: str


@dataclass
class DeploymentInstanceExecutionListInput:
    environment_id: str
    service_id: str


@dataclass
class DeploymentListInput:
    environment_id: Optional[str] = None
    include_deleted: Optional[bool] = None
    project_id: Optional[str] = None
    service_id: Optional[str] = None
    status: Optional["DeploymentStatusInput"] = None


@dataclass
class DeploymentStatusInput:
    in_: Optional[list["DeploymentStatus"]] = None
    not_in: Optional[list["DeploymentStatus"]] = None


@dataclass
class DeploymentTriggerCreateInput:
    branch: str
    environment_id: str
    project_id: str
    provider: str
    repository: str
    service_id: str
    check_suites: Optional[bool] = None
    root_directory: Optional[str] = None


@dataclass
class DeploymentTriggerUpdateInput:
    branch: Optional[str] = None
    check_suites: Optional[bool] = None
    repository: Optional[str] = None
    root_directory: Optional[str] = None


@dataclass
class EgressGatewayCreateInput:
    environment_id: str
    service_id: str
    region: Optional[str] = None


@dataclass
class EgressGatewayServiceTargetInput:
    environment_id: str
    service_id: str


@dataclass
class EnvironmentCreateInput:
    name: str
    project_id: str
    apply_changes_in_background: Optional[bool] = None
    ephemeral: Optional[bool] = None
    skip_initial_deploys: Optional[bool] = None
    source_environment_id: Optional[str] = None
    stage_initial_changes: Optional[bool] = None


@dataclass
class EnvironmentRenameInput:
    name: str


@dataclass
class EnvironmentTriggersDeployInput:
    environment_id: str
    project_id: str
    service_id: str


@dataclass
class EventFilterInput:
    action: Optional["EventStringListFilter"] = None
    object: Optional["EventStringListFilter"] = None
    service_id: Optional["EventStringListFilter"] = None


@dataclass
class EventStringListFilter:
    in_: Optional[list[str]] = None
    not_in: Optional[list[str]] = None


@dataclass
class ExplicitOwnerInput:
    id: str
    type: Optional["ResourceOwnerType"] = None


@dataclass
class FeatureFlagToggleInput:
    flag: "ActiveFeatureFlag"


@dataclass
class GitHubRepoDeployInput:
    project_id: str
    repo: str
    branch: Optional[str] = None
    environment_id: Optional[str] = None


@dataclass
class GitHubRepoUpdateInput:
    environment_id: str
    project_id: str
    service_id: str


@dataclass
class HerokuImportVariablesInput:
    environment_id: str
    heroku_app_id: str
    project_id: str
    service_id: str


@dataclass
class IntegrationCreateInput:
    config: Any
    name: str
    project_id: str
    integration_auth_id: Optional[str] = None


@dataclass
class IntegrationUpdateInput:
    config: Any
    name: str
    project_id: str
    integration_auth_id: Optional[str] = None


@dataclass
class JobApplicationCreateInput:
    email: str
    job_id: str
    name: str
    why: str


@dataclass
class LoginSessionAuthInput:
    code: str
    hostname: Optional[str] = None


@dataclass
class NotificationDeliveryFilterInput:
    environment_id: Optional[str] = None
    only_unread: Optional[bool] = None
    project_id: Optional[str] = None
    status: Optional["NotificationStatus"] = None
    type: Optional["NotificationDeliveryType"] = None
    workspace_id: Optional[str] = None


@dataclass
class ObservabilityDashboardCreateInput:
    environment_id: str
    items: Optional[list["ObservabilityDashboardUpdateInput"]] = None


@dataclass
class ObservabilityDashboardItemConfigInput:
    logs_filter: Optional[str] = None
    measurements: Optional[list["MetricMeasurement"]] = None
    project_usage_properties: Optional[list["ProjectUsageProperty"]] = None
    resource_ids: Optional[list[str]] = None


@dataclass
class ObservabilityDashboardItemCreateInput:
    config: "ObservabilityDashboardItemConfigInput"
    id: str
    name: str
    type: "ObservabilityDashboardItemType"
    description: Optional[str] = None


@dataclass
class ObservabilityDashboardUpdateInput:
    dashboard_item: "ObservabilityDashboardItemCreateInput"
    display_config: "DisplayConfig"
    id: str


@dataclass
class PluginCreateInput:
    name: str
    project_id: str
    environment_id: Optional[str] = None
    friendly_name: Optional[str] = None


@dataclass
class PluginRestartInput:
    environment_id: Optional[str] = None


@dataclass
class PluginUpdateInput:
    friendly_name: str


@dataclass
class PreferencesUpdateData:
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


@dataclass
class PrivateNetworkCreateOrGetInput:
    environment_id: str
    name: str
    project_id: str
    tags: list[str]


@dataclass
class PrivateNetworkEndpointCreateOrGetInput:
    environment_id: str
    private_network_id: str
    service_id: str
    service_name: str
    tags: list[str]


@dataclass
class ProjectCreateInput:
    default_environment_name: Optional[str] = None
    description: Optional[str] = None
    is_monorepo: Optional[bool] = None
    is_public: Optional[bool] = None
    name: Optional[str] = None
    pr_deploys: Optional[bool] = None
    repo: Optional["ProjectCreateRepo"] = None
    runtime: Optional["PublicRuntime"] = None
    workspace_id: Optional[str] = None


@dataclass
class ProjectCreateRepo:
    branch: str
    full_repo_name: str


@dataclass
class ProjectFeatureFlagToggleInput:
    flag: "ActiveProjectFeatureFlag"
    project_id: str


@dataclass
class ProjectInviteUserInput:
    email: str
    link: str


@dataclass
class ProjectInvitee:
    email: str
    role: "ProjectRole"


@dataclass
class ProjectMemberAddInput:
    project_id: str
    role: "ProjectRole"
    user_id: str


@dataclass
class ProjectMemberRemoveInput:
    project_id: str
    user_id: str


@dataclass
class ProjectMemberUpdateInput:
    project_id: str
    role: "ProjectRole"
    user_id: str


@dataclass
class ProjectTokenCreateInput:
    environment_id: str
    name: str
    project_id: str


@dataclass
class ProjectTransferConfirmInput:
    ownership_transfer_id: str
    project_id: str
    destination_workspace_id: Optional[str] = None


@dataclass
class ProjectTransferInitiateInput:
    member_id: str
    project_id: str


@dataclass
class ProjectTransferInput:
    workspace_id: str


@dataclass
class ProjectTransferToTeamInput:
    team_id: str


@dataclass
class ProjectUpdateInput:
    base_environment_id: Optional[str] = None
    bot_pr_environments: Optional[bool] = None
    description: Optional[str] = None
    focused_pr_environments: Optional[bool] = None
    is_public: Optional[bool] = None
    name: Optional[str] = None
    pr_deploys: Optional[bool] = None


@dataclass
class RecoveryCodeValidateInput:
    code: str
    two_factor_linking_key: Optional[str] = None


@dataclass
class ReferralInfoUpdateInput:
    code: str
    workspace_id: str


@dataclass
class RegistryCredentialsInput:
    """Private Docker registry credentials. Only available for Pro plan deployments."""
    password: str
    username: str


@dataclass
class ResetPluginCredentialsInput:
    environment_id: str


@dataclass
class ResetPluginInput:
    environment_id: str


@dataclass
class ServiceConnectInput:
    branch: Optional[str] = None
    image: Optional[str] = None
    repo: Optional[str] = None


@dataclass
class ServiceCreateInput:
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


@dataclass
class ServiceDomainCreateInput:
    environment_id: str
    service_id: str
    target_port: Optional[int] = None


@dataclass
class ServiceDomainUpdateInput:
    domain: str
    environment_id: str
    service_domain_id: str
    service_id: str
    target_port: Optional[int] = None


@dataclass
class ServiceFeatureFlagToggleInput:
    flag: "ActiveServiceFeatureFlag"
    service_id: str


@dataclass
class ServiceInstanceLimitsUpdateInput:
    environment_id: str
    service_id: str
    memory_gb: Optional[float] = None
    v_cp_us: Optional[float] = None


@dataclass
class ServiceInstanceUpdateInput:
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


@dataclass
class ServiceSourceInput:
    image: Optional[str] = None
    repo: Optional[str] = None


@dataclass
class ServiceUpdateInput:
    icon: Optional[str] = None
    name: Optional[str] = None


@dataclass
class SharedVariableConfigureInput:
    disabled_service_ids: list[str]
    enabled_service_ids: list[str]
    environment_id: str
    name: str
    project_id: str


@dataclass
class SshPublicKeyCreateInput:
    name: str
    public_key: str


@dataclass
class TCPProxyCreateInput:
    application_port: int
    environment_id: str
    service_id: str


@dataclass
class TemplateCloneInput:
    code: str
    workspace_id: Optional[str] = None


@dataclass
class TemplateDeleteInput:
    workspace_id: Optional[str] = None


@dataclass
class TemplateDeployInput:
    services: list["TemplateDeployService"]
    environment_id: Optional[str] = None
    project_id: Optional[str] = None
    template_code: Optional[str] = None
    workspace_id: Optional[str] = None


@dataclass
class TemplateDeployService:
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
    volumes: Optional[list["TemplateVolume"]] = None


@dataclass
class TemplateDeployV2Input:
    serialized_config: "SerializedTemplateConfig"
    template_id: str
    environment_id: Optional[str] = None
    project_id: Optional[str] = None
    workspace_id: Optional[str] = None


@dataclass
class TemplateGenerateInput:
    project_id: str
    environment_id: Optional[str] = None


@dataclass
class TemplatePublishInput:
    category: str
    description: str
    readme: str
    demo_project_id: Optional[str] = None
    image: Optional[str] = None
    workspace_id: Optional[str] = None


@dataclass
class TemplateServiceSourceEjectInput:
    project_id: str
    repo_name: str
    repo_owner: str
    service_ids: list[str]
    upstream_url: str


@dataclass
class TwoFactorInfoCreateInput:
    token: str


@dataclass
class TwoFactorInfoValidateInput:
    token: str
    two_factor_linking_key: Optional[str] = None


@dataclass
class UpdateNotificationRuleInput:
    channel_configs: Optional[list["NotificationChannelConfig"]] = None
    ephemeral_environments: Optional[bool] = None
    event_types: Optional[list[str]] = None
    severities: Optional[list["NotificationSeverity"]] = None


@dataclass
class UsageLimitRemoveInput:
    customer_id: str


@dataclass
class UsageLimitSetInput:
    customer_id: str
    soft_limit_dollars: int
    hard_limit_dollars: Optional[int] = None


@dataclass
class UserFlagsRemoveInput:
    flags: list["UserFlag"]
    user_id: Optional[str] = None


@dataclass
class UserFlagsSetInput:
    flags: list["UserFlag"]
    user_id: Optional[str] = None


@dataclass
class UserProfileUpdateInput:
    is_public: bool
    bio: Optional[str] = None
    website: Optional[str] = None


@dataclass
class VariableCollectionUpsertInput:
    environment_id: str
    project_id: str
    variables: Any
    replace: Optional[bool] = None
    service_id: Optional[str] = None
    skip_deploys: Optional[bool] = None


@dataclass
class VariableDeleteInput:
    environment_id: str
    name: str
    project_id: str
    service_id: Optional[str] = None


@dataclass
class VariableUpsertInput:
    environment_id: str
    name: str
    project_id: str
    value: str
    service_id: Optional[str] = None
    skip_deploys: Optional[bool] = None


@dataclass
class VolumeCreateInput:
    mount_path: str
    project_id: str
    environment_id: Optional[str] = None
    region: Optional[str] = None
    service_id: Optional[str] = None


@dataclass
class VolumeInstanceUpdateInput:
    mount_path: Optional[str] = None
    service_id: Optional[str] = None
    state: Optional["VolumeState"] = None


@dataclass
class VolumeUpdateInput:
    name: Optional[str] = None


@dataclass
class WorkspaceInviteCodeCreateInput:
    role: str


@dataclass
class WorkspacePermissionChangeInput:
    role: "TeamRole"
    user_id: str
    workspace_id: str


@dataclass
class WorkspacePolicyItemUpdateInput:
    enabled: bool
    policy: "WorkspacePolicyName"


@dataclass
class WorkspaceTrustedDomainCreateInput:
    domain_name: str
    role: str
    workspace_id: str


@dataclass
class WorkspaceUpdateInput:
    avatar: Optional[str] = None
    name: Optional[str] = None
    preferred_region: Optional[str] = None


@dataclass
class WorkspaceUserInviteInput:
    code: str
    email: str


@dataclass
class WorkspaceUserRemoveInput:
    user_id: str


@dataclass
class customerTogglePayoutsToCreditsInput:
    is_withdrawing_to_credits: bool

