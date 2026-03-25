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


# INTERFACE: Domain = "CustomDomain", "ServiceDomain"
Domain = Any

# INTERFACE: Node = "AdoptionInfo", "ApiToken", "AuditLog", "Bucket", "Container", "Credit", "Customer", "Deployment", "DeploymentEvent", "DeploymentInstanceExecution", "DeploymentSnapshot", "DeploymentTrigger", "Environment", "EnvironmentPatch", "Event", "Integration", "IntegrationAuth", "InviteCode", "NotificationChannel", "NotificationDelivery", "NotificationInstance", "NotificationRule", "ObservabilityDashboard", "ObservabilityDashboardAlert", "ObservabilityDashboardItem", "ObservabilityDashboardItemInstance", "ObservabilityDashboardMonitor", "Passkey", "PlanLimitOverride", "Plugin", "Preferences", "Project", "ProjectPermission", "ProjectToken", "ProviderAuth", "ReferralInfo", "Service", "ServiceInstance", "Session", "SpendCommitment", "SshPublicKey", "Team", "TeamPermission", "Template", "TemplateService", "UsageLimit", "User", "Variable", "Volume", "VolumeInstance", "VolumeInstanceBackupSchedule", "Workspace", "WorkspaceIdentityProvider", "WorkspacePolicy"
Node = Any

# UNION: NotificationDeliveryUpdate = "NotificationDeliveryCreated", "NotificationDeliveryResolved"
NotificationDeliveryUpdate = Any

# UNION: ObservabilityDashboardMonitorConfig = "MonitorThresholdConfig"
ObservabilityDashboardMonitorConfig = Any

# UNION: PublicProjectInvitation = "InviteCode", "ProjectInvitation"
PublicProjectInvitation = Any


class AccessRule(_Base):
    disallowed: Optional[str] = None


class AdoptionInfo(_Base):
    adoption_level: Optional[float] = None
    created_at: Optional[str] = None
    delta_level: Optional[float] = None
    id: Optional[str] = None
    matched_icp_email: Optional[str] = None
    monthly_estimated_usage: Optional[float] = None
    num_config_file: Optional[int] = None
    num_cron_schedule: Optional[int] = None
    num_deploys: Optional[int] = None
    num_envs: Optional[int] = None
    num_failed_deploys: Optional[int] = None
    num_healthcheck: Optional[int] = None
    num_icon_config: Optional[int] = None
    num_region: Optional[int] = None
    num_replicas: Optional[int] = None
    num_root_directory: Optional[int] = None
    num_seats: Optional[int] = None
    num_services: Optional[int] = None
    num_variables: Optional[int] = None
    num_watch_patterns: Optional[int] = None
    total_cores: Optional[float] = None
    total_disk: Optional[float] = None
    total_network: Optional[float] = None
    updated_at: Optional[str] = None
    workspace: Optional["Workspace"] = None


class AggregatedUsage(_Base):
    """The aggregated usage of a single measurement."""
    measurement: Optional["MetricMeasurement"] = None
    tags: Optional["MetricTags"] = None
    value: Optional[float] = None


class AllDomains(_Base):
    custom_domains: Optional[list["CustomDomain"]] = None
    service_domains: Optional[list["ServiceDomain"]] = None


class ApiToken(_Base):
    display_token: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    workspace_id: Optional[str] = None


class ApiTokenContext(_Base):
    """Information about the current API token and its accessible workspaces."""
    workspaces: Optional[list["ApiTokenWorkspace"]] = None


class ApiTokenRateLimit(_Base):
    remaining_points: Optional[int] = None
    resets_at: Optional[str] = None


class ApiTokenWorkspace(_Base):
    id: Optional[str] = None
    name: Optional[str] = None


class AppliedByMember(_Base):
    avatar: Optional[str] = None
    email: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    username: Optional[str] = None


class AuditLog(_Base):
    context: Optional[Any] = None
    created_at: Optional[str] = None
    environment: Optional["Environment"] = None
    environment_id: Optional[str] = None
    event_type: Optional[str] = None
    id: Optional[str] = None
    payload: Optional[Any] = None
    project: Optional["Project"] = None
    project_id: Optional[str] = None
    workspace_id: Optional[str] = None


class AuditLogEventTypeInfo(_Base):
    description: Optional[str] = None
    event_type: Optional[str] = None


class BillingPeriod(_Base):
    """The billing period for a customers subscription."""
    end: Optional[str] = None
    start: Optional[str] = None


class Bucket(_Base):
    created_at: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    project: Optional["Project"] = None
    project_id: Optional[str] = None
    updated_at: Optional[str] = None


class BucketInstanceDetails(_Base):
    object_count: Optional[int] = None
    size_bytes: Optional[int] = None


class BucketS3CompatibleCredentials(_Base):
    access_key_id: Optional[str] = None
    bucket_name: Optional[str] = None
    created_at: Optional[str] = None
    endpoint: Optional[str] = None
    region: Optional[str] = None
    secret_access_key: Optional[str] = None
    url_style: Optional[str] = None


class CanvasViewMergePreview(_Base):
    mutations: Optional[list[Any]] = None
    state: Optional[Any] = None


class CertificatePublicData(_Base):
    domain_names: Optional[list[str]] = None
    expires_at: Optional[str] = None
    fingerprint_sha256: Optional[str] = None
    issued_at: Optional[str] = None
    key_type: Optional["KeyType"] = None


class CnameCheck(_Base):
    link: Optional[str] = None
    message: Optional[str] = None
    status: Optional["CnameCheckStatus"] = None


class ComplianceAgreementsInfo(_Base):
    has_baa: Optional[bool] = None
    has_dpa: Optional[bool] = None


class Container(_Base):
    created_at: Optional[str] = None
    deleted_at: Optional[str] = None
    environment: Optional["Environment"] = None
    environment_id: Optional[str] = None
    id: Optional[str] = None
    migrated_at: Optional[str] = None
    plugin: Optional["Plugin"] = None
    plugin_id: Optional[str] = None


class Credit(_Base):
    amount: Optional[float] = None
    created_at: Optional[str] = None
    customer_id: Optional[str] = None
    id: Optional[str] = None
    memo: Optional[str] = None
    type: Optional["CreditType"] = None
    updated_at: Optional[str] = None


class CustomDomain(_Base):
    cdn_mode: Optional[str] = None
    cname_check: Optional["CnameCheck"] = None
    created_at: Optional[str] = None
    deleted_at: Optional[str] = None
    domain: Optional[str] = None
    edge_id: Optional[str] = None
    environment_id: Optional[str] = None
    id: Optional[str] = None
    project_id: Optional[str] = None
    service_id: Optional[str] = None
    status: Optional["CustomDomainStatus"] = None
    sync_status: Optional["CustomDomainSyncStatus"] = None
    target_port: Optional[int] = None
    updated_at: Optional[str] = None


class CustomDomainStatus(_Base):
    cdn_provider: Optional["CDNProvider"] = None
    certificate_error_message: Optional[str] = None
    certificate_error_type: Optional["CertificateErrorType"] = None
    certificate_retryable: Optional[bool] = None
    certificate_status: Optional["CertificateStatus"] = None
    certificate_status_detailed: Optional["CertificateStatusDetailed"] = None
    certificates: Optional[list["CertificatePublicData"]] = None
    dns_records: Optional[list["DNSRecords"]] = None
    verification_dns_host: Optional[str] = None
    verification_token: Optional[str] = None
    verified: Optional[bool] = None


class Customer(_Base):
    applied_credits: Optional[float] = None
    billing_address: Optional["CustomerAddress"] = None
    billing_email: Optional[str] = None
    billing_period: Optional["BillingPeriod"] = None
    credit_balance: Optional[float] = None
    credits: Optional["CustomerCreditsConnection"] = None
    current_usage: Optional[float] = None
    default_payment_method: Optional["PaymentMethod"] = None
    default_payment_method_id: Optional[str] = None
    has_exhausted_free_plan: Optional[bool] = None
    id: Optional[str] = None
    invoices: Optional[list["CustomerInvoice"]] = None
    is_prepaying: Optional[bool] = None
    is_trialing: Optional[bool] = None
    is_usage_subscriber: Optional[bool] = None
    is_withdrawing_to_credits: Optional[bool] = None
    plan_limit_override: Optional["PlanLimitOverride"] = None
    remaining_usage_credit_balance: Optional[float] = None
    spend_commitment: Optional["SpendCommitment"] = None
    state: Optional["SubscriptionState"] = None
    stripe_customer_id: Optional[str] = None
    subscriptions: Optional[list["CustomerSubscription"]] = None
    supported_withdrawal_platforms: Optional[list["WithdrawalPlatformTypes"]] = None
    tax_ids: Optional[list["CustomerTaxId"]] = None
    trial_days_remaining: Optional[int] = None
    usage_limit: Optional["UsageLimit"] = None
    workspace: Optional["Workspace"] = None


class CustomerAddress(_Base):
    city: Optional[str] = None
    country: Optional[str] = None
    line1: Optional[str] = None
    line2: Optional[str] = None
    name: Optional[str] = None
    postal_code: Optional[str] = None
    state: Optional[str] = None


class CustomerCreditsConnection(_Base):
    edges: Optional[list["CustomerCreditsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class CustomerCreditsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Credit"] = None


class CustomerInvoice(_Base):
    amount_due: Optional[float] = None
    amount_paid: Optional[float] = None
    hosted_url: Optional[str] = None
    invoice_id: Optional[str] = None
    items: Optional[list["SubscriptionItem"]] = None
    last_payment_error: Optional[str] = None
    payment_intent_status: Optional[str] = None
    pdf_url: Optional[str] = None
    period_end: Optional[str] = None
    period_start: Optional[str] = None
    reissued_invoice_from: Optional[str] = None
    reissued_invoice_of: Optional[str] = None
    spend_commitment_prepayment: Optional[bool] = None
    status: Optional[str] = None
    subscription_id: Optional[str] = None
    subscription_status: Optional[str] = None
    total: Optional[int] = None


class CustomerSubscription(_Base):
    billing_cycle_anchor: Optional[str] = None
    cancel_at: Optional[str] = None
    cancel_at_period_end: Optional[bool] = None
    coupon_id: Optional[str] = None
    discounts: Optional[list["SubscriptionDiscount"]] = None
    id: Optional[str] = None
    items: Optional[list["SubscriptionItem"]] = None
    latest_invoice_id: Optional[str] = None
    next_invoice_current_total: Optional[int] = None
    next_invoice_date: Optional[str] = None
    status: Optional[str] = None


class CustomerTaxId(_Base):
    id: Optional[str] = None
    type: Optional[str] = None
    value: Optional[str] = None


class DNSRecords(_Base):
    current_value: Optional[str] = None
    fqdn: Optional[str] = None
    hostlabel: Optional[str] = None
    purpose: Optional["DNSRecordPurpose"] = None
    record_type: Optional["DNSRecordType"] = None
    required_value: Optional[str] = None
    status: Optional["DNSRecordStatus"] = None
    zone: Optional[str] = None


class Deployment(_Base):
    can_redeploy: Optional[bool] = None
    can_rollback: Optional[bool] = None
    created_at: Optional[str] = None
    creator: Optional["DeploymentCreator"] = None
    deployment_stopped: Optional[bool] = None
    diagnosis: Optional[Any] = None
    environment: Optional["Environment"] = None
    environment_id: Optional[str] = None
    id: Optional[str] = None
    instances: Optional[list["DeploymentDeploymentInstance"]] = None
    meta: Optional[Any] = None
    project_id: Optional[str] = None
    service: Optional["Service"] = None
    service_id: Optional[str] = None
    snapshot_id: Optional[str] = None
    sockets: Optional[list["DeploymentSocket"]] = None
    static_url: Optional[str] = None
    status: Optional["DeploymentStatus"] = None
    status_updated_at: Optional[str] = None
    suggest_add_service_domain: Optional[bool] = None
    updated_at: Optional[str] = None
    url: Optional[str] = None


class DeploymentCreator(_Base):
    avatar: Optional[str] = None
    email: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None


class DeploymentDeploymentInstance(_Base):
    id: Optional[str] = None
    status: Optional["DeploymentInstanceStatus"] = None


class DeploymentEvent(_Base):
    completed_at: Optional[str] = None
    created_at: Optional[str] = None
    id: Optional[str] = None
    payload: Optional["DeploymentEventPayload"] = None
    step: Optional["DeploymentEventStep"] = None


class DeploymentEventPayload(_Base):
    error: Optional[str] = None


class DeploymentInstanceExecution(_Base):
    completed_at: Optional[str] = None
    created_at: Optional[str] = None
    deployment_id: Optional[str] = None
    deployment_meta: Optional[Any] = None
    id: Optional[str] = None
    status: Optional["DeploymentInstanceStatus"] = None
    updated_at: Optional[str] = None


class DeploymentSnapshot(_Base):
    created_at: Optional[str] = None
    id: Optional[str] = None
    updated_at: Optional[str] = None
    variables: Optional[Any] = None


class DeploymentSocket(_Base):
    ipv6: Optional[bool] = None
    port: Optional[int] = None
    process_name: Optional[str] = None
    updated_at: Optional[int] = None


class DeploymentTrigger(_Base):
    base_environment_override_id: Optional[str] = None
    branch: Optional[str] = None
    check_suites: Optional[bool] = None
    environment_id: Optional[str] = None
    id: Optional[str] = None
    project_id: Optional[str] = None
    provider: Optional[str] = None
    repository: Optional[str] = None
    service_id: Optional[str] = None
    valid_check_suites: Optional[int] = None


class DockerComposeImport(_Base):
    errors: Optional[list[str]] = None
    patch: Optional[Any] = None


class DomainAvailable(_Base):
    available: Optional[bool] = None
    message: Optional[str] = None


class DomainWithStatus(_Base):
    cdn_provider: Optional["CDNProvider"] = None
    certificate_error_message: Optional[str] = None
    certificate_error_type: Optional["CertificateErrorType"] = None
    certificate_retryable: Optional[bool] = None
    certificate_status: Optional["CertificateStatus"] = None
    certificate_status_detailed: Optional["CertificateStatusDetailed"] = None
    certificates: Optional[list["CertificatePublicData"]] = None
    dns_records: Optional[list["DNSRecords"]] = None
    domain: Optional["Domain"] = None


class EgressGateway(_Base):
    ipv4: Optional[str] = None
    region: Optional[str] = None


class Environment(_Base):
    can_access: Optional[bool] = None
    config: Optional[Any] = None
    created_at: Optional[str] = None
    deleted_at: Optional[str] = None
    deployment_triggers: Optional["EnvironmentDeploymentTriggersConnection"] = None
    deployments: Optional["EnvironmentDeploymentsConnection"] = None
    id: Optional[str] = None
    is_ephemeral: Optional[bool] = None
    meta: Optional["EnvironmentMeta"] = None
    name: Optional[str] = None
    project_id: Optional[str] = None
    service_instances: Optional["EnvironmentServiceInstancesConnection"] = None
    source_environment: Optional["Environment"] = None
    unmerged_changes_count: Optional[int] = None
    updated_at: Optional[str] = None
    variables: Optional["EnvironmentVariablesConnection"] = None
    volume_instances: Optional["EnvironmentVolumeInstancesConnection"] = None


class EnvironmentDeploymentTriggersConnection(_Base):
    edges: Optional[list["EnvironmentDeploymentTriggersConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class EnvironmentDeploymentTriggersConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["DeploymentTrigger"] = None


class EnvironmentDeploymentsConnection(_Base):
    edges: Optional[list["EnvironmentDeploymentsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class EnvironmentDeploymentsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Deployment"] = None


class EnvironmentMeta(_Base):
    base_branch: Optional[str] = None
    branch: Optional[str] = None
    latest_successful_git_hub_deployment_id: Optional[int] = None
    pr_comment_id: Optional[int] = None
    pr_number: Optional[int] = None
    pr_repo: Optional[str] = None
    pr_title: Optional[str] = None
    skipped_resource_ids: Optional[Any] = None


class EnvironmentPatch(_Base):
    applied_at: Optional[str] = None
    applied_by: Optional["AppliedByMember"] = None
    created_at: Optional[str] = None
    environment: Optional["Environment"] = None
    environment_id: Optional[str] = None
    id: Optional[str] = None
    last_applied_error: Optional[str] = None
    message: Optional[str] = None
    patch: Optional[Any] = None
    status: Optional["EnvironmentPatchStatus"] = None
    updated_at: Optional[str] = None


class EnvironmentServiceInstancesConnection(_Base):
    edges: Optional[list["EnvironmentServiceInstancesConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class EnvironmentServiceInstancesConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["ServiceInstance"] = None


class EnvironmentVariablesConnection(_Base):
    edges: Optional[list["EnvironmentVariablesConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class EnvironmentVariablesConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Variable"] = None


class EnvironmentVolumeInstancesConnection(_Base):
    edges: Optional[list["EnvironmentVolumeInstancesConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class EnvironmentVolumeInstancesConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["VolumeInstance"] = None


class EstimatedUsage(_Base):
    """The estimated usage of a single measurement."""
    estimated_value: Optional[float] = None
    measurement: Optional["MetricMeasurement"] = None
    project_id: Optional[str] = None


class Event(_Base):
    action: Optional[str] = None
    created_at: Optional[str] = None
    environment: Optional["Environment"] = None
    environment_id: Optional[str] = None
    id: Optional[str] = None
    object: Optional[str] = None
    payload: Optional[Any] = None
    project: Optional["Project"] = None
    project_id: Optional[str] = None
    severity: Optional["EventSeverity"] = None


class ExternalWorkspace(_Base):
    allow_deprecated_regions: Optional[bool] = None
    avatar: Optional[str] = None
    ban_reason: Optional[str] = None
    created_at: Optional[str] = None
    current_session_has_access: Optional[bool] = None
    customer_id: Optional[str] = None
    customer_state: Optional["SubscriptionState"] = None
    discord_role: Optional[str] = None
    has2_fa_enforcement: Optional[bool] = None
    has_baa: Optional[bool] = None
    has_guardrails_access: Optional[bool] = None
    has_rbac: Optional[bool] = None
    has_saml: Optional[bool] = None
    id: Optional[str] = None
    is_trialing: Optional[bool] = None
    name: Optional[str] = None
    plan: Optional["Plan"] = None
    preferred_region: Optional[str] = None
    projects: Optional[list["Project"]] = None
    redacted_due_to2_fa_pending: Optional[bool] = None
    subscription_plan_limit: Optional[Any] = None
    support_tier_override: Optional[str] = None
    team_id: Optional[str] = None


class FunctionRuntime(_Base):
    image: Optional[str] = None
    latest_version: Optional["FunctionRuntimeVersion"] = None
    name: Optional["FunctionRuntimeName"] = None
    versions: Optional[list["FunctionRuntimeVersion"]] = None


class FunctionRuntimeVersion(_Base):
    image: Optional[str] = None
    tag: Optional[str] = None


class GitHubAccess(_Base):
    has_access: Optional[bool] = None
    is_public: Optional[bool] = None


class GitHubBranch(_Base):
    name: Optional[str] = None


class GitHubCheck(_Base):
    name: Optional[str] = None
    status: Optional[str] = None


class GitHubPRInfo(_Base):
    additions: Optional[int] = None
    author: Optional[str] = None
    body: Optional[str] = None
    changed_files: Optional[int] = None
    checks: Optional[list["GitHubCheck"]] = None
    deletions: Optional[int] = None
    mergeable: Optional[bool] = None
    state: Optional[str] = None
    title: Optional[str] = None


class GitHubRepo(_Base):
    default_branch: Optional[str] = None
    description: Optional[str] = None
    full_name: Optional[str] = None
    id: Optional[int] = None
    installation_id: Optional[str] = None
    is_private: Optional[bool] = None
    name: Optional[str] = None
    owner_avatar_url: Optional[str] = None


class GitHubRepoWithoutInstallation(_Base):
    default_branch: Optional[str] = None
    description: Optional[str] = None
    full_name: Optional[str] = None
    id: Optional[int] = None
    is_private: Optional[bool] = None
    name: Optional[str] = None


class GitHubSshKey(_Base):
    """An SSH public key from GitHub."""
    id: Optional[int] = None
    key: Optional[str] = None
    title: Optional[str] = None


class HerokuApp(_Base):
    id: Optional[str] = None
    name: Optional[str] = None


class HttpDurationMetricsResult(_Base):
    """The result of an HTTP duration metrics query."""
    samples: Optional[list["HttpDurationMetricsSample"]] = None


class HttpDurationMetricsSample(_Base):
    """A single sample of HTTP duration metrics."""
    p50: Optional[float] = None
    p90: Optional[float] = None
    p95: Optional[float] = None
    p99: Optional[float] = None
    ts: Optional[int] = None


class HttpLog(_Base):
    """The result of a http logs query."""
    client_ua: Optional[str] = None
    deployment_id: Optional[str] = None
    deployment_instance_id: Optional[str] = None
    downstream_proto: Optional[str] = None
    edge_region: Optional[str] = None
    host: Optional[str] = None
    http_status: Optional[int] = None
    method: Optional[str] = None
    path: Optional[str] = None
    request_id: Optional[str] = None
    response_details: Optional[str] = None
    rx_bytes: Optional[int] = None
    src_ip: Optional[str] = None
    timestamp: Optional[str] = None
    total_duration: Optional[int] = None
    tx_bytes: Optional[int] = None
    upstream_address: Optional[str] = None
    upstream_errors: Optional[str] = None
    upstream_proto: Optional[str] = None
    upstream_rq_duration: Optional[int] = None


class HttpMetricsByStatusResult(_Base):
    """HTTP metrics grouped by status code."""
    samples: Optional[list["HttpMetricsSample"]] = None
    status_code: Optional[int] = None


class HttpMetricsResult(_Base):
    """The result of an HTTP metrics query."""
    samples: Optional[list["HttpMetricsSample"]] = None


class HttpMetricsSample(_Base):
    """A single sample of an HTTP metric."""
    ts: Optional[int] = None
    value: Optional[float] = None


class Incident(_Base):
    id: Optional[str] = None
    message: Optional[str] = None
    status: Optional["IncidentStatus"] = None
    url: Optional[str] = None


class Integration(_Base):
    config: Optional[Any] = None
    id: Optional[str] = None
    name: Optional[str] = None
    project_id: Optional[str] = None


class IntegrationAuth(_Base):
    id: Optional[str] = None
    integrations: Optional["IntegrationAuthIntegrationsConnection"] = None
    provider: Optional[str] = None
    provider_id: Optional[str] = None


class IntegrationAuthIntegrationsConnection(_Base):
    edges: Optional[list["IntegrationAuthIntegrationsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class IntegrationAuthIntegrationsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Integration"] = None


class InviteCode(_Base):
    code: Optional[str] = None
    created_at: Optional[str] = None
    id: Optional[str] = None
    project: Optional["Project"] = None
    project_id: Optional[str] = None
    role: Optional["ProjectRole"] = None


class Log(_Base):
    """The result of a logs query."""
    attributes: Optional[list["LogAttribute"]] = None
    message: Optional[str] = None
    severity: Optional[str] = None
    tags: Optional["LogTags"] = None
    timestamp: Optional[str] = None


class LogAttribute(_Base):
    """The attributes associated with a structured log"""
    key: Optional[str] = None
    value: Optional[str] = None


class LogTags(_Base):
    """The tags associated with a specific log"""
    deployment_id: Optional[str] = None
    deployment_instance_id: Optional[str] = None
    environment_id: Optional[str] = None
    plugin_id: Optional[str] = None
    project_id: Optional[str] = None
    service_id: Optional[str] = None
    snapshot_id: Optional[str] = None


class Maintenance(_Base):
    id: Optional[str] = None
    message: Optional[str] = None
    start: Optional[str] = None
    status: Optional["MaintenanceStatus"] = None
    url: Optional[str] = None


class Metric(_Base):
    """A single sample of a metric."""
    ts: Optional[int] = None
    value: Optional[float] = None


class MetricTags(_Base):
    """The tags that were used to group the metric."""
    deployment_id: Optional[str] = None
    deployment_instance_id: Optional[str] = None
    environment_id: Optional[str] = None
    plugin_id: Optional[str] = None
    project_id: Optional[str] = None
    region: Optional[str] = None
    service_id: Optional[str] = None
    volume_id: Optional[str] = None
    volume_instance_id: Optional[str] = None


class MetricsResult(_Base):
    """The result of a metrics query."""
    measurement: Optional["MetricMeasurement"] = None
    tags: Optional["MetricTags"] = None
    values: Optional[list["Metric"]] = None


class MonitorThresholdConfig(_Base):
    condition: Optional["MonitorThresholdCondition"] = None
    measurement: Optional["MetricMeasurement"] = None
    threshold: Optional[float] = None
    type: Optional[str] = None


class NotificationChannel(_Base):
    config: Optional[Any] = None
    created_at: Optional[str] = None
    id: Optional[str] = None
    updated_at: Optional[str] = None
    workspace_id: Optional[str] = None


class NotificationDelivery(_Base):
    created_at: Optional[str] = None
    id: Optional[str] = None
    notification_instance: Optional["NotificationInstance"] = None
    read_at: Optional[str] = None
    status: Optional["NotificationDeliveryStatus"] = None
    type: Optional["NotificationDeliveryType"] = None
    updated_at: Optional[str] = None
    user_id: Optional[str] = None


class NotificationDeliveryCreated(_Base):
    delivery: Optional["NotificationDelivery"] = None
    type: Optional[str] = None


class NotificationDeliveryResolved(_Base):
    delivery_ids: Optional[list[str]] = None
    type: Optional[str] = None


class NotificationInstance(_Base):
    created_at: Optional[str] = None
    environment_id: Optional[str] = None
    event: Optional["Event"] = None
    event_id: Optional[str] = None
    event_type: Optional[str] = None
    id: Optional[str] = None
    payload: Optional[Any] = None
    project_id: Optional[str] = None
    resolved_at: Optional[str] = None
    resource_id: Optional[str] = None
    resource_type: Optional[str] = None
    service_id: Optional[str] = None
    severity: Optional["NotificationSeverity"] = None
    status: Optional["NotificationStatus"] = None
    updated_at: Optional[str] = None
    volume_id: Optional[str] = None
    workspace_id: Optional[str] = None


class NotificationRule(_Base):
    channels: Optional[list["NotificationChannel"]] = None
    created_at: Optional[str] = None
    environment_id: Optional[str] = None
    ephemeral_environments: Optional[bool] = None
    event_types: Optional[list[str]] = None
    id: Optional[str] = None
    project_id: Optional[str] = None
    service_id: Optional[str] = None
    severities: Optional[list["NotificationSeverity"]] = None
    updated_at: Optional[str] = None
    workspace_id: Optional[str] = None


class ObservabilityDashboard(_Base):
    id: Optional[str] = None
    items: Optional[list["ObservabilityDashboardItemInstance"]] = None


class ObservabilityDashboardAlert(_Base):
    created_at: Optional[str] = None
    id: Optional[str] = None
    resolved_at: Optional[str] = None
    resource_id: Optional[str] = None
    resource_type: Optional["MonitorAlertResourceType"] = None
    status: Optional["MonitorStatus"] = None


class ObservabilityDashboardItem(_Base):
    config: Optional["ObservabilityDashboardItemConfig"] = None
    description: Optional[str] = None
    id: Optional[str] = None
    monitors: Optional[list["ObservabilityDashboardMonitor"]] = None
    name: Optional[str] = None
    type: Optional["ObservabilityDashboardItemType"] = None


class ObservabilityDashboardItemConfig(_Base):
    logs_filter: Optional[str] = None
    measurements: Optional[list["MetricMeasurement"]] = None
    project_usage_properties: Optional[list["ProjectUsageProperty"]] = None
    resource_ids: Optional[list[str]] = None


class ObservabilityDashboardItemInstance(_Base):
    dashboard_item: Optional["ObservabilityDashboardItem"] = None
    display_config: Optional[Any] = None
    id: Optional[str] = None


class ObservabilityDashboardMonitor(_Base):
    alerts: Optional[list["ObservabilityDashboardAlert"]] = None
    config: Optional["ObservabilityDashboardMonitorConfig"] = None
    created_at: Optional[str] = None
    id: Optional[str] = None
    updated_at: Optional[str] = None


class PageInfo(_Base):
    end_cursor: Optional[str] = None
    has_next_page: Optional[bool] = None
    has_previous_page: Optional[bool] = None
    start_cursor: Optional[str] = None


class PartnerProfile(_Base):
    category: Optional[str] = None
    description: Optional[str] = None
    slug: Optional[str] = None
    type: Optional["PartnerProfileType"] = None
    website: Optional[str] = None


class Passkey(_Base):
    aaguid: Optional[str] = None
    backed_up: Optional[bool] = None
    created_at: Optional[str] = None
    credential_id: Optional[str] = None
    device_name: Optional[str] = None
    device_type: Optional[str] = None
    display_name: Optional[str] = None
    id: Optional[str] = None
    last_used_at: Optional[str] = None
    last_used_device: Optional[str] = None
    transports: Optional[list[str]] = None
    updated_at: Optional[str] = None


class PaymentMethod(_Base):
    card: Optional["PaymentMethodCard"] = None
    id: Optional[str] = None


class PaymentMethodCard(_Base):
    brand: Optional[str] = None
    country: Optional[str] = None
    last4: Optional[str] = None


class PlanLimitOverride(_Base):
    config: Optional[Any] = None
    id: Optional[str] = None


class PlatformFeatureFlagStatus(_Base):
    flag: Optional["PlatformFeatureFlag"] = None
    rollout_percentage: Optional[int] = None
    status: Optional[bool] = None
    type: Optional["PlatformFeatureFlagType"] = None


class PlatformStatus(_Base):
    incident: Optional["Incident"] = None
    is_stable: Optional[bool] = None
    maintenance: Optional["Maintenance"] = None


class Plugin(_Base):
    containers: Optional["PluginContainersConnection"] = None
    created_at: Optional[str] = None
    deleted_at: Optional[str] = None
    deprecated_at: Optional[str] = None
    friendly_name: Optional[str] = None
    id: Optional[str] = None
    logs_enabled: Optional[bool] = None
    migration_database_service_id: Optional[str] = None
    name: Optional["PluginType"] = None
    project: Optional["Project"] = None
    status: Optional["PluginStatus"] = None
    variables: Optional["PluginVariablesConnection"] = None


class PluginContainersConnection(_Base):
    edges: Optional[list["PluginContainersConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class PluginContainersConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Container"] = None


class PluginVariablesConnection(_Base):
    edges: Optional[list["PluginVariablesConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class PluginVariablesConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Variable"] = None


class Preferences(_Base):
    build_failed_email: Optional[bool] = None
    changelog_email: Optional[bool] = None
    community_email: Optional[bool] = None
    deploy_crashed_email: Optional[bool] = None
    ephemeral_environment_email: Optional[bool] = None
    id: Optional[str] = None
    marketing_email: Optional[bool] = None
    subprocessor_updates_email: Optional[bool] = None
    template_queue_email: Optional[bool] = None
    usage_email: Optional[bool] = None


class PrivateNetwork(_Base):
    created_at: Optional[str] = None
    deleted_at: Optional[str] = None
    dns_name: Optional[str] = None
    environment_id: Optional[str] = None
    name: Optional[str] = None
    network_id: Optional[int] = None
    project_id: Optional[str] = None
    public_id: Optional[str] = None
    tags: Optional[list[str]] = None


class PrivateNetworkEndpoint(_Base):
    created_at: Optional[str] = None
    deleted_at: Optional[str] = None
    dns_name: Optional[str] = None
    new_dns_name: Optional[str] = None
    private_ips: Optional[list[str]] = None
    public_id: Optional[str] = None
    service_instance_id: Optional[str] = None
    sync_status: Optional["PrivateNetworkEndpointSyncStatus"] = None
    tags: Optional[list[str]] = None


class Project(_Base):
    base_environment: Optional["Environment"] = None
    base_environment_id: Optional[str] = None
    bot_pr_environments: Optional[bool] = None
    buckets: Optional["ProjectBucketsConnection"] = None
    created_at: Optional[str] = None
    deleted_at: Optional[str] = None
    deployment_triggers: Optional["ProjectDeploymentTriggersConnection"] = None
    deployments: Optional["ProjectDeploymentsConnection"] = None
    description: Optional[str] = None
    environments: Optional["ProjectEnvironmentsConnection"] = None
    expired_at: Optional[str] = None
    feature_flags: Optional[list["ActiveProjectFeatureFlag"]] = None
    focused_pr_environments: Optional[bool] = None
    groups: Optional["ProjectGroupsConnection"] = None
    id: Optional[str] = None
    is_public: Optional[bool] = None
    is_temp_project: Optional[bool] = None
    members: Optional[list["ProjectMember"]] = None
    name: Optional[str] = None
    plugins: Optional["ProjectPluginsConnection"] = None
    pr_deploys: Optional[bool] = None
    project_permissions: Optional["ProjectProjectPermissionsConnection"] = None
    services: Optional["ProjectServicesConnection"] = None
    subscription_plan_limit: Optional[Any] = None
    subscription_type: Optional["SubscriptionPlanType"] = None
    team: Optional["Team"] = None
    team_id: Optional[str] = None
    updated_at: Optional[str] = None
    volumes: Optional["ProjectVolumesConnection"] = None
    workspace: Optional["Workspace"] = None
    workspace_id: Optional[str] = None


class ProjectBucketsConnection(_Base):
    edges: Optional[list["ProjectBucketsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class ProjectBucketsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Bucket"] = None


class ProjectComplianceInfo(_Base):
    member_permissions: Optional[list["ProjectMemberPermissionsInfo"]] = None
    project_id: Optional[str] = None
    project_name: Optional[str] = None
    service_backups: Optional[list["ServiceBackupInfo"]] = None
    two_factor_members: Optional[list["ProjectMemberTwoFactorInfo"]] = None
    workspace_id: Optional[str] = None


class ProjectDeploymentTriggersConnection(_Base):
    edges: Optional[list["ProjectDeploymentTriggersConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class ProjectDeploymentTriggersConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["DeploymentTrigger"] = None


class ProjectDeploymentsConnection(_Base):
    edges: Optional[list["ProjectDeploymentsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class ProjectDeploymentsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Deployment"] = None


class ProjectEnvironmentsConnection(_Base):
    edges: Optional[list["ProjectEnvironmentsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class ProjectEnvironmentsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Environment"] = None


class ProjectGroupsConnection(_Base):
    edges: Optional[list["ProjectGroupsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class ProjectGroupsConnectionEdge(_Base):
    cursor: Optional[str] = None


class ProjectInvitation(_Base):
    email: Optional[str] = None
    expires_at: Optional[str] = None
    id: Optional[str] = None
    inviter: Optional["ProjectInvitationInviter"] = None
    is_expired: Optional[bool] = None
    project: Optional["PublicProjectInformation"] = None


class ProjectInvitationInviter(_Base):
    email: Optional[str] = None
    name: Optional[str] = None


class ProjectMember(_Base):
    avatar: Optional[str] = None
    email: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    role: Optional["ProjectRole"] = None


class ProjectMemberPermissionsInfo(_Base):
    email: Optional[str] = None
    name: Optional[str] = None
    role: Optional["ProjectRole"] = None


class ProjectMemberTwoFactorInfo(_Base):
    email: Optional[str] = None
    enabled_methods: Optional[list["TwoFactorMethodCompliance"]] = None
    name: Optional[str] = None
    two_factor_auth_enabled: Optional[bool] = None


class ProjectPermission(_Base):
    id: Optional[str] = None
    project_id: Optional[str] = None
    role: Optional["ProjectRole"] = None
    user_id: Optional[str] = None


class ProjectPluginsConnection(_Base):
    edges: Optional[list["ProjectPluginsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class ProjectPluginsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Plugin"] = None


class ProjectProjectPermissionsConnection(_Base):
    edges: Optional[list["ProjectProjectPermissionsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class ProjectProjectPermissionsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["ProjectPermission"] = None


class ProjectResourceAccess(_Base):
    custom_domain: Optional["AccessRule"] = None
    database_deployment: Optional["AccessRule"] = None
    deployment: Optional["AccessRule"] = None
    environment: Optional["AccessRule"] = None
    plugin: Optional["AccessRule"] = None


class ProjectServicesConnection(_Base):
    edges: Optional[list["ProjectServicesConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class ProjectServicesConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Service"] = None


class ProjectToken(_Base):
    created_at: Optional[str] = None
    display_token: Optional[str] = None
    environment: Optional["Environment"] = None
    environment_id: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    project: Optional["Project"] = None
    project_id: Optional[str] = None


class ProjectVolumesConnection(_Base):
    edges: Optional[list["ProjectVolumesConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class ProjectVolumesConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Volume"] = None


class ProjectWorkspaceMember(_Base):
    email: Optional[str] = None
    enabled_methods: Optional[list["TwoFactorMethodProjectWorkspace"]] = None
    name: Optional[str] = None
    two_factor_auth_enabled: Optional[bool] = None


class ProjectWorkspaceMembersResponse(_Base):
    members: Optional[list["ProjectWorkspaceMember"]] = None
    project_id: Optional[str] = None
    project_name: Optional[str] = None
    workspace_id: Optional[str] = None


class ProviderAuth(_Base):
    email: Optional[str] = None
    id: Optional[str] = None
    is_auth_enabled: Optional[bool] = None
    metadata: Optional[Any] = None
    provider: Optional[str] = None
    user_id: Optional[str] = None


class PublicProjectInformation(_Base):
    id: Optional[str] = None
    name: Optional[str] = None


class PublicStats(_Base):
    total_deployments_last_month: Optional[int] = None
    total_logs_last_month: Optional[int] = None
    total_projects: Optional[int] = None
    total_requests_last_month: Optional[int] = None
    total_services: Optional[int] = None
    total_users: Optional[int] = None


class QueryApiTokensConnection(_Base):
    edges: Optional[list["QueryApiTokensConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryApiTokensConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["ApiToken"] = None


class QueryAuditLogsConnection(_Base):
    edges: Optional[list["QueryAuditLogsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryAuditLogsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["AuditLog"] = None


class QueryDeploymentEventsConnection(_Base):
    edges: Optional[list["QueryDeploymentEventsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryDeploymentEventsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["DeploymentEvent"] = None


class QueryDeploymentInstanceExecutionsConnection(_Base):
    edges: Optional[list["QueryDeploymentInstanceExecutionsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryDeploymentInstanceExecutionsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["DeploymentInstanceExecution"] = None


class QueryDeploymentTriggersConnection(_Base):
    edges: Optional[list["QueryDeploymentTriggersConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryDeploymentTriggersConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["DeploymentTrigger"] = None


class QueryDeploymentsConnection(_Base):
    edges: Optional[list["QueryDeploymentsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryDeploymentsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Deployment"] = None


class QueryEnvironmentPatchesConnection(_Base):
    edges: Optional[list["QueryEnvironmentPatchesConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryEnvironmentPatchesConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["EnvironmentPatch"] = None


class QueryEnvironmentsConnection(_Base):
    edges: Optional[list["QueryEnvironmentsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryEnvironmentsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Environment"] = None


class QueryEventsConnection(_Base):
    edges: Optional[list["QueryEventsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryEventsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Event"] = None


class QueryIntegrationAuthsConnection(_Base):
    edges: Optional[list["QueryIntegrationAuthsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryIntegrationAuthsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["IntegrationAuth"] = None


class QueryIntegrationsConnection(_Base):
    edges: Optional[list["QueryIntegrationsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryIntegrationsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Integration"] = None


class QueryNotificationDeliveriesConnection(_Base):
    edges: Optional[list["QueryNotificationDeliveriesConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryNotificationDeliveriesConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["NotificationDelivery"] = None


class QueryObservabilityDashboardsConnection(_Base):
    edges: Optional[list["QueryObservabilityDashboardsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryObservabilityDashboardsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["ObservabilityDashboard"] = None


class QueryPasskeysConnection(_Base):
    edges: Optional[list["QueryPasskeysConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryPasskeysConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Passkey"] = None


class QueryProjectTokensConnection(_Base):
    edges: Optional[list["QueryProjectTokensConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryProjectTokensConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["ProjectToken"] = None


class QueryProjectsConnection(_Base):
    edges: Optional[list["QueryProjectsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryProjectsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Project"] = None


class QuerySessionsConnection(_Base):
    edges: Optional[list["QuerySessionsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QuerySessionsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Session"] = None


class QuerySshPublicKeysConnection(_Base):
    edges: Optional[list["QuerySshPublicKeysConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QuerySshPublicKeysConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["SshPublicKey"] = None


class QueryTeamTemplatesConnection(_Base):
    edges: Optional[list["QueryTeamTemplatesConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryTeamTemplatesConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Template"] = None


class QueryTemplatesConnection(_Base):
    edges: Optional[list["QueryTemplatesConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryTemplatesConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Template"] = None


class QueryTrustedDomainsConnection(_Base):
    edges: Optional[list["QueryTrustedDomainsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryTrustedDomainsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["TrustedDomain"] = None


class QueryUserTemplatesConnection(_Base):
    edges: Optional[list["QueryUserTemplatesConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryUserTemplatesConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Template"] = None


class QueryWorkspaceIdentityProvidersConnection(_Base):
    edges: Optional[list["QueryWorkspaceIdentityProvidersConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryWorkspaceIdentityProvidersConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["WorkspaceIdentityProvider"] = None


class QueryWorkspaceTemplatesConnection(_Base):
    edges: Optional[list["QueryWorkspaceTemplatesConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class QueryWorkspaceTemplatesConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Template"] = None


class RecoveryCodes(_Base):
    recovery_codes: Optional[list[str]] = None


class ReferralInfo(_Base):
    code: Optional[str] = None
    id: Optional[str] = None
    referral_stats: Optional["ReferralStats"] = None
    status: Optional[str] = None


class ReferralStats(_Base):
    credited: Optional[int] = None
    pending: Optional[int] = None


class ReferralUser(_Base):
    code: Optional[str] = None
    id: Optional[str] = None
    status: Optional["ReferralStatus"] = None


class Region(_Base):
    country: Optional[str] = None
    deployment_constraints: Optional["RegionDeploymentConstraints"] = None
    location: Optional[str] = None
    name: Optional[str] = None
    railway_metal: Optional[bool] = None
    region: Optional[str] = None
    workspace_id: Optional[str] = None


class RegionDeploymentConstraints(_Base):
    admin_only: Optional[bool] = None
    deprecation_info: Optional["RegionDeprecationInfo"] = None
    runtime_exclusivity: Optional[list[str]] = None
    staging_only: Optional[bool] = None


class RegionDeprecationInfo(_Base):
    is_deprecated: Optional[bool] = None
    replacement_region: Optional[str] = None


class ResourceAccess(_Base):
    deployment: Optional["AccessRule"] = None
    project: Optional["AccessRule"] = None


class Service(_Base):
    created_at: Optional[str] = None
    deleted_at: Optional[str] = None
    deployments: Optional["ServiceDeploymentsConnection"] = None
    feature_flags: Optional[list["ActiveServiceFeatureFlag"]] = None
    has_hidden_registry_credentials_from_template: Optional[bool] = None
    icon: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    project: Optional["Project"] = None
    project_id: Optional[str] = None
    repo_triggers: Optional["ServiceRepoTriggersConnection"] = None
    service_instances: Optional["ServiceServiceInstancesConnection"] = None
    template_id: Optional[str] = None
    template_service_id: Optional[str] = None
    template_thread_slug: Optional[str] = None
    updated_at: Optional[str] = None


class ServiceBackupInfo(_Base):
    schedules: Optional[list["VolumeInstanceBackupScheduleKind"]] = None
    service_id: Optional[str] = None
    service_name: Optional[str] = None


class ServiceDeploymentsConnection(_Base):
    edges: Optional[list["ServiceDeploymentsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class ServiceDeploymentsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Deployment"] = None


class ServiceDomain(_Base):
    cdn_mode: Optional[str] = None
    created_at: Optional[str] = None
    deleted_at: Optional[str] = None
    domain: Optional[str] = None
    edge_id: Optional[str] = None
    environment_id: Optional[str] = None
    id: Optional[str] = None
    new_domain_name: Optional[str] = None
    new_host_label: Optional[str] = None
    project_id: Optional[str] = None
    service_id: Optional[str] = None
    suffix: Optional[str] = None
    sync_status: Optional["ServiceDomainSyncStatus"] = None
    target_port: Optional[int] = None
    updated_at: Optional[str] = None


class ServiceInstance(_Base):
    active_deployments: Optional[list["Deployment"]] = None
    build_command: Optional[str] = None
    builder: Optional["Builder"] = None
    created_at: Optional[str] = None
    cron_schedule: Optional[str] = None
    deleted_at: Optional[str] = None
    dockerfile_path: Optional[str] = None
    domains: Optional["AllDomains"] = None
    draining_seconds: Optional[int] = None
    environment_id: Optional[str] = None
    healthcheck_path: Optional[str] = None
    healthcheck_timeout: Optional[int] = None
    id: Optional[str] = None
    ipv6_egress_enabled: Optional[bool] = None
    is_updatable: Optional[bool] = None
    latest_deployment: Optional["Deployment"] = None
    next_cron_run_at: Optional[str] = None
    nixpacks_plan: Optional[Any] = None
    num_replicas: Optional[int] = None
    overlap_seconds: Optional[int] = None
    pre_deploy_command: Optional[Any] = None
    railpack_info: Optional[Any] = None
    railway_config_file: Optional[str] = None
    region: Optional[str] = None
    restart_policy_max_retries: Optional[int] = None
    restart_policy_type: Optional["RestartPolicyType"] = None
    root_directory: Optional[str] = None
    service: Optional["Service"] = None
    service_id: Optional[str] = None
    service_name: Optional[str] = None
    sleep_application: Optional[bool] = None
    source: Optional["ServiceSource"] = None
    start_command: Optional[str] = None
    updated_at: Optional[str] = None
    upstream_url: Optional[str] = None
    watch_patterns: Optional[list[str]] = None


class ServiceRepoTriggersConnection(_Base):
    edges: Optional[list["ServiceRepoTriggersConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class ServiceRepoTriggersConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["DeploymentTrigger"] = None


class ServiceServiceInstancesConnection(_Base):
    edges: Optional[list["ServiceServiceInstancesConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class ServiceServiceInstancesConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["ServiceInstance"] = None


class ServiceSource(_Base):
    image: Optional[str] = None
    repo: Optional[str] = None


class Session(_Base):
    created_at: Optional[str] = None
    expired_at: Optional[str] = None
    id: Optional[str] = None
    is_current: Optional[bool] = None
    name: Optional[str] = None
    type: Optional["SessionType"] = None
    updated_at: Optional[str] = None


class SimilarTemplate(_Base):
    code: Optional[str] = None
    created_at: Optional[str] = None
    creator: Optional["TemplateCreator"] = None
    deploys: Optional[int] = None
    description: Optional[str] = None
    health: Optional[float] = None
    image: Optional[str] = None
    name: Optional[str] = None
    team_id: Optional[str] = None
    user_id: Optional[str] = None
    workspace_id: Optional[str] = None


class SpendCommitment(_Base):
    features: Optional[list[Any]] = None
    id: Optional[str] = None
    min_spend_amount_cents: Optional[int] = None


class SshPublicKey(_Base):
    created_at: Optional[str] = None
    fingerprint: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    public_key: Optional[str] = None
    updated_at: Optional[str] = None


class SubscriptionDiscount(_Base):
    coupon_id: Optional[str] = None
    coupon_name: Optional[str] = None


class SubscriptionItem(_Base):
    item_id: Optional[str] = None
    price_dollars: Optional[float] = None
    price_id: Optional[str] = None
    product_id: Optional[str] = None
    quantity: Optional[int] = None


class TCPProxy(_Base):
    application_port: Optional[int] = None
    created_at: Optional[str] = None
    deleted_at: Optional[str] = None
    domain: Optional[str] = None
    environment_id: Optional[str] = None
    id: Optional[str] = None
    proxy_port: Optional[int] = None
    service_id: Optional[str] = None
    sync_status: Optional["TCPProxySyncStatus"] = None
    updated_at: Optional[str] = None


class Team(_Base):
    adoption_history: Optional[list["AdoptionInfo"]] = None
    adoption_level: Optional[float] = None
    api_token_rate_limit: Optional["ApiTokenRateLimit"] = None
    avatar: Optional[str] = None
    created_at: Optional[str] = None
    customer: Optional["Customer"] = None
    id: Optional[str] = None
    members: Optional[list["TeamMember"]] = None
    name: Optional[str] = None
    preferred_region: Optional[str] = None
    projects: Optional["TeamProjectsConnection"] = None
    slack_channel_id: Optional[str] = None
    support_tier_override: Optional["SupportTierOverride"] = None
    team_permissions: Optional[list["TeamPermission"]] = None
    updated_at: Optional[str] = None
    workspace: Optional["Workspace"] = None


class TeamMember(_Base):
    avatar: Optional[str] = None
    email: Optional[str] = None
    feature_flags: Optional[list["ActiveFeatureFlag"]] = None
    id: Optional[str] = None
    name: Optional[str] = None
    role: Optional["TeamRole"] = None


class TeamPermission(_Base):
    created_at: Optional[str] = None
    id: Optional[str] = None
    role: Optional["TeamRole"] = None
    updated_at: Optional[str] = None
    user_id: Optional[str] = None
    workspace_id: Optional[str] = None


class TeamProjectsConnection(_Base):
    edges: Optional[list["TeamProjectsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class TeamProjectsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Project"] = None


class Template(_Base):
    active_projects: Optional[int] = None
    canvas_config: Optional[Any] = None
    category: Optional[str] = None
    code: Optional[str] = None
    community_thread_slug: Optional[str] = None
    config: Optional[Any] = None
    created_at: Optional[str] = None
    creator: Optional["TemplateCreator"] = None
    demo_project_id: Optional[str] = None
    description: Optional[str] = None
    guides: Optional["TemplateGuide"] = None
    health: Optional[float] = None
    id: Optional[str] = None
    image: Optional[str] = None
    is_approved: Optional[bool] = None
    is_v2_template: Optional[bool] = None
    is_verified: Optional[bool] = None
    languages: Optional[list[str]] = None
    metadata: Optional[Any] = None
    name: Optional[str] = None
    projects: Optional[int] = None
    readme: Optional[str] = None
    recent_projects: Optional[int] = None
    serialized_config: Optional[Any] = None
    services: Optional["TemplateServicesConnection"] = None
    similar_templates: Optional[list["SimilarTemplate"]] = None
    status: Optional["TemplateStatus"] = None
    support_health_metrics: Optional[Any] = None
    tags: Optional[list[str]] = None
    team_id: Optional[str] = None
    total_payout: Optional[float] = None
    workspace_id: Optional[str] = None


class TemplateCreator(_Base):
    avatar: Optional[str] = None
    has_public_profile: Optional[bool] = None
    name: Optional[str] = None
    username: Optional[str] = None


class TemplateDeployPayload(_Base):
    project_id: Optional[str] = None
    workflow_id: Optional[str] = None


class TemplateGuide(_Base):
    post: Optional[str] = None
    video: Optional[str] = None


class TemplateMetrics(_Base):
    active_deployments: Optional[int] = None
    deployments_last90_days: Optional[int] = None
    earnings_last30_days: Optional[float] = None
    earnings_last90_days: Optional[float] = None
    eligible_for_support_bonus: Optional[bool] = None
    support_health: Optional[float] = None
    template_health: Optional[float] = None
    total_deployments: Optional[int] = None
    total_earnings: Optional[float] = None


class TemplateService(_Base):
    config: Optional[Any] = None
    created_at: Optional[str] = None
    id: Optional[str] = None
    template_id: Optional[str] = None
    updated_at: Optional[str] = None


class TemplateServicesConnection(_Base):
    edges: Optional[list["TemplateServicesConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class TemplateServicesConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["TemplateService"] = None


class TrustedDomain(_Base):
    domain_name: Optional[str] = None
    id: Optional[str] = None
    role: Optional[str] = None
    status: Optional["TrustedDomainStatus"] = None
    verification_data: Optional["TrustedDomainVerificationData"] = None
    verification_type: Optional[str] = None
    workspace_id: Optional[str] = None


class TrustedDomainVerificationData(_Base):
    dns_host: Optional[str] = None
    domain_match: Optional["Domain"] = None
    domain_status: Optional["CustomDomainStatus"] = None
    token: Optional[str] = None


class TwoFactorInfo(_Base):
    has_recovery_codes: Optional[bool] = None
    is_verified: Optional[bool] = None


class TwoFactorInfoSecret(_Base):
    secret: Optional[str] = None
    uri: Optional[str] = None


class UsageLimit(_Base):
    customer_id: Optional[str] = None
    hard_limit: Optional[int] = None
    id: Optional[str] = None
    is_over_limit: Optional[bool] = None
    soft_limit: Optional[int] = None


class User(_Base):
    agreed_fair_use: Optional[bool] = None
    api_token_rate_limit: Optional["ApiTokenRateLimit"] = None
    avatar: Optional[str] = None
    ban_reason: Optional[str] = None
    created_at: Optional[str] = None
    email: Optional[str] = None
    feature_flags: Optional[list["ActiveFeatureFlag"]] = None
    flags: Optional[list["UserFlag"]] = None
    github_provider_id: Optional[str] = None
    github_username: Optional[str] = None
    has2_fa: Optional[bool] = None
    has_passkeys: Optional[bool] = None
    id: Optional[str] = None
    is_admin: Optional[bool] = None
    is_conductor: Optional[bool] = None
    is_verified: Optional[bool] = None
    last_login: Optional[str] = None
    name: Optional[str] = None
    platform_feature_flags: Optional[list["ActivePlatformFlag"]] = None
    profile: Optional["UserProfile"] = None
    projects: Optional["UserProjectsConnection"] = None
    provider_auths: Optional["UserProviderAuthsConnection"] = None
    registration_status: Optional["RegistrationStatus"] = None
    risk_level: Optional[float] = None
    terms_agreed_on: Optional[str] = None
    username: Optional[str] = None
    workspace: Optional["Workspace"] = None
    workspaces: Optional[list["Workspace"]] = None


class UserKickbackEarnings(_Base):
    total_amount: Optional[float] = None


class UserProfile(_Base):
    bio: Optional[str] = None
    is_public: Optional[bool] = None
    website: Optional[str] = None


class UserProfileResponse(_Base):
    avatar: Optional[str] = None
    created_at: Optional[str] = None
    customer_id: Optional[str] = None
    id: Optional[str] = None
    is_trialing: Optional[bool] = None
    name: Optional[str] = None
    profile: Optional["UserProfile"] = None
    public_projects: Optional["UserProfileResponsePublicProjectsConnection"] = None
    published_templates: Optional[list["SimilarTemplate"]] = None
    state: Optional[str] = None
    total_deploys: Optional[int] = None
    username: Optional[str] = None


class UserProfileResponsePublicProjectsConnection(_Base):
    edges: Optional[list["UserProfileResponsePublicProjectsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class UserProfileResponsePublicProjectsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Project"] = None


class UserProjectsConnection(_Base):
    edges: Optional[list["UserProjectsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class UserProjectsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Project"] = None


class UserProviderAuthsConnection(_Base):
    edges: Optional[list["UserProviderAuthsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class UserProviderAuthsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["ProviderAuth"] = None


class Variable(_Base):
    created_at: Optional[str] = None
    environment: Optional["Environment"] = None
    environment_id: Optional[str] = None
    id: Optional[str] = None
    is_sealed: Optional[bool] = None
    name: Optional[str] = None
    plugin: Optional["Plugin"] = None
    plugin_id: Optional[str] = None
    references: Optional[list[str]] = None
    service: Optional["Service"] = None
    service_id: Optional[str] = None
    updated_at: Optional[str] = None


class VercelAccount(_Base):
    id: Optional[str] = None
    integration_auth_id: Optional[str] = None
    is_user: Optional[bool] = None
    name: Optional[str] = None
    projects: Optional[list["VercelProject"]] = None
    slug: Optional[str] = None


class VercelInfo(_Base):
    accounts: Optional[list["VercelAccount"]] = None


class VercelProject(_Base):
    account_id: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None


class Volume(_Base):
    created_at: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    project: Optional["Project"] = None
    project_id: Optional[str] = None
    volume_instances: Optional["VolumeVolumeInstancesConnection"] = None


class VolumeInstance(_Base):
    created_at: Optional[str] = None
    current_size_mb: Optional[float] = None
    environment: Optional["Environment"] = None
    environment_id: Optional[str] = None
    external_id: Optional[str] = None
    id: Optional[str] = None
    mount_path: Optional[str] = None
    region: Optional[str] = None
    service: Optional["Service"] = None
    service_id: Optional[str] = None
    size_mb: Optional[int] = None
    state: Optional["VolumeState"] = None
    volume: Optional["Volume"] = None
    volume_id: Optional[str] = None


class VolumeInstanceBackup(_Base):
    created_at: Optional[str] = None
    creator_id: Optional[str] = None
    expires_at: Optional[str] = None
    external_id: Optional[str] = None
    id: Optional[str] = None
    name: Optional[str] = None
    referenced_mb: Optional[int] = None
    schedule_id: Optional[str] = None
    used_mb: Optional[int] = None
    volume_instance_size_mb: Optional[int] = None


class VolumeInstanceBackupSchedule(_Base):
    created_at: Optional[str] = None
    cron: Optional[str] = None
    id: Optional[str] = None
    kind: Optional["VolumeInstanceBackupScheduleKind"] = None
    name: Optional[str] = None
    retention_seconds: Optional[int] = None


class VolumeInstanceReplicationProgress(_Base):
    bytes_transferred: Optional[int] = None
    percent_complete: Optional[float] = None
    timestamp: Optional[str] = None
    transfer_rate_mbps: Optional[float] = None


class VolumeReplicationProgressUpdate(_Base):
    current_snapshot: Optional["VolumeSnapshotReplicationProgressUpdate"] = None
    dest_external_id: Optional[str] = None
    dest_region: Optional[str] = None
    dest_stacker_id: Optional[str] = None
    error: Optional[str] = None
    estimated_time_remaining_ms: Optional[int] = None
    history: Optional[list["VolumeInstanceReplicationProgress"]] = None
    nb_snapshots: Optional[int] = None
    offline_bytes_transferred: Optional[int] = None
    offline_total_bytes: Optional[int] = None
    online_bytes_transferred: Optional[int] = None
    online_total_bytes: Optional[int] = None
    percent_complete: Optional[float] = None
    snapshots_sizes: Optional[list[int]] = None
    src_external_id: Optional[str] = None
    src_region: Optional[str] = None
    src_stacker_id: Optional[str] = None
    status: Optional["ReplicateVolumeInstanceStatus"] = None
    transfer_rate_mbps: Optional[float] = None


class VolumeSnapshotReplicationProgressUpdate(_Base):
    bytes_transferred: Optional[int] = None
    compressed_bytes_transferred: Optional[int] = None
    compressed_transfer_rate_mbps: Optional[float] = None
    elapsed_ms: Optional[int] = None
    error: Optional[str] = None
    estimated_time_remaining_ms: Optional[int] = None
    index: Optional[int] = None
    percent_complete: Optional[float] = None
    started_at: Optional[str] = None
    status: Optional["ReplicateVolumeInstanceSnapshotStatus"] = None
    total_bytes: Optional[int] = None
    transfer_rate_mbps: Optional[float] = None


class VolumeVolumeInstancesConnection(_Base):
    edges: Optional[list["VolumeVolumeInstancesConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class VolumeVolumeInstancesConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["VolumeInstance"] = None


class WorkflowId(_Base):
    workflow_id: Optional[str] = None


class WorkflowResult(_Base):
    error: Optional[str] = None
    status: Optional["WorkflowStatus"] = None


class Workspace(_Base):
    adoption_history: Optional[list["AdoptionInfo"]] = None
    adoption_level: Optional[float] = None
    allow_deprecated_regions: Optional[bool] = None
    api_token_rate_limit: Optional["ApiTokenRateLimit"] = None
    avatar: Optional[str] = None
    ban_reason: Optional[str] = None
    created_at: Optional[str] = None
    customer: Optional["Customer"] = None
    discord_role: Optional[str] = None
    has2_fa_enforcement: Optional[bool] = None
    has_guardrails_access: Optional[bool] = None
    has_saml: Optional[bool] = None
    id: Optional[str] = None
    identity_providers: Optional["WorkspaceIdentityProvidersConnection"] = None
    members: Optional[list["WorkspaceMember"]] = None
    name: Optional[str] = None
    partner_profile: Optional["PartnerProfile"] = None
    plan: Optional["Plan"] = None
    preferred_region: Optional[str] = None
    projects: Optional["WorkspaceProjectsConnection"] = None
    redacted_due_to2_fa_pending: Optional[bool] = None
    referred_users: Optional[list["ReferralUser"]] = None
    slack_channel_id: Optional[str] = None
    subscription_model: Optional["SubscriptionModel"] = None
    subscription_plan_limit: Optional[Any] = None
    support_tier_override: Optional["SupportTierOverride"] = None
    team: Optional["Team"] = None
    updated_at: Optional[str] = None
    users_without2_fa: Optional[list[str]] = None


class WorkspaceIdPConnection(_Base):
    created_at: Optional[str] = None
    provider: Optional[str] = None
    status: Optional["WorkspaceIdPConnectionStatus"] = None
    updated_at: Optional[str] = None


class WorkspaceIdentityProvider(_Base):
    connection: Optional["WorkspaceIdPConnection"] = None
    created_at: Optional[str] = None
    enforcement_enabled_at: Optional[str] = None
    id: Optional[str] = None
    updated_at: Optional[str] = None
    workspace: Optional["Workspace"] = None
    workspace_id: Optional[str] = None


class WorkspaceIdentityProvidersConnection(_Base):
    edges: Optional[list["WorkspaceIdentityProvidersConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class WorkspaceIdentityProvidersConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["WorkspaceIdentityProvider"] = None


class WorkspaceMember(_Base):
    avatar: Optional[str] = None
    email: Optional[str] = None
    feature_flags: Optional[list["ActiveFeatureFlag"]] = None
    id: Optional[str] = None
    name: Optional[str] = None
    role: Optional["TeamRole"] = None
    two_factor_auth_enabled: Optional[bool] = None


class WorkspacePolicy(_Base):
    id: Optional[str] = None
    restrict_public_tcp_proxies: Optional[bool] = None
    restrict_railway_domain_generation: Optional[bool] = None


class WorkspaceProjectsConnection(_Base):
    edges: Optional[list["WorkspaceProjectsConnectionEdge"]] = None
    page_info: Optional["PageInfo"] = None


class WorkspaceProjectsConnectionEdge(_Base):
    cursor: Optional[str] = None
    node: Optional["Project"] = None

