from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from .enums import *  # noqa: F401,F403

@dataclass
class AccessRule:
    disallowed: Optional[str] = None


@dataclass
class AdoptionInfo:
    created_at: str
    id: str
    num_config_file: int
    num_cron_schedule: int
    num_deploys: int
    num_envs: int
    num_failed_deploys: int
    num_healthcheck: int
    num_icon_config: int
    num_region: int
    num_replicas: int
    num_root_directory: int
    num_seats: int
    num_services: int
    num_variables: int
    num_watch_patterns: int
    updated_at: str
    workspace: "Workspace"
    adoption_level: Optional[float] = None
    delta_level: Optional[float] = None
    matched_icp_email: Optional[str] = None
    monthly_estimated_usage: Optional[float] = None
    total_cores: Optional[float] = None
    total_disk: Optional[float] = None
    total_network: Optional[float] = None


@dataclass
class AggregatedUsage:
    """The aggregated usage of a single measurement."""
    measurement: "MetricMeasurement"
    tags: "MetricTags"
    value: float


@dataclass
class AllDomains:
    custom_domains: list["CustomDomain"]
    service_domains: list["ServiceDomain"]


@dataclass
class ApiToken:
    display_token: str
    id: str
    name: str
    workspace_id: Optional[str] = None


@dataclass
class ApiTokenContext:
    """Information about the current API token and its accessible workspaces."""
    workspaces: list["ApiTokenWorkspace"]


@dataclass
class ApiTokenRateLimit:
    remaining_points: int
    resets_at: str


@dataclass
class ApiTokenWorkspace:
    id: str
    name: str


@dataclass
class AppliedByMember:
    email: str
    id: str
    avatar: Optional[str] = None
    name: Optional[str] = None
    username: Optional[str] = None


@dataclass
class AuditLog:
    created_at: str
    event_type: str
    id: str
    context: Optional[Any] = None
    environment: Optional["Environment"] = None
    environment_id: Optional[str] = None
    payload: Optional[Any] = None
    project: Optional["Project"] = None
    project_id: Optional[str] = None
    workspace_id: Optional[str] = None


@dataclass
class AuditLogEventTypeInfo:
    description: str
    event_type: str


@dataclass
class BillingPeriod:
    """The billing period for a customers subscription."""
    end: str
    start: str


@dataclass
class Bucket:
    created_at: str
    id: str
    name: str
    project: "Project"
    project_id: str
    updated_at: str


@dataclass
class BucketInstanceDetails:
    object_count: int
    size_bytes: int


@dataclass
class BucketS3CompatibleCredentials:
    access_key_id: str
    bucket_name: str
    created_at: str
    endpoint: str
    region: str
    secret_access_key: str
    url_style: str


@dataclass
class CanvasViewMergePreview:
    mutations: list[Any]
    state: Any


@dataclass
class CertificatePublicData:
    domain_names: list[str]
    fingerprint_sha256: str
    key_type: "KeyType"
    expires_at: Optional[str] = None
    issued_at: Optional[str] = None


@dataclass
class CnameCheck:
    message: str
    status: "CnameCheckStatus"
    link: Optional[str] = None


@dataclass
class ComplianceAgreementsInfo:
    has_baa: bool
    has_dpa: bool


@dataclass
class Container:
    created_at: str
    environment: "Environment"
    environment_id: str
    id: str
    plugin: "Plugin"
    plugin_id: str
    deleted_at: Optional[str] = None
    migrated_at: Optional[str] = None


@dataclass
class Credit:
    amount: float
    created_at: str
    customer_id: str
    id: str
    type: "CreditType"
    updated_at: str
    memo: Optional[str] = None


@dataclass
class CustomDomain:
    domain: str
    environment_id: str
    id: str
    service_id: str
    status: "CustomDomainStatus"
    sync_status: "CustomDomainSyncStatus"
    cdn_mode: Optional[str] = None
    created_at: Optional[str] = None
    deleted_at: Optional[str] = None
    edge_id: Optional[str] = None
    project_id: Optional[str] = None
    target_port: Optional[int] = None
    updated_at: Optional[str] = None


@dataclass
class CustomDomainStatus:
    certificate_status: "CertificateStatus"
    dns_records: list["DNSRecords"]
    verified: bool
    cdn_provider: Optional["CDNProvider"] = None
    certificate_error_message: Optional[str] = None
    certificate_error_type: Optional["CertificateErrorType"] = None
    certificate_retryable: Optional[bool] = None
    certificate_status_detailed: Optional["CertificateStatusDetailed"] = None
    certificates: Optional[list["CertificatePublicData"]] = None
    verification_dns_host: Optional[str] = None
    verification_token: Optional[str] = None


@dataclass
class Customer:
    applied_credits: float
    billing_period: "BillingPeriod"
    credit_balance: float
    current_usage: float
    has_exhausted_free_plan: bool
    id: str
    invoices: list["CustomerInvoice"]
    is_prepaying: bool
    is_trialing: bool
    is_usage_subscriber: bool
    is_withdrawing_to_credits: bool
    remaining_usage_credit_balance: float
    state: "SubscriptionState"
    stripe_customer_id: str
    subscriptions: list["CustomerSubscription"]
    supported_withdrawal_platforms: list["WithdrawalPlatformTypes"]
    tax_ids: list["CustomerTaxId"]
    trial_days_remaining: int
    workspace: "Workspace"
    billing_address: Optional["CustomerAddress"] = None
    billing_email: Optional[str] = None
    credits: Optional["CustomerCreditsConnection"] = None
    default_payment_method: Optional["PaymentMethod"] = None
    default_payment_method_id: Optional[str] = None
    plan_limit_override: Optional["PlanLimitOverride"] = None
    spend_commitment: Optional["SpendCommitment"] = None
    usage_limit: Optional["UsageLimit"] = None


@dataclass
class CustomerAddress:
    city: Optional[str] = None
    country: Optional[str] = None
    line1: Optional[str] = None
    line2: Optional[str] = None
    name: Optional[str] = None
    postal_code: Optional[str] = None
    state: Optional[str] = None


@dataclass
class CustomerCreditsConnection:
    edges: list["CustomerCreditsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class CustomerCreditsConnectionEdge:
    cursor: str
    node: "Credit"


@dataclass
class CustomerInvoice:
    amount_due: float
    amount_paid: float
    invoice_id: str
    items: list["SubscriptionItem"]
    period_end: str
    period_start: str
    total: int
    hosted_url: Optional[str] = None
    last_payment_error: Optional[str] = None
    payment_intent_status: Optional[str] = None
    pdf_url: Optional[str] = None
    reissued_invoice_from: Optional[str] = None
    reissued_invoice_of: Optional[str] = None
    spend_commitment_prepayment: Optional[bool] = None
    status: Optional[str] = None
    subscription_id: Optional[str] = None
    subscription_status: Optional[str] = None


@dataclass
class CustomerSubscription:
    billing_cycle_anchor: str
    cancel_at_period_end: bool
    discounts: list["SubscriptionDiscount"]
    id: str
    items: list["SubscriptionItem"]
    latest_invoice_id: str
    next_invoice_current_total: int
    next_invoice_date: str
    status: str
    cancel_at: Optional[str] = None
    coupon_id: Optional[str] = None


@dataclass
class CustomerTaxId:
    id: str
    type: str
    value: str


@dataclass
class DNSRecords:
    current_value: str
    fqdn: str
    hostlabel: str
    purpose: "DNSRecordPurpose"
    record_type: "DNSRecordType"
    required_value: str
    status: "DNSRecordStatus"
    zone: str


@dataclass
class Deployment:
    can_redeploy: bool
    can_rollback: bool
    created_at: str
    deployment_stopped: bool
    environment: "Environment"
    environment_id: str
    id: str
    instances: list["DeploymentDeploymentInstance"]
    project_id: str
    service: "Service"
    sockets: list["DeploymentSocket"]
    status: "DeploymentStatus"
    suggest_add_service_domain: bool
    updated_at: str
    creator: Optional["DeploymentCreator"] = None
    diagnosis: Optional["DeploymentDiagnosis"] = None
    meta: Optional["DeploymentMeta"] = None
    service_id: Optional[str] = None
    snapshot_id: Optional[str] = None
    static_url: Optional[str] = None
    status_updated_at: Optional[str] = None
    url: Optional[str] = None


@dataclass
class DeploymentCreator:
    email: str
    id: str
    avatar: Optional[str] = None
    name: Optional[str] = None


@dataclass
class DeploymentDeploymentInstance:
    id: str
    status: "DeploymentInstanceStatus"


@dataclass
class DeploymentEvent:
    created_at: str
    id: str
    step: "DeploymentEventStep"
    completed_at: Optional[str] = None
    payload: Optional["DeploymentEventPayload"] = None


@dataclass
class DeploymentEventPayload:
    error: Optional[str] = None


@dataclass
class DeploymentInstanceExecution:
    created_at: str
    deployment_id: str
    deployment_meta: "DeploymentMeta"
    id: str
    status: "DeploymentInstanceStatus"
    updated_at: str
    completed_at: Optional[str] = None


@dataclass
class DeploymentSnapshot:
    created_at: str
    id: str
    updated_at: str
    variables: Any


@dataclass
class DeploymentSocket:
    ipv6: bool
    port: int
    process_name: str
    updated_at: int


@dataclass
class DeploymentTrigger:
    branch: str
    check_suites: bool
    environment_id: str
    id: str
    project_id: str
    provider: str
    repository: str
    valid_check_suites: int
    base_environment_override_id: Optional[str] = None
    service_id: Optional[str] = None


@dataclass
class DockerComposeImport:
    errors: list[str]
    patch: Optional["EnvironmentConfig"] = None


@dataclass
class DomainAvailable:
    available: bool
    message: str


@dataclass
class DomainWithStatus:
    certificate_status: "CertificateStatus"
    dns_records: list["DNSRecords"]
    cdn_provider: Optional["CDNProvider"] = None
    certificate_error_message: Optional[str] = None
    certificate_error_type: Optional["CertificateErrorType"] = None
    certificate_retryable: Optional[bool] = None
    certificate_status_detailed: Optional["CertificateStatusDetailed"] = None
    certificates: Optional[list["CertificatePublicData"]] = None
    domain: Optional["Domain"] = None


@dataclass
class EgressGateway:
    ipv4: str
    region: str


@dataclass
class Environment:
    can_access: bool
    created_at: str
    id: str
    is_ephemeral: bool
    name: str
    project_id: str
    updated_at: str
    config: Optional["EnvironmentConfig"] = None
    deleted_at: Optional[str] = None
    deployment_triggers: Optional["EnvironmentDeploymentTriggersConnection"] = None
    deployments: Optional["EnvironmentDeploymentsConnection"] = None
    meta: Optional["EnvironmentMeta"] = None
    service_instances: Optional["EnvironmentServiceInstancesConnection"] = None
    source_environment: Optional["Environment"] = None
    unmerged_changes_count: Optional[int] = None
    variables: Optional["EnvironmentVariablesConnection"] = None
    volume_instances: Optional["EnvironmentVolumeInstancesConnection"] = None


@dataclass
class EnvironmentDeploymentTriggersConnection:
    edges: list["EnvironmentDeploymentTriggersConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class EnvironmentDeploymentTriggersConnectionEdge:
    cursor: str
    node: "DeploymentTrigger"


@dataclass
class EnvironmentDeploymentsConnection:
    edges: list["EnvironmentDeploymentsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class EnvironmentDeploymentsConnectionEdge:
    cursor: str
    node: "Deployment"


@dataclass
class EnvironmentMeta:
    base_branch: Optional[str] = None
    branch: Optional[str] = None
    latest_successful_git_hub_deployment_id: Optional[int] = None
    pr_comment_id: Optional[int] = None
    pr_number: Optional[int] = None
    pr_repo: Optional[str] = None
    pr_title: Optional[str] = None
    skipped_resource_ids: Optional["SkippedResourceIds"] = None


@dataclass
class EnvironmentPatch:
    created_at: str
    environment: "Environment"
    environment_id: str
    id: str
    status: "EnvironmentPatchStatus"
    updated_at: str
    applied_at: Optional[str] = None
    applied_by: Optional["AppliedByMember"] = None
    last_applied_error: Optional[str] = None
    message: Optional[str] = None
    patch: Optional["EnvironmentConfig"] = None


@dataclass
class EnvironmentServiceInstancesConnection:
    edges: list["EnvironmentServiceInstancesConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class EnvironmentServiceInstancesConnectionEdge:
    cursor: str
    node: "ServiceInstance"


@dataclass
class EnvironmentVariablesConnection:
    edges: list["EnvironmentVariablesConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class EnvironmentVariablesConnectionEdge:
    cursor: str
    node: "Variable"


@dataclass
class EnvironmentVolumeInstancesConnection:
    edges: list["EnvironmentVolumeInstancesConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class EnvironmentVolumeInstancesConnectionEdge:
    cursor: str
    node: "VolumeInstance"


@dataclass
class EstimatedUsage:
    """The estimated usage of a single measurement."""
    estimated_value: float
    measurement: "MetricMeasurement"
    project_id: str


@dataclass
class Event:
    action: str
    created_at: str
    id: str
    object: str
    project: "Project"
    severity: "EventSeverity"
    environment: Optional["Environment"] = None
    environment_id: Optional[str] = None
    payload: Optional[Any] = None
    project_id: Optional[str] = None


@dataclass
class ExternalWorkspace:
    created_at: str
    customer_state: "SubscriptionState"
    has2_fa_enforcement: bool
    has_baa: bool
    has_guardrails_access: bool
    has_rbac: bool
    has_saml: bool
    id: str
    name: str
    plan: "Plan"
    projects: list["Project"]
    redacted_due_to2_fa_pending: bool
    allow_deprecated_regions: Optional[bool] = None
    avatar: Optional[str] = None
    ban_reason: Optional[str] = None
    current_session_has_access: Optional[bool] = None
    customer_id: Optional[str] = None
    discord_role: Optional[str] = None
    is_trialing: Optional[bool] = None
    preferred_region: Optional[str] = None
    subscription_plan_limit: Optional[Any] = None
    support_tier_override: Optional[str] = None
    team_id: Optional[str] = None


@dataclass
class FunctionRuntime:
    image: str
    latest_version: "FunctionRuntimeVersion"
    name: "FunctionRuntimeName"
    versions: list["FunctionRuntimeVersion"]


@dataclass
class FunctionRuntimeVersion:
    image: str
    tag: str


@dataclass
class GitHubAccess:
    has_access: bool
    is_public: bool


@dataclass
class GitHubBranch:
    name: str


@dataclass
class GitHubCheck:
    name: str
    status: str


@dataclass
class GitHubPRInfo:
    additions: int
    author: str
    body: str
    changed_files: int
    checks: list["GitHubCheck"]
    deletions: int
    state: str
    title: str
    mergeable: Optional[bool] = None


@dataclass
class GitHubRepo:
    default_branch: str
    full_name: str
    id: int
    installation_id: str
    is_private: bool
    name: str
    description: Optional[str] = None
    owner_avatar_url: Optional[str] = None


@dataclass
class GitHubRepoWithoutInstallation:
    default_branch: str
    full_name: str
    id: int
    is_private: bool
    name: str
    description: Optional[str] = None


@dataclass
class GitHubSshKey:
    """An SSH public key from GitHub."""
    id: int
    key: str
    title: str


@dataclass
class HerokuApp:
    id: str
    name: str


@dataclass
class HttpDurationMetricsResult:
    """The result of an HTTP duration metrics query."""
    samples: list["HttpDurationMetricsSample"]


@dataclass
class HttpDurationMetricsSample:
    """A single sample of HTTP duration metrics."""
    p50: float
    p90: float
    p95: float
    p99: float
    ts: int


@dataclass
class HttpLog:
    """The result of a http logs query."""
    client_ua: str
    deployment_id: str
    deployment_instance_id: str
    downstream_proto: str
    edge_region: str
    host: str
    http_status: int
    method: str
    path: str
    request_id: str
    response_details: str
    rx_bytes: int
    src_ip: str
    timestamp: str
    total_duration: int
    tx_bytes: int
    upstream_address: str
    upstream_errors: str
    upstream_proto: str
    upstream_rq_duration: int


@dataclass
class HttpMetricsByStatusResult:
    """HTTP metrics grouped by status code."""
    samples: list["HttpMetricsSample"]
    status_code: int


@dataclass
class HttpMetricsResult:
    """The result of an HTTP metrics query."""
    samples: list["HttpMetricsSample"]


@dataclass
class HttpMetricsSample:
    """A single sample of an HTTP metric."""
    ts: int
    value: float


@dataclass
class Incident:
    id: str
    message: str
    status: "IncidentStatus"
    url: str


@dataclass
class Integration:
    config: Any
    id: str
    name: str
    project_id: str


@dataclass
class IntegrationAuth:
    id: str
    provider: str
    provider_id: str
    integrations: Optional["IntegrationAuthIntegrationsConnection"] = None


@dataclass
class IntegrationAuthIntegrationsConnection:
    edges: list["IntegrationAuthIntegrationsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class IntegrationAuthIntegrationsConnectionEdge:
    cursor: str
    node: "Integration"


@dataclass
class InviteCode:
    code: str
    created_at: str
    id: str
    project: "Project"
    project_id: str
    role: "ProjectRole"


@dataclass
class Log:
    """The result of a logs query."""
    attributes: list["LogAttribute"]
    message: str
    timestamp: str
    severity: Optional[str] = None
    tags: Optional["LogTags"] = None


@dataclass
class LogAttribute:
    """The attributes associated with a structured log"""
    key: str
    value: str


@dataclass
class LogTags:
    """The tags associated with a specific log"""
    deployment_id: Optional[str] = None
    deployment_instance_id: Optional[str] = None
    environment_id: Optional[str] = None
    project_id: Optional[str] = None
    service_id: Optional[str] = None
    snapshot_id: Optional[str] = None


@dataclass
class Maintenance:
    id: str
    message: str
    start: str
    status: "MaintenanceStatus"
    url: str


@dataclass
class Metric:
    """A single sample of a metric."""
    ts: int
    value: float


@dataclass
class MetricTags:
    """The tags that were used to group the metric."""
    deployment_id: Optional[str] = None
    deployment_instance_id: Optional[str] = None
    environment_id: Optional[str] = None
    project_id: Optional[str] = None
    region: Optional[str] = None
    service_id: Optional[str] = None
    volume_id: Optional[str] = None
    volume_instance_id: Optional[str] = None


@dataclass
class MetricsResult:
    """The result of a metrics query."""
    measurement: "MetricMeasurement"
    tags: "MetricTags"
    values: list["Metric"]


@dataclass
class MonitorThresholdConfig:
    condition: "MonitorThresholdCondition"
    threshold: float
    type: str
    measurement: Optional["MetricMeasurement"] = None


@dataclass
class NotificationChannel:
    config: "NotificationChannelConfig"
    created_at: str
    id: str
    updated_at: str
    workspace_id: str


@dataclass
class NotificationDelivery:
    created_at: str
    id: str
    notification_instance: "NotificationInstance"
    status: "NotificationDeliveryStatus"
    type: "NotificationDeliveryType"
    updated_at: str
    read_at: Optional[str] = None
    user_id: Optional[str] = None


@dataclass
class NotificationDeliveryCreated:
    delivery: "NotificationDelivery"
    type: str


@dataclass
class NotificationDeliveryResolved:
    delivery_ids: list[str]
    type: str


@dataclass
class NotificationInstance:
    created_at: str
    event: "Event"
    event_id: str
    id: str
    payload: "NotificationPayload"
    severity: "NotificationSeverity"
    status: "NotificationStatus"
    updated_at: str
    workspace_id: str
    environment_id: Optional[str] = None
    event_type: Optional[str] = None
    project_id: Optional[str] = None
    resolved_at: Optional[str] = None
    resource_id: Optional[str] = None
    resource_type: Optional[str] = None
    service_id: Optional[str] = None
    volume_id: Optional[str] = None


@dataclass
class NotificationRule:
    channels: list["NotificationChannel"]
    created_at: str
    event_types: list[str]
    id: str
    severities: list["NotificationSeverity"]
    updated_at: str
    workspace_id: str
    environment_id: Optional[str] = None
    ephemeral_environments: Optional[bool] = None
    project_id: Optional[str] = None
    service_id: Optional[str] = None


@dataclass
class ObservabilityDashboard:
    id: str
    items: list["ObservabilityDashboardItemInstance"]


@dataclass
class ObservabilityDashboardAlert:
    created_at: str
    id: str
    resource_type: "MonitorAlertResourceType"
    status: "MonitorStatus"
    resolved_at: Optional[str] = None
    resource_id: Optional[str] = None


@dataclass
class ObservabilityDashboardItem:
    config: "ObservabilityDashboardItemConfig"
    id: str
    monitors: list["ObservabilityDashboardMonitor"]
    name: str
    type: "ObservabilityDashboardItemType"
    description: Optional[str] = None


@dataclass
class ObservabilityDashboardItemConfig:
    logs_filter: Optional[str] = None
    measurements: Optional[list["MetricMeasurement"]] = None
    project_usage_properties: Optional[list["ProjectUsageProperty"]] = None
    resource_ids: Optional[list[str]] = None


@dataclass
class ObservabilityDashboardItemInstance:
    dashboard_item: "ObservabilityDashboardItem"
    display_config: "DisplayConfig"
    id: str


@dataclass
class ObservabilityDashboardMonitor:
    config: "ObservabilityDashboardMonitorConfig"
    created_at: str
    id: str
    updated_at: str
    alerts: Optional[list["ObservabilityDashboardAlert"]] = None


@dataclass
class PageInfo:
    has_next_page: bool
    has_previous_page: bool
    end_cursor: Optional[str] = None
    start_cursor: Optional[str] = None


@dataclass
class PartnerProfile:
    category: str
    description: str
    slug: str
    type: "PartnerProfileType"
    website: str


@dataclass
class Passkey:
    backed_up: bool
    created_at: str
    credential_id: str
    device_name: str
    device_type: str
    id: str
    transports: list[str]
    updated_at: str
    aaguid: Optional[str] = None
    display_name: Optional[str] = None
    last_used_at: Optional[str] = None
    last_used_device: Optional[str] = None


@dataclass
class PaymentMethod:
    id: str
    card: Optional["PaymentMethodCard"] = None


@dataclass
class PaymentMethodCard:
    brand: str
    last4: str
    country: Optional[str] = None


@dataclass
class PlanLimitOverride:
    config: Any
    id: str


@dataclass
class PlatformFeatureFlagStatus:
    flag: "PlatformFeatureFlag"
    rollout_percentage: int
    status: bool
    type: "PlatformFeatureFlagType"


@dataclass
class PlatformStatus:
    is_stable: bool
    incident: Optional["Incident"] = None
    maintenance: Optional["Maintenance"] = None


@dataclass
class Plugin:
    created_at: str
    friendly_name: str
    id: str
    logs_enabled: bool
    name: "PluginType"
    project: "Project"
    status: "PluginStatus"
    containers: Optional["PluginContainersConnection"] = None
    deleted_at: Optional[str] = None
    deprecated_at: Optional[str] = None
    migration_database_service_id: Optional[str] = None
    variables: Optional["PluginVariablesConnection"] = None


@dataclass
class PluginContainersConnection:
    edges: list["PluginContainersConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class PluginContainersConnectionEdge:
    cursor: str
    node: "Container"


@dataclass
class PluginVariablesConnection:
    edges: list["PluginVariablesConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class PluginVariablesConnectionEdge:
    cursor: str
    node: "Variable"


@dataclass
class Preferences:
    build_failed_email: bool
    changelog_email: bool
    community_email: bool
    deploy_crashed_email: bool
    ephemeral_environment_email: bool
    id: str
    marketing_email: bool
    subprocessor_updates_email: bool
    template_queue_email: bool
    usage_email: bool


@dataclass
class PrivateNetwork:
    dns_name: str
    environment_id: str
    name: str
    network_id: int
    project_id: str
    public_id: str
    tags: list[str]
    created_at: Optional[str] = None
    deleted_at: Optional[str] = None


@dataclass
class PrivateNetworkEndpoint:
    dns_name: str
    private_ips: list[str]
    public_id: str
    service_instance_id: str
    sync_status: "PrivateNetworkEndpointSyncStatus"
    tags: list[str]
    created_at: Optional[str] = None
    deleted_at: Optional[str] = None
    new_dns_name: Optional[str] = None


@dataclass
class Project:
    bot_pr_environments: bool
    created_at: str
    feature_flags: list["ActiveProjectFeatureFlag"]
    focused_pr_environments: bool
    id: str
    is_public: bool
    is_temp_project: bool
    members: list["ProjectMember"]
    name: str
    pr_deploys: bool
    subscription_plan_limit: Any
    subscription_type: "SubscriptionPlanType"
    updated_at: str
    base_environment: Optional["Environment"] = None
    base_environment_id: Optional[str] = None
    buckets: Optional["ProjectBucketsConnection"] = None
    deleted_at: Optional[str] = None
    description: Optional[str] = None
    environments: Optional["ProjectEnvironmentsConnection"] = None
    expired_at: Optional[str] = None
    groups: Optional["ProjectGroupsConnection"] = None
    project_permissions: Optional["ProjectProjectPermissionsConnection"] = None
    services: Optional["ProjectServicesConnection"] = None
    volumes: Optional["ProjectVolumesConnection"] = None
    workspace: Optional["Workspace"] = None
    workspace_id: Optional[str] = None


@dataclass
class ProjectBucketsConnection:
    edges: list["ProjectBucketsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class ProjectBucketsConnectionEdge:
    cursor: str
    node: "Bucket"


@dataclass
class ProjectComplianceInfo:
    member_permissions: list["ProjectMemberPermissionsInfo"]
    project_id: str
    project_name: str
    service_backups: list["ServiceBackupInfo"]
    two_factor_members: list["ProjectMemberTwoFactorInfo"]
    workspace_id: str


@dataclass
class ProjectDeploymentTriggersConnection:
    edges: list["ProjectDeploymentTriggersConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class ProjectDeploymentTriggersConnectionEdge:
    cursor: str
    node: "DeploymentTrigger"


@dataclass
class ProjectDeploymentsConnection:
    edges: list["ProjectDeploymentsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class ProjectDeploymentsConnectionEdge:
    cursor: str
    node: "Deployment"


@dataclass
class ProjectEnvironmentsConnection:
    edges: list["ProjectEnvironmentsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class ProjectEnvironmentsConnectionEdge:
    cursor: str
    node: "Environment"


@dataclass
class ProjectGroupsConnection:
    edges: list["ProjectGroupsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class ProjectGroupsConnectionEdge:
    cursor: str


@dataclass
class ProjectInvitation:
    email: str
    expires_at: str
    id: str
    is_expired: bool
    project: "PublicProjectInformation"
    inviter: Optional["ProjectInvitationInviter"] = None


@dataclass
class ProjectInvitationInviter:
    email: str
    name: Optional[str] = None


@dataclass
class ProjectMember:
    email: str
    id: str
    role: "ProjectRole"
    avatar: Optional[str] = None
    name: Optional[str] = None


@dataclass
class ProjectMemberPermissionsInfo:
    email: str
    role: "ProjectRole"
    name: Optional[str] = None


@dataclass
class ProjectMemberTwoFactorInfo:
    email: str
    enabled_methods: list["TwoFactorMethodCompliance"]
    two_factor_auth_enabled: bool
    name: Optional[str] = None


@dataclass
class ProjectPermission:
    id: str
    project_id: str
    role: "ProjectRole"
    user_id: str


@dataclass
class ProjectPluginsConnection:
    edges: list["ProjectPluginsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class ProjectPluginsConnectionEdge:
    cursor: str
    node: "Plugin"


@dataclass
class ProjectProjectPermissionsConnection:
    edges: list["ProjectProjectPermissionsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class ProjectProjectPermissionsConnectionEdge:
    cursor: str
    node: "ProjectPermission"


@dataclass
class ProjectResourceAccess:
    custom_domain: "AccessRule"
    database_deployment: "AccessRule"
    deployment: "AccessRule"
    environment: "AccessRule"


@dataclass
class ProjectServicesConnection:
    edges: list["ProjectServicesConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class ProjectServicesConnectionEdge:
    cursor: str
    node: "Service"


@dataclass
class ProjectToken:
    created_at: str
    display_token: str
    environment: "Environment"
    environment_id: str
    id: str
    name: str
    project: "Project"
    project_id: str


@dataclass
class ProjectVolumesConnection:
    edges: list["ProjectVolumesConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class ProjectVolumesConnectionEdge:
    cursor: str
    node: "Volume"


@dataclass
class ProjectWorkspaceMember:
    email: str
    enabled_methods: list["TwoFactorMethodProjectWorkspace"]
    two_factor_auth_enabled: bool
    name: Optional[str] = None


@dataclass
class ProjectWorkspaceMembersResponse:
    members: list["ProjectWorkspaceMember"]
    project_id: str
    project_name: str
    workspace_id: str


@dataclass
class ProviderAuth:
    email: str
    id: str
    is_auth_enabled: bool
    metadata: Any
    provider: str
    user_id: str


@dataclass
class PublicProjectInformation:
    id: str
    name: str


@dataclass
class PublicStats:
    total_deployments_last_month: int
    total_logs_last_month: int
    total_projects: int
    total_requests_last_month: int
    total_services: int
    total_users: int


@dataclass
class QueryApiTokensConnection:
    edges: list["QueryApiTokensConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryApiTokensConnectionEdge:
    cursor: str
    node: "ApiToken"


@dataclass
class QueryAuditLogsConnection:
    edges: list["QueryAuditLogsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryAuditLogsConnectionEdge:
    cursor: str
    node: "AuditLog"


@dataclass
class QueryDeploymentEventsConnection:
    edges: list["QueryDeploymentEventsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryDeploymentEventsConnectionEdge:
    cursor: str
    node: "DeploymentEvent"


@dataclass
class QueryDeploymentInstanceExecutionsConnection:
    edges: list["QueryDeploymentInstanceExecutionsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryDeploymentInstanceExecutionsConnectionEdge:
    cursor: str
    node: "DeploymentInstanceExecution"


@dataclass
class QueryDeploymentTriggersConnection:
    edges: list["QueryDeploymentTriggersConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryDeploymentTriggersConnectionEdge:
    cursor: str
    node: "DeploymentTrigger"


@dataclass
class QueryDeploymentsConnection:
    edges: list["QueryDeploymentsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryDeploymentsConnectionEdge:
    cursor: str
    node: "Deployment"


@dataclass
class QueryEnvironmentPatchesConnection:
    edges: list["QueryEnvironmentPatchesConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryEnvironmentPatchesConnectionEdge:
    cursor: str
    node: "EnvironmentPatch"


@dataclass
class QueryEnvironmentsConnection:
    edges: list["QueryEnvironmentsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryEnvironmentsConnectionEdge:
    cursor: str
    node: "Environment"


@dataclass
class QueryEventsConnection:
    edges: list["QueryEventsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryEventsConnectionEdge:
    cursor: str
    node: "Event"


@dataclass
class QueryIntegrationAuthsConnection:
    edges: list["QueryIntegrationAuthsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryIntegrationAuthsConnectionEdge:
    cursor: str
    node: "IntegrationAuth"


@dataclass
class QueryIntegrationsConnection:
    edges: list["QueryIntegrationsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryIntegrationsConnectionEdge:
    cursor: str
    node: "Integration"


@dataclass
class QueryNotificationDeliveriesConnection:
    edges: list["QueryNotificationDeliveriesConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryNotificationDeliveriesConnectionEdge:
    cursor: str
    node: "NotificationDelivery"


@dataclass
class QueryObservabilityDashboardsConnection:
    edges: list["QueryObservabilityDashboardsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryObservabilityDashboardsConnectionEdge:
    cursor: str
    node: "ObservabilityDashboard"


@dataclass
class QueryPasskeysConnection:
    edges: list["QueryPasskeysConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryPasskeysConnectionEdge:
    cursor: str
    node: "Passkey"


@dataclass
class QueryProjectTokensConnection:
    edges: list["QueryProjectTokensConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryProjectTokensConnectionEdge:
    cursor: str
    node: "ProjectToken"


@dataclass
class QueryProjectsConnection:
    edges: list["QueryProjectsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryProjectsConnectionEdge:
    cursor: str
    node: "Project"


@dataclass
class QuerySessionsConnection:
    edges: list["QuerySessionsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QuerySessionsConnectionEdge:
    cursor: str
    node: "Session"


@dataclass
class QuerySshPublicKeysConnection:
    edges: list["QuerySshPublicKeysConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QuerySshPublicKeysConnectionEdge:
    cursor: str
    node: "SshPublicKey"


@dataclass
class QueryTeamTemplatesConnection:
    edges: list["QueryTeamTemplatesConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryTeamTemplatesConnectionEdge:
    cursor: str
    node: "Template"


@dataclass
class QueryTemplatesConnection:
    edges: list["QueryTemplatesConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryTemplatesConnectionEdge:
    cursor: str
    node: "Template"


@dataclass
class QueryTrustedDomainsConnection:
    edges: list["QueryTrustedDomainsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryTrustedDomainsConnectionEdge:
    cursor: str
    node: "TrustedDomain"


@dataclass
class QueryUserTemplatesConnection:
    edges: list["QueryUserTemplatesConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryUserTemplatesConnectionEdge:
    cursor: str
    node: "Template"


@dataclass
class QueryWorkspaceIdentityProvidersConnection:
    edges: list["QueryWorkspaceIdentityProvidersConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryWorkspaceIdentityProvidersConnectionEdge:
    cursor: str
    node: "WorkspaceIdentityProvider"


@dataclass
class QueryWorkspaceTemplatesConnection:
    edges: list["QueryWorkspaceTemplatesConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class QueryWorkspaceTemplatesConnectionEdge:
    cursor: str
    node: "Template"


@dataclass
class RecoveryCodes:
    recovery_codes: list[str]


@dataclass
class ReferralInfo:
    code: str
    id: str
    referral_stats: "ReferralStats"
    status: str


@dataclass
class ReferralStats:
    credited: int
    pending: int


@dataclass
class ReferralUser:
    code: str
    id: str
    status: "ReferralStatus"


@dataclass
class Region:
    country: str
    location: str
    name: str
    deployment_constraints: Optional["RegionDeploymentConstraints"] = None
    railway_metal: Optional[bool] = None
    region: Optional[str] = None
    workspace_id: Optional[str] = None


@dataclass
class RegionDeploymentConstraints:
    admin_only: Optional[bool] = None
    deprecation_info: Optional["RegionDeprecationInfo"] = None
    runtime_exclusivity: Optional[list[str]] = None
    staging_only: Optional[bool] = None


@dataclass
class RegionDeprecationInfo:
    is_deprecated: bool
    replacement_region: str


@dataclass
class ResourceAccess:
    deployment: "AccessRule"
    project: "AccessRule"


@dataclass
class Service:
    created_at: str
    feature_flags: list["ActiveServiceFeatureFlag"]
    has_hidden_registry_credentials_from_template: bool
    id: str
    name: str
    project: "Project"
    project_id: str
    updated_at: str
    deleted_at: Optional[str] = None
    icon: Optional[str] = None
    repo_triggers: Optional["ServiceRepoTriggersConnection"] = None
    template_id: Optional[str] = None
    template_service_id: Optional[str] = None
    template_thread_slug: Optional[str] = None


@dataclass
class ServiceBackupInfo:
    schedules: list["VolumeInstanceBackupScheduleKind"]
    service_id: str
    service_name: str


@dataclass
class ServiceDeploymentsConnection:
    edges: list["ServiceDeploymentsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class ServiceDeploymentsConnectionEdge:
    cursor: str
    node: "Deployment"


@dataclass
class ServiceDomain:
    domain: str
    environment_id: str
    id: str
    service_id: str
    sync_status: "ServiceDomainSyncStatus"
    cdn_mode: Optional[str] = None
    created_at: Optional[str] = None
    deleted_at: Optional[str] = None
    edge_id: Optional[str] = None
    new_domain_name: Optional[str] = None
    new_host_label: Optional[str] = None
    project_id: Optional[str] = None
    suffix: Optional[str] = None
    target_port: Optional[int] = None
    updated_at: Optional[str] = None


@dataclass
class ServiceInstance:
    active_deployments: list["Deployment"]
    builder: "Builder"
    created_at: str
    domains: "AllDomains"
    environment_id: str
    id: str
    is_updatable: bool
    restart_policy_max_retries: int
    restart_policy_type: "RestartPolicyType"
    service: "Service"
    service_id: str
    service_name: str
    updated_at: str
    watch_patterns: list[str]
    build_command: Optional[str] = None
    cron_schedule: Optional[str] = None
    deleted_at: Optional[str] = None
    dockerfile_path: Optional[str] = None
    draining_seconds: Optional[int] = None
    healthcheck_path: Optional[str] = None
    healthcheck_timeout: Optional[int] = None
    ipv6_egress_enabled: Optional[bool] = None
    latest_deployment: Optional["Deployment"] = None
    next_cron_run_at: Optional[str] = None
    nixpacks_plan: Optional[Any] = None
    num_replicas: Optional[int] = None
    overlap_seconds: Optional[int] = None
    pre_deploy_command: Optional[Any] = None
    railpack_info: Optional["RailpackInfo"] = None
    railway_config_file: Optional[str] = None
    region: Optional[str] = None
    root_directory: Optional[str] = None
    sleep_application: Optional[bool] = None
    source: Optional["ServiceSource"] = None
    start_command: Optional[str] = None
    upstream_url: Optional[str] = None


@dataclass
class ServiceRepoTriggersConnection:
    edges: list["ServiceRepoTriggersConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class ServiceRepoTriggersConnectionEdge:
    cursor: str
    node: "DeploymentTrigger"


@dataclass
class ServiceServiceInstancesConnection:
    edges: list["ServiceServiceInstancesConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class ServiceServiceInstancesConnectionEdge:
    cursor: str
    node: "ServiceInstance"


@dataclass
class ServiceSource:
    image: Optional[str] = None
    repo: Optional[str] = None


@dataclass
class Session:
    created_at: str
    expired_at: str
    id: str
    is_current: bool
    name: str
    type: "SessionType"
    updated_at: str


@dataclass
class SimilarTemplate:
    code: str
    created_at: str
    deploys: int
    name: str
    creator: Optional["TemplateCreator"] = None
    description: Optional[str] = None
    health: Optional[float] = None
    image: Optional[str] = None
    user_id: Optional[str] = None
    workspace_id: Optional[str] = None


@dataclass
class SpendCommitment:
    features: list["SpendCommitmentFeatureId"]
    id: str
    min_spend_amount_cents: int


@dataclass
class SshPublicKey:
    created_at: str
    fingerprint: str
    id: str
    name: str
    public_key: str
    updated_at: str


@dataclass
class SubscriptionDiscount:
    coupon_id: str
    coupon_name: str


@dataclass
class SubscriptionItem:
    item_id: str
    price_id: str
    product_id: str
    price_dollars: Optional[float] = None
    quantity: Optional[int] = None


@dataclass
class TCPProxy:
    application_port: int
    domain: str
    environment_id: str
    id: str
    proxy_port: int
    service_id: str
    sync_status: "TCPProxySyncStatus"
    created_at: Optional[str] = None
    deleted_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class Team:
    pass


@dataclass
class TeamMember:
    email: str
    id: str
    role: "TeamRole"
    avatar: Optional[str] = None
    feature_flags: Optional[list["ActiveFeatureFlag"]] = None
    name: Optional[str] = None


@dataclass
class TeamPermission:
    created_at: str
    id: str
    role: "TeamRole"
    updated_at: str
    user_id: str
    workspace_id: str


@dataclass
class TeamProjectsConnection:
    edges: list["TeamProjectsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class TeamProjectsConnectionEdge:
    cursor: str
    node: "Project"


@dataclass
class Template:
    active_projects: int
    code: str
    created_at: str
    id: str
    is_approved: bool
    is_v2_template: bool
    is_verified: bool
    name: str
    projects: int
    recent_projects: int
    similar_templates: list["SimilarTemplate"]
    status: "TemplateStatus"
    total_payout: float
    canvas_config: Optional[Any] = None
    category: Optional[str] = None
    community_thread_slug: Optional[str] = None
    creator: Optional["TemplateCreator"] = None
    demo_project_id: Optional[str] = None
    description: Optional[str] = None
    guides: Optional["TemplateGuide"] = None
    health: Optional[float] = None
    image: Optional[str] = None
    languages: Optional[list[str]] = None
    readme: Optional[str] = None
    serialized_config: Optional["SerializedTemplateConfig"] = None
    services: Optional["TemplateServicesConnection"] = None
    support_health_metrics: Optional["SupportHealthMetrics"] = None
    tags: Optional[list[str]] = None
    workspace_id: Optional[str] = None


@dataclass
class TemplateCreator:
    has_public_profile: bool
    avatar: Optional[str] = None
    name: Optional[str] = None
    username: Optional[str] = None


@dataclass
class TemplateDeployPayload:
    project_id: str
    workflow_id: Optional[str] = None


@dataclass
class TemplateGuide:
    post: Optional[str] = None
    video: Optional[str] = None


@dataclass
class TemplateMetrics:
    active_deployments: int
    deployments_last90_days: int
    earnings_last30_days: float
    earnings_last90_days: float
    eligible_for_support_bonus: bool
    support_health: float
    template_health: float
    total_deployments: int
    total_earnings: float


@dataclass
class TemplateService:
    config: "TemplateServiceConfig"
    created_at: str
    id: str
    template_id: str
    updated_at: str


@dataclass
class TemplateServicesConnection:
    edges: list["TemplateServicesConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class TemplateServicesConnectionEdge:
    cursor: str
    node: "TemplateService"


@dataclass
class TrustedDomain:
    domain_name: str
    id: str
    role: str
    status: "TrustedDomainStatus"
    verification_data: "TrustedDomainVerificationData"
    verification_type: str
    workspace_id: str


@dataclass
class TrustedDomainVerificationData:
    dns_host: Optional[str] = None
    domain_match: Optional["Domain"] = None
    domain_status: Optional["CustomDomainStatus"] = None
    token: Optional[str] = None


@dataclass
class TwoFactorInfo:
    has_recovery_codes: bool
    is_verified: bool


@dataclass
class TwoFactorInfoSecret:
    secret: str
    uri: str


@dataclass
class UsageLimit:
    customer_id: str
    id: str
    is_over_limit: bool
    soft_limit: int
    hard_limit: Optional[int] = None


@dataclass
class User:
    agreed_fair_use: bool
    created_at: str
    email: str
    feature_flags: list["ActiveFeatureFlag"]
    flags: list["UserFlag"]
    has2_fa: bool
    has_passkeys: bool
    id: str
    is_admin: bool
    is_conductor: bool
    is_verified: bool
    last_login: str
    platform_feature_flags: list["ActivePlatformFlag"]
    registration_status: "RegistrationStatus"
    workspaces: list["Workspace"]
    api_token_rate_limit: Optional["ApiTokenRateLimit"] = None
    avatar: Optional[str] = None
    ban_reason: Optional[str] = None
    github_provider_id: Optional[str] = None
    github_username: Optional[str] = None
    name: Optional[str] = None
    profile: Optional["UserProfile"] = None
    provider_auths: Optional["UserProviderAuthsConnection"] = None
    risk_level: Optional[float] = None
    terms_agreed_on: Optional[str] = None
    username: Optional[str] = None


@dataclass
class UserKickbackEarnings:
    total_amount: float


@dataclass
class UserProfile:
    is_public: bool
    bio: Optional[str] = None
    website: Optional[str] = None


@dataclass
class UserProfileResponse:
    created_at: str
    id: str
    profile: "UserProfile"
    total_deploys: int
    avatar: Optional[str] = None
    customer_id: Optional[str] = None
    is_trialing: Optional[bool] = None
    name: Optional[str] = None
    public_projects: Optional["UserProfileResponsePublicProjectsConnection"] = None
    state: Optional[str] = None
    username: Optional[str] = None


@dataclass
class UserProfileResponsePublicProjectsConnection:
    edges: list["UserProfileResponsePublicProjectsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class UserProfileResponsePublicProjectsConnectionEdge:
    cursor: str
    node: "Project"


@dataclass
class UserProjectsConnection:
    edges: list["UserProjectsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class UserProjectsConnectionEdge:
    cursor: str
    node: "Project"


@dataclass
class UserProviderAuthsConnection:
    edges: list["UserProviderAuthsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class UserProviderAuthsConnectionEdge:
    cursor: str
    node: "ProviderAuth"


@dataclass
class Variable:
    created_at: str
    environment: "Environment"
    id: str
    is_sealed: bool
    name: str
    plugin: "Plugin"
    references: list[str]
    service: "Service"
    updated_at: str
    environment_id: Optional[str] = None
    service_id: Optional[str] = None


@dataclass
class VercelAccount:
    id: str
    integration_auth_id: str
    is_user: bool
    projects: list["VercelProject"]
    name: Optional[str] = None
    slug: Optional[str] = None


@dataclass
class VercelInfo:
    accounts: list["VercelAccount"]


@dataclass
class VercelProject:
    account_id: str
    id: str
    name: str


@dataclass
class Volume:
    created_at: str
    id: str
    name: str
    project: "Project"
    project_id: str


@dataclass
class VolumeInstance:
    created_at: str
    current_size_mb: float
    environment: "Environment"
    environment_id: str
    id: str
    mount_path: str
    service: "Service"
    size_mb: int
    volume: "Volume"
    volume_id: str
    external_id: Optional[str] = None
    region: Optional[str] = None
    service_id: Optional[str] = None
    state: Optional["VolumeState"] = None


@dataclass
class VolumeInstanceBackup:
    created_at: str
    external_id: str
    id: str
    creator_id: Optional[str] = None
    expires_at: Optional[str] = None
    name: Optional[str] = None
    referenced_mb: Optional[int] = None
    schedule_id: Optional[str] = None
    used_mb: Optional[int] = None
    volume_instance_size_mb: Optional[int] = None


@dataclass
class VolumeInstanceBackupSchedule:
    created_at: str
    cron: str
    id: str
    kind: "VolumeInstanceBackupScheduleKind"
    name: str
    retention_seconds: Optional[int] = None


@dataclass
class VolumeInstanceReplicationProgress:
    bytes_transferred: int
    percent_complete: float
    timestamp: str
    transfer_rate_mbps: Optional[float] = None


@dataclass
class VolumeReplicationProgressUpdate:
    current_snapshot: "VolumeSnapshotReplicationProgressUpdate"
    dest_external_id: str
    history: list["VolumeInstanceReplicationProgress"]
    nb_snapshots: int
    offline_bytes_transferred: int
    offline_total_bytes: int
    online_bytes_transferred: int
    online_total_bytes: int
    percent_complete: float
    snapshots_sizes: list[int]
    src_external_id: str
    status: "ReplicateVolumeInstanceStatus"
    dest_region: Optional[str] = None
    dest_stacker_id: Optional[str] = None
    error: Optional[str] = None
    estimated_time_remaining_ms: Optional[int] = None
    src_region: Optional[str] = None
    src_stacker_id: Optional[str] = None
    transfer_rate_mbps: Optional[float] = None


@dataclass
class VolumeSnapshotReplicationProgressUpdate:
    bytes_transferred: int
    compressed_bytes_transferred: int
    elapsed_ms: int
    index: int
    percent_complete: float
    status: "ReplicateVolumeInstanceSnapshotStatus"
    total_bytes: int
    compressed_transfer_rate_mbps: Optional[float] = None
    error: Optional[str] = None
    estimated_time_remaining_ms: Optional[int] = None
    started_at: Optional[str] = None
    transfer_rate_mbps: Optional[float] = None


@dataclass
class VolumeVolumeInstancesConnection:
    edges: list["VolumeVolumeInstancesConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class VolumeVolumeInstancesConnectionEdge:
    cursor: str
    node: "VolumeInstance"


@dataclass
class WorkflowId:
    workflow_id: Optional[str] = None


@dataclass
class WorkflowResult:
    status: "WorkflowStatus"
    error: Optional[str] = None


@dataclass
class Workspace:
    adoption_history: list["AdoptionInfo"]
    adoption_level: float
    created_at: str
    customer: "Customer"
    has2_fa_enforcement: bool
    has_guardrails_access: bool
    has_saml: bool
    id: str
    members: list["WorkspaceMember"]
    name: str
    plan: "Plan"
    redacted_due_to2_fa_pending: bool
    referred_users: list["ReferralUser"]
    updated_at: str
    users_without2_fa: list[str]
    allow_deprecated_regions: Optional[bool] = None
    api_token_rate_limit: Optional["ApiTokenRateLimit"] = None
    avatar: Optional[str] = None
    ban_reason: Optional[str] = None
    discord_role: Optional[str] = None
    identity_providers: Optional["WorkspaceIdentityProvidersConnection"] = None
    partner_profile: Optional["PartnerProfile"] = None
    preferred_region: Optional[str] = None
    projects: Optional["WorkspaceProjectsConnection"] = None
    slack_channel_id: Optional[str] = None
    subscription_plan_limit: Optional[Any] = None
    support_tier_override: Optional["SupportTierOverride"] = None


@dataclass
class WorkspaceIdPConnection:
    status: "WorkspaceIdPConnectionStatus"
    created_at: Optional[str] = None
    provider: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class WorkspaceIdentityProvider:
    connection: "WorkspaceIdPConnection"
    created_at: str
    id: str
    updated_at: str
    workspace: "Workspace"
    workspace_id: str
    enforcement_enabled_at: Optional[str] = None


@dataclass
class WorkspaceIdentityProvidersConnection:
    edges: list["WorkspaceIdentityProvidersConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class WorkspaceIdentityProvidersConnectionEdge:
    cursor: str
    node: "WorkspaceIdentityProvider"


@dataclass
class WorkspaceMember:
    email: str
    id: str
    role: "TeamRole"
    avatar: Optional[str] = None
    feature_flags: Optional[list["ActiveFeatureFlag"]] = None
    name: Optional[str] = None
    two_factor_auth_enabled: Optional[bool] = None


@dataclass
class WorkspacePolicy:
    id: str
    restrict_public_tcp_proxies: bool
    restrict_railway_domain_generation: bool


@dataclass
class WorkspaceProjectsConnection:
    edges: list["WorkspaceProjectsConnectionEdge"]
    page_info: "PageInfo"


@dataclass
class WorkspaceProjectsConnectionEdge:
    cursor: str
    node: "Project"

