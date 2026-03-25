from __future__ import annotations

from typing import Any, Optional

import httpx
from pydantic import BaseModel, TypeAdapter

from .enums import *  # noqa: F401,F403
from .inputs import *  # noqa: F401,F403
from .types import *  # noqa: F401,F403


def _prepare_input(obj: Any) -> Any:
    """Recursively serialize inputs for GraphQL variables."""
    if isinstance(obj, BaseModel):
        return obj.model_dump(by_alias=True, exclude_none=True)
    if isinstance(obj, dict):
        return {k: _prepare_input(v) for k, v in obj.items() if v is not None}
    if isinstance(obj, list):
        return [_prepare_input(v) for v in obj]
    if isinstance(obj, Enum):
        return obj.value
    return obj


class RailwayError(Exception):
    """Raised when the Railway GraphQL API returns errors."""

    def __init__(self, errors: list[dict], data: Any = None):
        self.errors = errors
        self.data = data
        messages = "; ".join(e.get("message", str(e)) for e in errors)
        super().__init__(messages)


class RailwayClient:
    """Typed Python client for the Railway GraphQL API (v2)."""

    ENDPOINT = "https://backboard.railway.com/graphql/v2"

    def __init__(
        self,
        *,
        api_token: str | None = None,
        project_token: str | None = None,
        endpoint: str | None = None,
        timeout: float = 30.0,
    ):
        """
        Create a new Railway API client.

        Provide exactly one of api_token or project_token.

        Args:
            api_token: Railway API token (account or workspace scope).
            project_token: Railway project-scoped token.
            endpoint: Override the default API endpoint.
            timeout: Request timeout in seconds.
        """
        if api_token and project_token:
            raise ValueError("Provide exactly one of api_token or project_token, not both.")
        if not api_token and not project_token:
            raise ValueError("Provide either api_token or project_token.")
        self._endpoint = endpoint or self.ENDPOINT
        self._timeout = timeout
        if project_token:
            self._headers = {"Content-Type": "application/json", "Project-Access-Token": project_token}
        else:
            self._headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_token}"}
        self._client = httpx.Client(timeout=timeout)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> RailwayClient:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def _execute(self, query: str, variables: dict[str, Any] | None = None) -> Any:
        """Execute a raw GraphQL query and return the data dict."""
        payload: dict[str, Any] = {"query": query}
        if variables:
            payload["variables"] = variables
        resp = self._client.post(self._endpoint, headers=self._headers, json=payload)
        resp.raise_for_status()
        body = resp.json()
        if "errors" in body:
            raise RailwayError(body["errors"], body.get("data"))
        return body.get("data")

    # ── Queries ────────────────────────────────────────────

    def admin_volume_instances_for_volume(self, volume_id: str) -> list["VolumeInstance"]:
        query = """query($volumeId: String!) { adminVolumeInstancesForVolume(volumeId: $volumeId) { createdAt currentSizeMB environmentId externalId id mountPath region serviceId sizeMB volumeId environment { canAccess createdAt deletedAt id isEphemeral name projectId unmergedChangesCount updatedAt } service { createdAt deletedAt hasHiddenRegistryCredentialsFromTemplate icon id name projectId templateId templateServiceId templateThreadSlug updatedAt } volume { createdAt id name projectId } } }"""
        variables: dict[str, Any] = {
            "volumeId": _prepare_input(volume_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("adminVolumeInstancesForVolume")
        return TypeAdapter(list["VolumeInstance"]).validate_python(_data) if _data else []

    def all_platform_feature_flags(self) -> list["PlatformFeatureFlagStatus"]:
        query = """query { allPlatformFeatureFlags { rolloutPercentage status } }"""
        _data = self._execute(query).get("allPlatformFeatureFlags")
        return TypeAdapter(list["PlatformFeatureFlagStatus"]).validate_python(_data) if _data else []

    def api_token(self) -> "ApiTokenContext":
        query = """query { apiToken { workspaces { id name } } }"""
        return ApiTokenContext.model_validate(self._execute(query).get("apiToken"))

    def api_tokens(self, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, last: Optional[int] = None) -> "QueryApiTokensConnection":
        query = """query($after: String, $before: String, $first: Int, $last: Int) { apiTokens(after: $after, before: $before, first: $first, last: $last) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "first": _prepare_input(first),
            "last": _prepare_input(last),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryApiTokensConnection.model_validate(self._execute(query, variables).get("apiTokens"))

    def audit_log(self, id: str, workspace_id: str) -> "AuditLog":
        query = """query($id: String!, $workspaceId: String!) { auditLog(id: $id, workspaceId: $workspaceId) { context createdAt environmentId eventType id payload projectId workspaceId environment { canAccess createdAt deletedAt id isEphemeral name projectId unmergedChangesCount updatedAt } project { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return AuditLog.model_validate(self._execute(query, variables).get("auditLog"))

    def audit_log_event_type_info(self) -> list["AuditLogEventTypeInfo"]:
        query = """query { auditLogEventTypeInfo { description eventType } }"""
        _data = self._execute(query).get("auditLogEventTypeInfo")
        return TypeAdapter(list["AuditLogEventTypeInfo"]).validate_python(_data) if _data else []

    def audit_logs(self, workspace_id: str, *, after: Optional[str] = None, before: Optional[str] = None, end_date: Optional[str] = None, environment_id: Optional[str] = None, event_types: Optional[list[str]] = None, project_id: Optional[str] = None, start_date: Optional[str] = None, first: Optional[int] = None, last: Optional[int] = None, sort: Optional["SortOrder"] = None) -> "QueryAuditLogsConnection":
        query = """query($after: String, $before: String, $filter: AuditLogFilterInput, $first: Int, $last: Int, $sort: SortOrder, $workspaceId: String!) { auditLogs(after: $after, before: $before, filter: $filter, first: $first, last: $last, sort: $sort, workspaceId: $workspaceId) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "filter": _prepare_input(AuditLogFilterInput(end_date=end_date, environment_id=environment_id, event_types=event_types, project_id=project_id, start_date=start_date)),
            "first": _prepare_input(first),
            "last": _prepare_input(last),
            "sort": _prepare_input(sort),
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryAuditLogsConnection.model_validate(self._execute(query, variables).get("auditLogs"))

    def bucket_instance_details(self, bucket_id: str, environment_id: str) -> Optional["BucketInstanceDetails"]:
        query = """query($bucketId: String!, $environmentId: String!) { bucketInstanceDetails(bucketId: $bucketId, environmentId: $environmentId) { objectCount sizeBytes } }"""
        variables: dict[str, Any] = {
            "bucketId": _prepare_input(bucket_id),
            "environmentId": _prepare_input(environment_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("bucketInstanceDetails")
        return BucketInstanceDetails.model_validate(_data) if _data else None

    def bucket_s3_credentials(self, bucket_id: str, environment_id: str, project_id: str) -> list["BucketS3CompatibleCredentials"]:
        query = """query($bucketId: String!, $environmentId: String!, $projectId: String!) { bucketS3Credentials(bucketId: $bucketId, environmentId: $environmentId, projectId: $projectId) { accessKeyId bucketName createdAt endpoint region secretAccessKey urlStyle } }"""
        variables: dict[str, Any] = {
            "bucketId": _prepare_input(bucket_id),
            "environmentId": _prepare_input(environment_id),
            "projectId": _prepare_input(project_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("bucketS3Credentials")
        return TypeAdapter(list["BucketS3CompatibleCredentials"]).validate_python(_data) if _data else []

    def build_logs(self, deployment_id: str, *, end_date: Optional[str] = None, filter: Optional[str] = None, limit: Optional[int] = None, start_date: Optional[str] = None) -> list["Log"]:
        query = """query($deploymentId: String!, $endDate: DateTime, $filter: String, $limit: Int, $startDate: DateTime) { buildLogs(deploymentId: $deploymentId, endDate: $endDate, filter: $filter, limit: $limit, startDate: $startDate) { message severity timestamp attributes { key value } tags { deploymentId deploymentInstanceId environmentId pluginId projectId serviceId snapshotId } } }"""
        variables: dict[str, Any] = {
            "deploymentId": _prepare_input(deployment_id),
            "endDate": _prepare_input(end_date),
            "filter": _prepare_input(filter),
            "limit": _prepare_input(limit),
            "startDate": _prepare_input(start_date),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("buildLogs")
        return TypeAdapter(list["Log"]).validate_python(_data) if _data else []

    def canvas_view_merge_preview(self, source_environment_id: str, target_environment_id: str) -> "CanvasViewMergePreview":
        query = """query($sourceEnvironmentId: String!, $targetEnvironmentId: String!) { canvasViewMergePreview(sourceEnvironmentId: $sourceEnvironmentId, targetEnvironmentId: $targetEnvironmentId) { mutations state } }"""
        variables: dict[str, Any] = {
            "sourceEnvironmentId": _prepare_input(source_environment_id),
            "targetEnvironmentId": _prepare_input(target_environment_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return CanvasViewMergePreview.model_validate(self._execute(query, variables).get("canvasViewMergePreview"))

    def changelog_block_image(self, id: str) -> str:
        query = """query($id: String!) { changelogBlockImage(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("changelogBlockImage")

    def compliance_agreements(self, workspace_id: str) -> "ComplianceAgreementsInfo":
        query = """query($workspaceId: String!) { complianceAgreements(workspaceId: $workspaceId) { hasBAA hasDPA } }"""
        variables: dict[str, Any] = {
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return ComplianceAgreementsInfo.model_validate(self._execute(query, variables).get("complianceAgreements"))

    def custom_domain(self, id: str, project_id: str) -> "CustomDomain":
        query = """query($id: String!, $projectId: String!) { customDomain(id: $id, projectId: $projectId) { cdnMode createdAt deletedAt domain edgeId environmentId id projectId serviceId targetPort updatedAt cnameCheck { link message } status { certificateErrorMessage certificateRetryable verificationDnsHost verificationToken verified } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "projectId": _prepare_input(project_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return CustomDomain.model_validate(self._execute(query, variables).get("customDomain"))

    def custom_domain_available(self, domain: str) -> "DomainAvailable":
        query = """query($domain: String!) { customDomainAvailable(domain: $domain) { available message } }"""
        variables: dict[str, Any] = {
            "domain": _prepare_input(domain),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return DomainAvailable.model_validate(self._execute(query, variables).get("customDomainAvailable"))

    def deployment(self, id: str) -> "Deployment":
        query = """query($id: String!) { deployment(id: $id) { canRedeploy canRollback createdAt deploymentStopped diagnosis environmentId id meta projectId serviceId snapshotId staticUrl statusUpdatedAt suggestAddServiceDomain updatedAt url creator { avatar email id name } environment { canAccess createdAt deletedAt id isEphemeral name projectId unmergedChangesCount updatedAt } instances { id } service { createdAt deletedAt hasHiddenRegistryCredentialsFromTemplate icon id name projectId templateId templateServiceId templateThreadSlug updatedAt } sockets { ipv6 port processName updatedAt } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Deployment.model_validate(self._execute(query, variables).get("deployment"))

    def deployment_events(self, id: str, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, last: Optional[int] = None) -> "QueryDeploymentEventsConnection":
        query = """query($after: String, $before: String, $first: Int, $id: String!, $last: Int) { deploymentEvents(after: $after, before: $before, first: $first, id: $id, last: $last) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "first": _prepare_input(first),
            "id": _prepare_input(id),
            "last": _prepare_input(last),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryDeploymentEventsConnection.model_validate(self._execute(query, variables).get("deploymentEvents"))

    def deployment_instance_executions(self, environment_id: str, service_id: str, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, last: Optional[int] = None) -> "QueryDeploymentInstanceExecutionsConnection":
        query = """query($after: String, $before: String, $first: Int, $input: DeploymentInstanceExecutionListInput!, $last: Int) { deploymentInstanceExecutions(after: $after, before: $before, first: $first, input: $input, last: $last) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "first": _prepare_input(first),
            "input": _prepare_input(DeploymentInstanceExecutionListInput(environment_id=environment_id, service_id=service_id)),
            "last": _prepare_input(last),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryDeploymentInstanceExecutionsConnection.model_validate(self._execute(query, variables).get("deploymentInstanceExecutions"))

    def deployment_logs(self, deployment_id: str, *, end_date: Optional[str] = None, filter: Optional[str] = None, limit: Optional[int] = None, start_date: Optional[str] = None) -> list["Log"]:
        query = """query($deploymentId: String!, $endDate: DateTime, $filter: String, $limit: Int, $startDate: DateTime) { deploymentLogs(deploymentId: $deploymentId, endDate: $endDate, filter: $filter, limit: $limit, startDate: $startDate) { message severity timestamp attributes { key value } tags { deploymentId deploymentInstanceId environmentId pluginId projectId serviceId snapshotId } } }"""
        variables: dict[str, Any] = {
            "deploymentId": _prepare_input(deployment_id),
            "endDate": _prepare_input(end_date),
            "filter": _prepare_input(filter),
            "limit": _prepare_input(limit),
            "startDate": _prepare_input(start_date),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("deploymentLogs")
        return TypeAdapter(list["Log"]).validate_python(_data) if _data else []

    def deployment_snapshot(self, deployment_id: str) -> Optional["DeploymentSnapshot"]:
        query = """query($deploymentId: String!) { deploymentSnapshot(deploymentId: $deploymentId) { createdAt id updatedAt variables } }"""
        variables: dict[str, Any] = {
            "deploymentId": _prepare_input(deployment_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("deploymentSnapshot")
        return DeploymentSnapshot.model_validate(_data) if _data else None

    def deployment_triggers(self, environment_id: str, project_id: str, service_id: str, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, last: Optional[int] = None) -> "QueryDeploymentTriggersConnection":
        query = """query($after: String, $before: String, $environmentId: String!, $first: Int, $last: Int, $projectId: String!, $serviceId: String!) { deploymentTriggers(after: $after, before: $before, environmentId: $environmentId, first: $first, last: $last, projectId: $projectId, serviceId: $serviceId) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "environmentId": _prepare_input(environment_id),
            "first": _prepare_input(first),
            "last": _prepare_input(last),
            "projectId": _prepare_input(project_id),
            "serviceId": _prepare_input(service_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryDeploymentTriggersConnection.model_validate(self._execute(query, variables).get("deploymentTriggers"))

    def deployments(self, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, environment_id: Optional[str] = None, include_deleted: Optional[bool] = None, project_id: Optional[str] = None, service_id: Optional[str] = None, status: Optional["DeploymentStatusInput"] = None, last: Optional[int] = None) -> "QueryDeploymentsConnection":
        query = """query($after: String, $before: String, $first: Int, $input: DeploymentListInput!, $last: Int) { deployments(after: $after, before: $before, first: $first, input: $input, last: $last) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "first": _prepare_input(first),
            "input": _prepare_input(DeploymentListInput(environment_id=environment_id, include_deleted=include_deleted, project_id=project_id, service_id=service_id, status=status)),
            "last": _prepare_input(last),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryDeploymentsConnection.model_validate(self._execute(query, variables).get("deployments"))

    def domain_status(self, id: str, project_id: str) -> "DomainWithStatus":
        query = """query($id: String!, $projectId: String!) { domainStatus(id: $id, projectId: $projectId) { certificateErrorMessage certificateRetryable certificates { domainNames expiresAt fingerprintSha256 issuedAt } dnsRecords { currentValue fqdn hostlabel requiredValue zone } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "projectId": _prepare_input(project_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return DomainWithStatus.model_validate(self._execute(query, variables).get("domainStatus"))

    def domains(self, environment_id: str, project_id: str, service_id: str) -> "AllDomains":
        query = """query($environmentId: String!, $projectId: String!, $serviceId: String!) { domains(environmentId: $environmentId, projectId: $projectId, serviceId: $serviceId) { customDomains { cdnMode createdAt deletedAt domain edgeId environmentId id projectId serviceId targetPort updatedAt } serviceDomains { cdnMode createdAt deletedAt domain edgeId environmentId id newDomainName newHostLabel projectId serviceId suffix targetPort updatedAt } } }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "projectId": _prepare_input(project_id),
            "serviceId": _prepare_input(service_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return AllDomains.model_validate(self._execute(query, variables).get("domains"))

    def egress_gateways(self, environment_id: str, service_id: str) -> list["EgressGateway"]:
        query = """query($environmentId: String!, $serviceId: String!) { egressGateways(environmentId: $environmentId, serviceId: $serviceId) { ipv4 region } }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "serviceId": _prepare_input(service_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("egressGateways")
        return TypeAdapter(list["EgressGateway"]).validate_python(_data) if _data else []

    def environment(self, id: str, *, project_id: Optional[str] = None) -> "Environment":
        query = """query($id: String!, $projectId: String) { environment(id: $id, projectId: $projectId) { canAccess createdAt deletedAt id isEphemeral name projectId unmergedChangesCount updatedAt meta { baseBranch branch latestSuccessfulGitHubDeploymentId prCommentId prNumber prRepo prTitle skippedResourceIds } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "projectId": _prepare_input(project_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Environment.model_validate(self._execute(query, variables).get("environment"))

    def environment_logs(self, environment_id: str, *, after_date: Optional[str] = None, after_limit: Optional[int] = None, anchor_date: Optional[str] = None, before_date: Optional[str] = None, before_limit: Optional[int] = None, filter: Optional[str] = None) -> list["Log"]:
        query = """query($afterDate: String, $afterLimit: Int, $anchorDate: String, $beforeDate: String, $beforeLimit: Int, $environmentId: String!, $filter: String) { environmentLogs(afterDate: $afterDate, afterLimit: $afterLimit, anchorDate: $anchorDate, beforeDate: $beforeDate, beforeLimit: $beforeLimit, environmentId: $environmentId, filter: $filter) { message severity timestamp attributes { key value } tags { deploymentId deploymentInstanceId environmentId pluginId projectId serviceId snapshotId } } }"""
        variables: dict[str, Any] = {
            "afterDate": _prepare_input(after_date),
            "afterLimit": _prepare_input(after_limit),
            "anchorDate": _prepare_input(anchor_date),
            "beforeDate": _prepare_input(before_date),
            "beforeLimit": _prepare_input(before_limit),
            "environmentId": _prepare_input(environment_id),
            "filter": _prepare_input(filter),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("environmentLogs")
        return TypeAdapter(list["Log"]).validate_python(_data) if _data else []

    def environment_patch(self, id: str) -> "EnvironmentPatch":
        query = """query($id: String!) { environmentPatch(id: $id) { appliedAt createdAt environmentId id lastAppliedError message updatedAt appliedBy { avatar email id name username } environment { canAccess createdAt deletedAt id isEphemeral name projectId unmergedChangesCount updatedAt } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return EnvironmentPatch.model_validate(self._execute(query, variables).get("environmentPatch"))

    def environment_patches(self, environment_id: str, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, last: Optional[int] = None) -> "QueryEnvironmentPatchesConnection":
        query = """query($after: String, $before: String, $environmentId: String!, $first: Int, $last: Int) { environmentPatches(after: $after, before: $before, environmentId: $environmentId, first: $first, last: $last) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "environmentId": _prepare_input(environment_id),
            "first": _prepare_input(first),
            "last": _prepare_input(last),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryEnvironmentPatchesConnection.model_validate(self._execute(query, variables).get("environmentPatches"))

    def environment_staged_changes(self, environment_id: str) -> "EnvironmentPatch":
        query = """query($environmentId: String!) { environmentStagedChanges(environmentId: $environmentId) { appliedAt createdAt environmentId id lastAppliedError message updatedAt appliedBy { avatar email id name username } environment { canAccess createdAt deletedAt id isEphemeral name projectId unmergedChangesCount updatedAt } } }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return EnvironmentPatch.model_validate(self._execute(query, variables).get("environmentStagedChanges"))

    def environments(self, project_id: str, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, is_ephemeral: Optional[bool] = None, last: Optional[int] = None) -> "QueryEnvironmentsConnection":
        query = """query($after: String, $before: String, $first: Int, $isEphemeral: Boolean, $last: Int, $projectId: String!) { environments(after: $after, before: $before, first: $first, isEphemeral: $isEphemeral, last: $last, projectId: $projectId) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "first": _prepare_input(first),
            "isEphemeral": _prepare_input(is_ephemeral),
            "last": _prepare_input(last),
            "projectId": _prepare_input(project_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryEnvironmentsConnection.model_validate(self._execute(query, variables).get("environments"))

    def estimated_usage(self, measurements: list["MetricMeasurement"], *, include_deleted: Optional[bool] = None, project_id: Optional[str] = None, workspace_id: Optional[str] = None) -> list["EstimatedUsage"]:
        query = """query($includeDeleted: Boolean, $measurements: [MetricMeasurement!]!, $projectId: String, $workspaceId: String) { estimatedUsage(includeDeleted: $includeDeleted, measurements: $measurements, projectId: $projectId, workspaceId: $workspaceId) { estimatedValue projectId } }"""
        variables: dict[str, Any] = {
            "includeDeleted": _prepare_input(include_deleted),
            "measurements": _prepare_input(measurements),
            "projectId": _prepare_input(project_id),
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("estimatedUsage")
        return TypeAdapter(list["EstimatedUsage"]).validate_python(_data) if _data else []

    def events(self, project_id: str, *, after: Optional[str] = None, before: Optional[str] = None, environment_id: Optional[str] = None, action: Optional["EventStringListFilter"] = None, object: Optional["EventStringListFilter"] = None, service_id: Optional["EventStringListFilter"] = None, first: Optional[int] = None, last: Optional[int] = None) -> "QueryEventsConnection":
        query = """query($after: String, $before: String, $environmentId: String, $filter: EventFilterInput, $first: Int, $last: Int, $projectId: String!) { events(after: $after, before: $before, environmentId: $environmentId, filter: $filter, first: $first, last: $last, projectId: $projectId) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "environmentId": _prepare_input(environment_id),
            "filter": _prepare_input(EventFilterInput(action=action, object=object, service_id=service_id)),
            "first": _prepare_input(first),
            "last": _prepare_input(last),
            "projectId": _prepare_input(project_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryEventsConnection.model_validate(self._execute(query, variables).get("events"))

    def external_workspaces(self, *, project_id: Optional[str] = None) -> list["ExternalWorkspace"]:
        query = """query($projectId: String) { externalWorkspaces(projectId: $projectId) { allowDeprecatedRegions avatar banReason createdAt currentSessionHasAccess customerId discordRole has2FAEnforcement hasBAA hasGuardrailsAccess hasRBAC hasSAML id isTrialing name preferredRegion redactedDueTo2FAPending subscriptionPlanLimit supportTierOverride teamId projects { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "projectId": _prepare_input(project_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("externalWorkspaces")
        return TypeAdapter(list["ExternalWorkspace"]).validate_python(_data) if _data else []

    def function_runtime(self, name: "FunctionRuntimeName") -> "FunctionRuntime":
        query = """query($name: FunctionRuntimeName!) { functionRuntime(name: $name) { image latestVersion { image tag } versions { image tag } } }"""
        variables: dict[str, Any] = {
            "name": _prepare_input(name),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return FunctionRuntime.model_validate(self._execute(query, variables).get("functionRuntime"))

    def function_runtimes(self) -> list["FunctionRuntime"]:
        query = """query { functionRuntimes { image latestVersion { image tag } versions { image tag } } }"""
        _data = self._execute(query).get("functionRuntimes")
        return TypeAdapter(list["FunctionRuntime"]).validate_python(_data) if _data else []

    def git_hub_repo_access_available(self, full_repo_name: str) -> "GitHubAccess":
        query = """query($fullRepoName: String!) { gitHubRepoAccessAvailable(fullRepoName: $fullRepoName) { hasAccess isPublic } }"""
        variables: dict[str, Any] = {
            "fullRepoName": _prepare_input(full_repo_name),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return GitHubAccess.model_validate(self._execute(query, variables).get("gitHubRepoAccessAvailable"))

    def git_hub_ssh_keys(self) -> list["GitHubSshKey"]:
        query = """query { gitHubSshKeys { id key title } }"""
        _data = self._execute(query).get("gitHubSshKeys")
        return TypeAdapter(list["GitHubSshKey"]).validate_python(_data) if _data else []

    def github_is_repo_name_available(self, full_repo_name: str) -> bool:
        query = """query($fullRepoName: String!) { githubIsRepoNameAvailable(fullRepoName: $fullRepoName) }"""
        variables: dict[str, Any] = {
            "fullRepoName": _prepare_input(full_repo_name),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("githubIsRepoNameAvailable")

    def github_pr_info(self, pr_number: int, service_id: str) -> Optional["GitHubPRInfo"]:
        query = """query($prNumber: Int!, $serviceId: String!) { githubPRInfo(prNumber: $prNumber, serviceId: $serviceId) { additions author body changedFiles deletions mergeable state title checks { name status } } }"""
        variables: dict[str, Any] = {
            "prNumber": _prepare_input(pr_number),
            "serviceId": _prepare_input(service_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("githubPRInfo")
        return GitHubPRInfo.model_validate(_data) if _data else None

    def github_repo(self, full_repo_name: str) -> "GitHubRepoWithoutInstallation":
        query = """query($fullRepoName: String!) { githubRepo(fullRepoName: $fullRepoName) { defaultBranch description fullName id isPrivate name } }"""
        variables: dict[str, Any] = {
            "fullRepoName": _prepare_input(full_repo_name),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return GitHubRepoWithoutInstallation.model_validate(self._execute(query, variables).get("githubRepo"))

    def github_repo_branches(self, owner: str, repo: str) -> list["GitHubBranch"]:
        query = """query($owner: String!, $repo: String!) { githubRepoBranches(owner: $owner, repo: $repo) { name } }"""
        variables: dict[str, Any] = {
            "owner": _prepare_input(owner),
            "repo": _prepare_input(repo),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("githubRepoBranches")
        return TypeAdapter(list["GitHubBranch"]).validate_python(_data) if _data else []

    def github_repos(self) -> list["GitHubRepo"]:
        query = """query { githubRepos { defaultBranch description fullName id installationId isPrivate name ownerAvatarUrl } }"""
        _data = self._execute(query).get("githubRepos")
        return TypeAdapter(list["GitHubRepo"]).validate_python(_data) if _data else []

    def github_writable_scopes(self) -> list[str]:
        query = """query { githubWritableScopes }"""
        return self._execute(query).get("githubWritableScopes")

    def heroku_apps(self) -> list["HerokuApp"]:
        query = """query { herokuApps { id name } }"""
        _data = self._execute(query).get("herokuApps")
        return TypeAdapter(list["HerokuApp"]).validate_python(_data) if _data else []

    def http_duration_metrics(self, end_date: str, environment_id: str, service_id: str, start_date: str, *, method: Optional[str] = None, path: Optional[str] = None, status_code: Optional[int] = None, step_seconds: Optional[int] = None) -> "HttpDurationMetricsResult":
        query = """query($endDate: DateTime!, $environmentId: String!, $method: String, $path: String, $serviceId: String!, $startDate: DateTime!, $statusCode: Int, $stepSeconds: Int) { httpDurationMetrics(endDate: $endDate, environmentId: $environmentId, method: $method, path: $path, serviceId: $serviceId, startDate: $startDate, statusCode: $statusCode, stepSeconds: $stepSeconds) { samples { p50 p90 p95 p99 ts } } }"""
        variables: dict[str, Any] = {
            "endDate": _prepare_input(end_date),
            "environmentId": _prepare_input(environment_id),
            "method": _prepare_input(method),
            "path": _prepare_input(path),
            "serviceId": _prepare_input(service_id),
            "startDate": _prepare_input(start_date),
            "statusCode": _prepare_input(status_code),
            "stepSeconds": _prepare_input(step_seconds),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return HttpDurationMetricsResult.model_validate(self._execute(query, variables).get("httpDurationMetrics"))

    def http_logs(self, deployment_id: str, *, after_date: Optional[str] = None, after_limit: Optional[int] = None, anchor_date: Optional[str] = None, before_date: Optional[str] = None, before_limit: Optional[int] = None, end_date: Optional[str] = None, filter: Optional[str] = None, limit: Optional[int] = None, start_date: Optional[str] = None) -> list["HttpLog"]:
        query = """query($afterDate: String, $afterLimit: Int, $anchorDate: String, $beforeDate: String, $beforeLimit: Int, $deploymentId: String!, $endDate: String, $filter: String, $limit: Int, $startDate: String) { httpLogs(afterDate: $afterDate, afterLimit: $afterLimit, anchorDate: $anchorDate, beforeDate: $beforeDate, beforeLimit: $beforeLimit, deploymentId: $deploymentId, endDate: $endDate, filter: $filter, limit: $limit, startDate: $startDate) { clientUa deploymentId deploymentInstanceId downstreamProto edgeRegion host httpStatus method path requestId responseDetails rxBytes srcIp timestamp totalDuration txBytes upstreamAddress upstreamErrors upstreamProto upstreamRqDuration } }"""
        variables: dict[str, Any] = {
            "afterDate": _prepare_input(after_date),
            "afterLimit": _prepare_input(after_limit),
            "anchorDate": _prepare_input(anchor_date),
            "beforeDate": _prepare_input(before_date),
            "beforeLimit": _prepare_input(before_limit),
            "deploymentId": _prepare_input(deployment_id),
            "endDate": _prepare_input(end_date),
            "filter": _prepare_input(filter),
            "limit": _prepare_input(limit),
            "startDate": _prepare_input(start_date),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("httpLogs")
        return TypeAdapter(list["HttpLog"]).validate_python(_data) if _data else []

    def http_metrics(self, end_date: str, environment_id: str, service_id: str, start_date: str, *, method: Optional[str] = None, path: Optional[str] = None, status_code: Optional[int] = None, step_seconds: Optional[int] = None) -> "HttpMetricsResult":
        query = """query($endDate: DateTime!, $environmentId: String!, $method: String, $path: String, $serviceId: String!, $startDate: DateTime!, $statusCode: Int, $stepSeconds: Int) { httpMetrics(endDate: $endDate, environmentId: $environmentId, method: $method, path: $path, serviceId: $serviceId, startDate: $startDate, statusCode: $statusCode, stepSeconds: $stepSeconds) { samples { ts value } } }"""
        variables: dict[str, Any] = {
            "endDate": _prepare_input(end_date),
            "environmentId": _prepare_input(environment_id),
            "method": _prepare_input(method),
            "path": _prepare_input(path),
            "serviceId": _prepare_input(service_id),
            "startDate": _prepare_input(start_date),
            "statusCode": _prepare_input(status_code),
            "stepSeconds": _prepare_input(step_seconds),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return HttpMetricsResult.model_validate(self._execute(query, variables).get("httpMetrics"))

    def http_metrics_grouped_by_status(self, end_date: str, environment_id: str, service_id: str, start_date: str, *, method: Optional[str] = None, path: Optional[str] = None, step_seconds: Optional[int] = None) -> list["HttpMetricsByStatusResult"]:
        query = """query($endDate: DateTime!, $environmentId: String!, $method: String, $path: String, $serviceId: String!, $startDate: DateTime!, $stepSeconds: Int) { httpMetricsGroupedByStatus(endDate: $endDate, environmentId: $environmentId, method: $method, path: $path, serviceId: $serviceId, startDate: $startDate, stepSeconds: $stepSeconds) { statusCode samples { ts value } } }"""
        variables: dict[str, Any] = {
            "endDate": _prepare_input(end_date),
            "environmentId": _prepare_input(environment_id),
            "method": _prepare_input(method),
            "path": _prepare_input(path),
            "serviceId": _prepare_input(service_id),
            "startDate": _prepare_input(start_date),
            "stepSeconds": _prepare_input(step_seconds),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("httpMetricsGroupedByStatus")
        return TypeAdapter(list["HttpMetricsByStatusResult"]).validate_python(_data) if _data else []

    def integration_auth(self, provider: str, provider_id: str) -> "IntegrationAuth":
        query = """query($provider: String!, $providerId: String!) { integrationAuth(provider: $provider, providerId: $providerId) { id provider providerId } }"""
        variables: dict[str, Any] = {
            "provider": _prepare_input(provider),
            "providerId": _prepare_input(provider_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return IntegrationAuth.model_validate(self._execute(query, variables).get("integrationAuth"))

    def integration_auths(self, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, last: Optional[int] = None) -> "QueryIntegrationAuthsConnection":
        query = """query($after: String, $before: String, $first: Int, $last: Int) { integrationAuths(after: $after, before: $before, first: $first, last: $last) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "first": _prepare_input(first),
            "last": _prepare_input(last),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryIntegrationAuthsConnection.model_validate(self._execute(query, variables).get("integrationAuths"))

    def integrations(self, project_id: str, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, last: Optional[int] = None) -> "QueryIntegrationsConnection":
        query = """query($after: String, $before: String, $first: Int, $last: Int, $projectId: String!) { integrations(after: $after, before: $before, first: $first, last: $last, projectId: $projectId) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "first": _prepare_input(first),
            "last": _prepare_input(last),
            "projectId": _prepare_input(project_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryIntegrationsConnection.model_validate(self._execute(query, variables).get("integrations"))

    def invite_code(self, code: str) -> "InviteCode":
        query = """query($code: String!) { inviteCode(code: $code) { code createdAt id projectId project { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "code": _prepare_input(code),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return InviteCode.model_validate(self._execute(query, variables).get("inviteCode"))

    def me(self) -> "User":
        query = """query { me { agreedFairUse avatar banReason createdAt email githubProviderId githubUsername has2FA hasPasskeys id isAdmin isConductor isVerified lastLogin name riskLevel termsAgreedOn username apiTokenRateLimit { remainingPoints resetsAt } profile { bio isPublic website } workspace { adoptionLevel allowDeprecatedRegions avatar banReason createdAt discordRole has2FAEnforcement hasGuardrailsAccess hasSAML id name preferredRegion redactedDueTo2FAPending slackChannelId subscriptionPlanLimit updatedAt usersWithout2FA } workspaces { adoptionLevel allowDeprecatedRegions avatar banReason createdAt discordRole has2FAEnforcement hasGuardrailsAccess hasSAML id name preferredRegion redactedDueTo2FAPending slackChannelId subscriptionPlanLimit updatedAt usersWithout2FA } } }"""
        return User.model_validate(self._execute(query).get("me"))

    def metrics(self, measurements: list["MetricMeasurement"], start_date: str, *, averaging_window_seconds: Optional[int] = None, end_date: Optional[str] = None, environment_id: Optional[str] = None, group_by: Optional[list["MetricTag"]] = None, include_deleted: Optional[bool] = None, project_id: Optional[str] = None, sample_rate_seconds: Optional[int] = None, service_id: Optional[str] = None, volume_id: Optional[str] = None, volume_instance_external_id: Optional[str] = None, workspace_id: Optional[str] = None) -> list["MetricsResult"]:
        query = """query($averagingWindowSeconds: Int, $endDate: DateTime, $environmentId: String, $groupBy: [MetricTag!], $includeDeleted: Boolean, $measurements: [MetricMeasurement!]!, $projectId: String, $sampleRateSeconds: Int, $serviceId: String, $startDate: DateTime!, $volumeId: String, $volumeInstanceExternalId: String, $workspaceId: String) { metrics(averagingWindowSeconds: $averagingWindowSeconds, endDate: $endDate, environmentId: $environmentId, groupBy: $groupBy, includeDeleted: $includeDeleted, measurements: $measurements, projectId: $projectId, sampleRateSeconds: $sampleRateSeconds, serviceId: $serviceId, startDate: $startDate, volumeId: $volumeId, volumeInstanceExternalId: $volumeInstanceExternalId, workspaceId: $workspaceId) { tags { deploymentId deploymentInstanceId environmentId pluginId projectId region serviceId volumeId volumeInstanceId } values { ts value } } }"""
        variables: dict[str, Any] = {
            "averagingWindowSeconds": _prepare_input(averaging_window_seconds),
            "endDate": _prepare_input(end_date),
            "environmentId": _prepare_input(environment_id),
            "groupBy": _prepare_input(group_by),
            "includeDeleted": _prepare_input(include_deleted),
            "measurements": _prepare_input(measurements),
            "projectId": _prepare_input(project_id),
            "sampleRateSeconds": _prepare_input(sample_rate_seconds),
            "serviceId": _prepare_input(service_id),
            "startDate": _prepare_input(start_date),
            "volumeId": _prepare_input(volume_id),
            "volumeInstanceExternalId": _prepare_input(volume_instance_external_id),
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("metrics")
        return TypeAdapter(list["MetricsResult"]).validate_python(_data) if _data else []

    def notification_deliveries(self, *, after: Optional[str] = None, before: Optional[str] = None, environment_id: Optional[str] = None, only_unread: Optional[bool] = None, project_id: Optional[str] = None, status: Optional["NotificationStatus"] = None, type: Optional["NotificationDeliveryType"] = None, workspace_id: Optional[str] = None, first: Optional[int] = None, last: Optional[int] = None) -> "QueryNotificationDeliveriesConnection":
        query = """query($after: String, $before: String, $filter: NotificationDeliveryFilterInput, $first: Int, $last: Int) { notificationDeliveries(after: $after, before: $before, filter: $filter, first: $first, last: $last) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "filter": _prepare_input(NotificationDeliveryFilterInput(environment_id=environment_id, only_unread=only_unread, project_id=project_id, status=status, type=type, workspace_id=workspace_id)),
            "first": _prepare_input(first),
            "last": _prepare_input(last),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryNotificationDeliveriesConnection.model_validate(self._execute(query, variables).get("notificationDeliveries"))

    def notification_rules(self, workspace_id: str, *, project_id: Optional[str] = None) -> list["NotificationRule"]:
        query = """query($projectId: String, $workspaceId: String!) { notificationRules(projectId: $projectId, workspaceId: $workspaceId) { createdAt environmentId ephemeralEnvironments eventTypes id projectId serviceId updatedAt workspaceId channels { config createdAt id updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "projectId": _prepare_input(project_id),
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("notificationRules")
        return TypeAdapter(list["NotificationRule"]).validate_python(_data) if _data else []

    def observability_dashboards(self, environment_id: str, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, last: Optional[int] = None) -> "QueryObservabilityDashboardsConnection":
        query = """query($after: String, $before: String, $environmentId: String!, $first: Int, $last: Int) { observabilityDashboards(after: $after, before: $before, environmentId: $environmentId, first: $first, last: $last) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "environmentId": _prepare_input(environment_id),
            "first": _prepare_input(first),
            "last": _prepare_input(last),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryObservabilityDashboardsConnection.model_validate(self._execute(query, variables).get("observabilityDashboards"))

    def passkeys(self, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, last: Optional[int] = None) -> "QueryPasskeysConnection":
        query = """query($after: String, $before: String, $first: Int, $last: Int) { passkeys(after: $after, before: $before, first: $first, last: $last) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "first": _prepare_input(first),
            "last": _prepare_input(last),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryPasskeysConnection.model_validate(self._execute(query, variables).get("passkeys"))

    def platform_status(self) -> "PlatformStatus":
        query = """query { platformStatus { isStable incident { id message url } maintenance { id message start url } } }"""
        return PlatformStatus.model_validate(self._execute(query).get("platformStatus"))

    def plugin(self, id: str) -> "Plugin":
        query = """query($id: String!) { plugin(id: $id) { createdAt deletedAt deprecatedAt friendlyName id logsEnabled migrationDatabaseServiceId project { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Plugin.model_validate(self._execute(query, variables).get("plugin"))

    def plugin_logs(self, environment_id: str, plugin_id: str, *, end_date: Optional[str] = None, filter: Optional[str] = None, limit: Optional[int] = None, start_date: Optional[str] = None) -> list["Log"]:
        query = """query($endDate: DateTime, $environmentId: String!, $filter: String, $limit: Int, $pluginId: String!, $startDate: DateTime) { pluginLogs(endDate: $endDate, environmentId: $environmentId, filter: $filter, limit: $limit, pluginId: $pluginId, startDate: $startDate) { message severity timestamp attributes { key value } tags { deploymentId deploymentInstanceId environmentId pluginId projectId serviceId snapshotId } } }"""
        variables: dict[str, Any] = {
            "endDate": _prepare_input(end_date),
            "environmentId": _prepare_input(environment_id),
            "filter": _prepare_input(filter),
            "limit": _prepare_input(limit),
            "pluginId": _prepare_input(plugin_id),
            "startDate": _prepare_input(start_date),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("pluginLogs")
        return TypeAdapter(list["Log"]).validate_python(_data) if _data else []

    def preferences(self, *, token: Optional[str] = None) -> "Preferences":
        query = """query($token: String) { preferences(token: $token) { buildFailedEmail changelogEmail communityEmail deployCrashedEmail ephemeralEnvironmentEmail id marketingEmail subprocessorUpdatesEmail templateQueueEmail usageEmail } }"""
        variables: dict[str, Any] = {
            "token": _prepare_input(token),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Preferences.model_validate(self._execute(query, variables).get("preferences"))

    def private_network_endpoint(self, environment_id: str, private_network_id: str, service_id: str) -> Optional["PrivateNetworkEndpoint"]:
        query = """query($environmentId: String!, $privateNetworkId: String!, $serviceId: String!) { privateNetworkEndpoint(environmentId: $environmentId, privateNetworkId: $privateNetworkId, serviceId: $serviceId) { createdAt deletedAt dnsName newDnsName privateIps publicId serviceInstanceId tags } }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "privateNetworkId": _prepare_input(private_network_id),
            "serviceId": _prepare_input(service_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("privateNetworkEndpoint")
        return PrivateNetworkEndpoint.model_validate(_data) if _data else None

    def private_network_endpoint_name_available(self, environment_id: str, prefix: str, private_network_id: str) -> bool:
        query = """query($environmentId: String!, $prefix: String!, $privateNetworkId: String!) { privateNetworkEndpointNameAvailable(environmentId: $environmentId, prefix: $prefix, privateNetworkId: $privateNetworkId) }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "prefix": _prepare_input(prefix),
            "privateNetworkId": _prepare_input(private_network_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("privateNetworkEndpointNameAvailable")

    def private_networks(self, environment_id: str) -> list["PrivateNetwork"]:
        query = """query($environmentId: String!) { privateNetworks(environmentId: $environmentId) { createdAt deletedAt dnsName environmentId name networkId projectId publicId tags } }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("privateNetworks")
        return TypeAdapter(list["PrivateNetwork"]).validate_python(_data) if _data else []

    def project(self, id: str) -> "Project":
        query = """query($id: String!) { project(id: $id) { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId baseEnvironment { canAccess createdAt deletedAt id isEphemeral name projectId unmergedChangesCount updatedAt } members { avatar email id name } team { adoptionLevel avatar createdAt id name preferredRegion slackChannelId updatedAt } workspace { adoptionLevel allowDeprecatedRegions avatar banReason createdAt discordRole has2FAEnforcement hasGuardrailsAccess hasSAML id name preferredRegion redactedDueTo2FAPending slackChannelId subscriptionPlanLimit updatedAt usersWithout2FA } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Project.model_validate(self._execute(query, variables).get("project"))

    def project_compliance(self, project_id: str) -> "ProjectComplianceInfo":
        query = """query($projectId: String!) { projectCompliance(projectId: $projectId) { projectId projectName workspaceId memberPermissions { email name } serviceBackups { serviceId serviceName } twoFactorMembers { email name twoFactorAuthEnabled } } }"""
        variables: dict[str, Any] = {
            "projectId": _prepare_input(project_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return ProjectComplianceInfo.model_validate(self._execute(query, variables).get("projectCompliance"))

    def project_invitation(self, code: str) -> "PublicProjectInvitation":
        query = """query($code: String!) { projectInvitation(code: $code) }"""
        variables: dict[str, Any] = {
            "code": _prepare_input(code),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return PublicProjectInvitation.model_validate(self._execute(query, variables).get("projectInvitation"))

    def project_invitations(self, id: str) -> list["ProjectInvitation"]:
        query = """query($id: String!) { projectInvitations(id: $id) { email expiresAt id isExpired inviter { email name } project { id name } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("projectInvitations")
        return TypeAdapter(list["ProjectInvitation"]).validate_python(_data) if _data else []

    def project_invite_code(self, project_id: str, role: "ProjectRole") -> "InviteCode":
        query = """query($projectId: String!, $role: ProjectRole!) { projectInviteCode(projectId: $projectId, role: $role) { code createdAt id projectId project { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "projectId": _prepare_input(project_id),
            "role": _prepare_input(role),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return InviteCode.model_validate(self._execute(query, variables).get("projectInviteCode"))

    def project_members(self, project_id: str) -> list["ProjectMember"]:
        query = """query($projectId: String!) { projectMembers(projectId: $projectId) { avatar email id name } }"""
        variables: dict[str, Any] = {
            "projectId": _prepare_input(project_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("projectMembers")
        return TypeAdapter(list["ProjectMember"]).validate_python(_data) if _data else []

    def project_resource_access(self, project_id: str) -> "ProjectResourceAccess":
        query = """query($projectId: String!) { projectResourceAccess(projectId: $projectId) { customDomain { disallowed } databaseDeployment { disallowed } deployment { disallowed } environment { disallowed } plugin { disallowed } } }"""
        variables: dict[str, Any] = {
            "projectId": _prepare_input(project_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return ProjectResourceAccess.model_validate(self._execute(query, variables).get("projectResourceAccess"))

    def project_token(self) -> "ProjectToken":
        query = """query { projectToken { createdAt displayToken environmentId id name projectId environment { canAccess createdAt deletedAt id isEphemeral name projectId unmergedChangesCount updatedAt } project { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId } } }"""
        return ProjectToken.model_validate(self._execute(query).get("projectToken"))

    def project_tokens(self, project_id: str, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, last: Optional[int] = None) -> "QueryProjectTokensConnection":
        query = """query($after: String, $before: String, $first: Int, $last: Int, $projectId: String!) { projectTokens(after: $after, before: $before, first: $first, last: $last, projectId: $projectId) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "first": _prepare_input(first),
            "last": _prepare_input(last),
            "projectId": _prepare_input(project_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryProjectTokensConnection.model_validate(self._execute(query, variables).get("projectTokens"))

    def project_workspace_members(self, project_id: str) -> "ProjectWorkspaceMembersResponse":
        query = """query($projectId: String!) { projectWorkspaceMembers(projectId: $projectId) { projectId projectName workspaceId members { email name twoFactorAuthEnabled } } }"""
        variables: dict[str, Any] = {
            "projectId": _prepare_input(project_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return ProjectWorkspaceMembersResponse.model_validate(self._execute(query, variables).get("projectWorkspaceMembers"))

    def projects(self, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, include_deleted: Optional[bool] = None, last: Optional[int] = None, user_id: Optional[str] = None, workspace_id: Optional[str] = None) -> "QueryProjectsConnection":
        query = """query($after: String, $before: String, $first: Int, $includeDeleted: Boolean, $last: Int, $userId: String, $workspaceId: String) { projects(after: $after, before: $before, first: $first, includeDeleted: $includeDeleted, last: $last, userId: $userId, workspaceId: $workspaceId) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "first": _prepare_input(first),
            "includeDeleted": _prepare_input(include_deleted),
            "last": _prepare_input(last),
            "userId": _prepare_input(user_id),
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryProjectsConnection.model_validate(self._execute(query, variables).get("projects"))

    def public_stats(self) -> "PublicStats":
        query = """query { publicStats { totalDeploymentsLastMonth totalLogsLastMonth totalProjects totalRequestsLastMonth totalServices totalUsers } }"""
        return PublicStats.model_validate(self._execute(query).get("publicStats"))

    def referral_info(self, workspace_id: str) -> "ReferralInfo":
        query = """query($workspaceId: String!) { referralInfo(workspaceId: $workspaceId) { code id status referralStats { credited pending } } }"""
        variables: dict[str, Any] = {
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return ReferralInfo.model_validate(self._execute(query, variables).get("referralInfo"))

    def regions(self, *, project_id: Optional[str] = None) -> list["Region"]:
        query = """query($projectId: String) { regions(projectId: $projectId) { country location name railwayMetal region workspaceId deploymentConstraints { adminOnly runtimeExclusivity stagingOnly } } }"""
        variables: dict[str, Any] = {
            "projectId": _prepare_input(project_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("regions")
        return TypeAdapter(list["Region"]).validate_python(_data) if _data else []

    def resource_access(self, id: str, *, type: Optional["ResourceOwnerType"] = None) -> "ResourceAccess":
        query = """query($explicitResourceOwner: ExplicitOwnerInput!) { resourceAccess(explicitResourceOwner: $explicitResourceOwner) { deployment { disallowed } project { disallowed } } }"""
        variables: dict[str, Any] = {
            "explicitResourceOwner": _prepare_input(ExplicitOwnerInput(id=id, type=type)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return ResourceAccess.model_validate(self._execute(query, variables).get("resourceAccess"))

    def service(self, id: str) -> "Service":
        query = """query($id: String!) { service(id: $id) { createdAt deletedAt hasHiddenRegistryCredentialsFromTemplate icon id name projectId templateId templateServiceId templateThreadSlug updatedAt project { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Service.model_validate(self._execute(query, variables).get("service"))

    def service_domain_available(self, domain: str) -> "DomainAvailable":
        query = """query($domain: String!) { serviceDomainAvailable(domain: $domain) { available message } }"""
        variables: dict[str, Any] = {
            "domain": _prepare_input(domain),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return DomainAvailable.model_validate(self._execute(query, variables).get("serviceDomainAvailable"))

    def service_instance(self, environment_id: str, service_id: str) -> "ServiceInstance":
        query = """query($environmentId: String!, $serviceId: String!) { serviceInstance(environmentId: $environmentId, serviceId: $serviceId) { buildCommand createdAt cronSchedule deletedAt dockerfilePath drainingSeconds environmentId healthcheckPath healthcheckTimeout id ipv6EgressEnabled isUpdatable nextCronRunAt nixpacksPlan numReplicas overlapSeconds preDeployCommand railpackInfo railwayConfigFile region restartPolicyMaxRetries rootDirectory serviceId serviceName sleepApplication startCommand updatedAt upstreamUrl watchPatterns activeDeployments { canRedeploy canRollback createdAt deploymentStopped diagnosis environmentId id meta projectId serviceId snapshotId staticUrl statusUpdatedAt suggestAddServiceDomain updatedAt url } latestDeployment { canRedeploy canRollback createdAt deploymentStopped diagnosis environmentId id meta projectId serviceId snapshotId staticUrl statusUpdatedAt suggestAddServiceDomain updatedAt url } service { createdAt deletedAt hasHiddenRegistryCredentialsFromTemplate icon id name projectId templateId templateServiceId templateThreadSlug updatedAt } source { image repo } } }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "serviceId": _prepare_input(service_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return ServiceInstance.model_validate(self._execute(query, variables).get("serviceInstance"))

    def service_instance_is_updatable(self, environment_id: str, service_id: str) -> bool:
        query = """query($environmentId: String!, $serviceId: String!) { serviceInstanceIsUpdatable(environmentId: $environmentId, serviceId: $serviceId) }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "serviceId": _prepare_input(service_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("serviceInstanceIsUpdatable")

    def service_instance_limit_override(self, environment_id: str, service_id: str) -> Optional[Any]:
        query = """query($environmentId: String!, $serviceId: String!) { serviceInstanceLimitOverride(environmentId: $environmentId, serviceId: $serviceId) }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "serviceId": _prepare_input(service_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("serviceInstanceLimitOverride")

    def service_instance_limits(self, environment_id: str, service_id: str) -> Any:
        query = """query($environmentId: String!, $serviceId: String!) { serviceInstanceLimits(environmentId: $environmentId, serviceId: $serviceId) }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "serviceId": _prepare_input(service_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("serviceInstanceLimits")

    def sessions(self, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, last: Optional[int] = None) -> "QuerySessionsConnection":
        query = """query($after: String, $before: String, $first: Int, $last: Int) { sessions(after: $after, before: $before, first: $first, last: $last) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "first": _prepare_input(first),
            "last": _prepare_input(last),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QuerySessionsConnection.model_validate(self._execute(query, variables).get("sessions"))

    def ssh_public_keys(self, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, last: Optional[int] = None) -> "QuerySshPublicKeysConnection":
        query = """query($after: String, $before: String, $first: Int, $last: Int) { sshPublicKeys(after: $after, before: $before, first: $first, last: $last) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "first": _prepare_input(first),
            "last": _prepare_input(last),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QuerySshPublicKeysConnection.model_validate(self._execute(query, variables).get("sshPublicKeys"))

    def tcp_proxies(self, environment_id: str, service_id: str) -> list["TCPProxy"]:
        query = """query($environmentId: String!, $serviceId: String!) { tcpProxies(environmentId: $environmentId, serviceId: $serviceId) { applicationPort createdAt deletedAt domain environmentId id proxyPort serviceId updatedAt } }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "serviceId": _prepare_input(service_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("tcpProxies")
        return TypeAdapter(list["TCPProxy"]).validate_python(_data) if _data else []

    def team(self, id: str) -> "Team":
        query = """query($id: String!) { team(id: $id) { adoptionLevel avatar createdAt id name preferredRegion slackChannelId updatedAt adoptionHistory { adoptionLevel createdAt deltaLevel id matchedIcpEmail monthlyEstimatedUsage numConfigFile numCronSchedule numDeploys numEnvs numFailedDeploys numHealthcheck numIconConfig numRegion numReplicas numRootDirectory numSeats numServices numVariables numWatchPatterns totalCores totalDisk totalNetwork updatedAt } apiTokenRateLimit { remainingPoints resetsAt } customer { appliedCredits billingEmail creditBalance currentUsage defaultPaymentMethodId hasExhaustedFreePlan id isPrepaying isTrialing isUsageSubscriber isWithdrawingToCredits remainingUsageCreditBalance stripeCustomerId trialDaysRemaining } members { avatar email id name } teamPermissions { createdAt id updatedAt userId workspaceId } workspace { adoptionLevel allowDeprecatedRegions avatar banReason createdAt discordRole has2FAEnforcement hasGuardrailsAccess hasSAML id name preferredRegion redactedDueTo2FAPending slackChannelId subscriptionPlanLimit updatedAt usersWithout2FA } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Team.model_validate(self._execute(query, variables).get("team"))

    def team_templates(self, team_id: str, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, last: Optional[int] = None) -> "QueryTeamTemplatesConnection":
        query = """query($after: String, $before: String, $first: Int, $last: Int, $teamId: String!) { teamTemplates(after: $after, before: $before, first: $first, last: $last, teamId: $teamId) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "first": _prepare_input(first),
            "last": _prepare_input(last),
            "teamId": _prepare_input(team_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryTeamTemplatesConnection.model_validate(self._execute(query, variables).get("teamTemplates"))

    def template(self, *, code: Optional[str] = None, id: Optional[str] = None, owner: Optional[str] = None, repo: Optional[str] = None) -> "Template":
        query = """query($code: String, $id: String, $owner: String, $repo: String) { template(code: $code, id: $id, owner: $owner, repo: $repo) { activeProjects canvasConfig category code communityThreadSlug config createdAt demoProjectId description health id image isApproved isV2Template isVerified languages metadata name projects readme recentProjects serializedConfig supportHealthMetrics tags teamId totalPayout workspaceId creator { avatar hasPublicProfile name username } guides { post video } similarTemplates { code createdAt deploys description health image name teamId userId workspaceId } } }"""
        variables: dict[str, Any] = {
            "code": _prepare_input(code),
            "id": _prepare_input(id),
            "owner": _prepare_input(owner),
            "repo": _prepare_input(repo),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Template.model_validate(self._execute(query, variables).get("template"))

    def template_metrics(self, id: str) -> "TemplateMetrics":
        query = """query($id: String!) { templateMetrics(id: $id) { activeDeployments deploymentsLast90Days earningsLast30Days earningsLast90Days eligibleForSupportBonus supportHealth templateHealth totalDeployments totalEarnings } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return TemplateMetrics.model_validate(self._execute(query, variables).get("templateMetrics"))

    def template_source_for_project(self, project_id: str) -> Optional["Template"]:
        query = """query($projectId: String!) { templateSourceForProject(projectId: $projectId) { activeProjects canvasConfig category code communityThreadSlug config createdAt demoProjectId description health id image isApproved isV2Template isVerified languages metadata name projects readme recentProjects serializedConfig supportHealthMetrics tags teamId totalPayout workspaceId creator { avatar hasPublicProfile name username } guides { post video } similarTemplates { code createdAt deploys description health image name teamId userId workspaceId } } }"""
        variables: dict[str, Any] = {
            "projectId": _prepare_input(project_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("templateSourceForProject")
        return Template.model_validate(_data) if _data else None

    def templates(self, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, last: Optional[int] = None, recommended: Optional[bool] = None, verified: Optional[bool] = None) -> "QueryTemplatesConnection":
        query = """query($after: String, $before: String, $first: Int, $last: Int, $recommended: Boolean, $verified: Boolean) { templates(after: $after, before: $before, first: $first, last: $last, recommended: $recommended, verified: $verified) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "first": _prepare_input(first),
            "last": _prepare_input(last),
            "recommended": _prepare_input(recommended),
            "verified": _prepare_input(verified),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryTemplatesConnection.model_validate(self._execute(query, variables).get("templates"))

    def templates_count(self) -> int:
        query = """query { templatesCount }"""
        return self._execute(query).get("templatesCount")

    def trusted_domains(self, workspace_id: str, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, last: Optional[int] = None) -> "QueryTrustedDomainsConnection":
        query = """query($after: String, $before: String, $first: Int, $last: Int, $workspaceId: String!) { trustedDomains(after: $after, before: $before, first: $first, last: $last, workspaceId: $workspaceId) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "first": _prepare_input(first),
            "last": _prepare_input(last),
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryTrustedDomainsConnection.model_validate(self._execute(query, variables).get("trustedDomains"))

    def two_factor_info(self) -> "TwoFactorInfo":
        query = """query { twoFactorInfo { hasRecoveryCodes isVerified } }"""
        return TwoFactorInfo.model_validate(self._execute(query).get("twoFactorInfo"))

    def usage(self, measurements: list["MetricMeasurement"], *, end_date: Optional[str] = None, group_by: Optional[list["MetricTag"]] = None, include_deleted: Optional[bool] = None, project_id: Optional[str] = None, start_date: Optional[str] = None, workspace_id: Optional[str] = None) -> list["AggregatedUsage"]:
        query = """query($endDate: DateTime, $groupBy: [MetricTag!], $includeDeleted: Boolean, $measurements: [MetricMeasurement!]!, $projectId: String, $startDate: DateTime, $workspaceId: String) { usage(endDate: $endDate, groupBy: $groupBy, includeDeleted: $includeDeleted, measurements: $measurements, projectId: $projectId, startDate: $startDate, workspaceId: $workspaceId) { value tags { deploymentId deploymentInstanceId environmentId pluginId projectId region serviceId volumeId volumeInstanceId } } }"""
        variables: dict[str, Any] = {
            "endDate": _prepare_input(end_date),
            "groupBy": _prepare_input(group_by),
            "includeDeleted": _prepare_input(include_deleted),
            "measurements": _prepare_input(measurements),
            "projectId": _prepare_input(project_id),
            "startDate": _prepare_input(start_date),
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("usage")
        return TypeAdapter(list["AggregatedUsage"]).validate_python(_data) if _data else []

    def user_kickback_earnings(self, user_id: str) -> "UserKickbackEarnings":
        query = """query($userId: String!) { userKickbackEarnings(userId: $userId) { total_amount } }"""
        variables: dict[str, Any] = {
            "userId": _prepare_input(user_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return UserKickbackEarnings.model_validate(self._execute(query, variables).get("userKickbackEarnings"))

    def user_profile(self, username: str) -> "UserProfileResponse":
        query = """query($username: String!) { userProfile(username: $username) { avatar createdAt customerId id isTrialing name state totalDeploys username profile { bio isPublic website } publishedTemplates { code createdAt deploys description health image name teamId userId workspaceId } } }"""
        variables: dict[str, Any] = {
            "username": _prepare_input(username),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return UserProfileResponse.model_validate(self._execute(query, variables).get("userProfile"))

    def user_templates(self, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, last: Optional[int] = None) -> "QueryUserTemplatesConnection":
        query = """query($after: String, $before: String, $first: Int, $last: Int) { userTemplates(after: $after, before: $before, first: $first, last: $last) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "first": _prepare_input(first),
            "last": _prepare_input(last),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryUserTemplatesConnection.model_validate(self._execute(query, variables).get("userTemplates"))

    def variables(self, environment_id: str, project_id: str, *, service_id: Optional[str] = None, unrendered: Optional[bool] = None) -> Any:
        query = """query($environmentId: String!, $projectId: String!, $serviceId: String, $unrendered: Boolean) { variables(environmentId: $environmentId, projectId: $projectId, serviceId: $serviceId, unrendered: $unrendered) }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "projectId": _prepare_input(project_id),
            "serviceId": _prepare_input(service_id),
            "unrendered": _prepare_input(unrendered),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("variables")

    def variables_for_service_deployment(self, environment_id: str, project_id: str, service_id: str) -> Any:
        query = """query($environmentId: String!, $projectId: String!, $serviceId: String!) { variablesForServiceDeployment(environmentId: $environmentId, projectId: $projectId, serviceId: $serviceId) }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "projectId": _prepare_input(project_id),
            "serviceId": _prepare_input(service_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("variablesForServiceDeployment")

    def vercel_info(self) -> "VercelInfo":
        query = """query { vercelInfo { accounts { id integrationAuthId isUser name slug } } }"""
        return VercelInfo.model_validate(self._execute(query).get("vercelInfo"))

    def volume_instance(self, id: str) -> "VolumeInstance":
        query = """query($id: String!) { volumeInstance(id: $id) { createdAt currentSizeMB environmentId externalId id mountPath region serviceId sizeMB volumeId environment { canAccess createdAt deletedAt id isEphemeral name projectId unmergedChangesCount updatedAt } service { createdAt deletedAt hasHiddenRegistryCredentialsFromTemplate icon id name projectId templateId templateServiceId templateThreadSlug updatedAt } volume { createdAt id name projectId } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return VolumeInstance.model_validate(self._execute(query, variables).get("volumeInstance"))

    def volume_instance_backup_list(self, volume_instance_id: str) -> list["VolumeInstanceBackup"]:
        query = """query($volumeInstanceId: String!) { volumeInstanceBackupList(volumeInstanceId: $volumeInstanceId) { createdAt creatorId expiresAt externalId id name referencedMB scheduleId usedMB volumeInstanceSizeMB } }"""
        variables: dict[str, Any] = {
            "volumeInstanceId": _prepare_input(volume_instance_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("volumeInstanceBackupList")
        return TypeAdapter(list["VolumeInstanceBackup"]).validate_python(_data) if _data else []

    def volume_instance_backup_schedule_list(self, volume_instance_id: str) -> list["VolumeInstanceBackupSchedule"]:
        query = """query($volumeInstanceId: String!) { volumeInstanceBackupScheduleList(volumeInstanceId: $volumeInstanceId) { createdAt cron id name retentionSeconds } }"""
        variables: dict[str, Any] = {
            "volumeInstanceId": _prepare_input(volume_instance_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("volumeInstanceBackupScheduleList")
        return TypeAdapter(list["VolumeInstanceBackupSchedule"]).validate_python(_data) if _data else []

    def workflow_status(self, workflow_id: str) -> "WorkflowResult":
        query = """query($workflowId: String!) { workflowStatus(workflowId: $workflowId) { error } }"""
        variables: dict[str, Any] = {
            "workflowId": _prepare_input(workflow_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return WorkflowResult.model_validate(self._execute(query, variables).get("workflowStatus"))

    def workspace(self, workspace_id: str) -> "Workspace":
        query = """query($workspaceId: String!) { workspace(workspaceId: $workspaceId) { adoptionLevel allowDeprecatedRegions avatar banReason createdAt discordRole has2FAEnforcement hasGuardrailsAccess hasSAML id name preferredRegion redactedDueTo2FAPending slackChannelId subscriptionPlanLimit updatedAt usersWithout2FA adoptionHistory { adoptionLevel createdAt deltaLevel id matchedIcpEmail monthlyEstimatedUsage numConfigFile numCronSchedule numDeploys numEnvs numFailedDeploys numHealthcheck numIconConfig numRegion numReplicas numRootDirectory numSeats numServices numVariables numWatchPatterns totalCores totalDisk totalNetwork updatedAt } apiTokenRateLimit { remainingPoints resetsAt } customer { appliedCredits billingEmail creditBalance currentUsage defaultPaymentMethodId hasExhaustedFreePlan id isPrepaying isTrialing isUsageSubscriber isWithdrawingToCredits remainingUsageCreditBalance stripeCustomerId trialDaysRemaining } members { avatar email id name twoFactorAuthEnabled } partnerProfile { category description slug website } referredUsers { code id } team { adoptionLevel avatar createdAt id name preferredRegion slackChannelId updatedAt } } }"""
        variables: dict[str, Any] = {
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Workspace.model_validate(self._execute(query, variables).get("workspace"))

    def workspace_by_code(self, code: str) -> "Workspace":
        query = """query($code: String!) { workspaceByCode(code: $code) { adoptionLevel allowDeprecatedRegions avatar banReason createdAt discordRole has2FAEnforcement hasGuardrailsAccess hasSAML id name preferredRegion redactedDueTo2FAPending slackChannelId subscriptionPlanLimit updatedAt usersWithout2FA adoptionHistory { adoptionLevel createdAt deltaLevel id matchedIcpEmail monthlyEstimatedUsage numConfigFile numCronSchedule numDeploys numEnvs numFailedDeploys numHealthcheck numIconConfig numRegion numReplicas numRootDirectory numSeats numServices numVariables numWatchPatterns totalCores totalDisk totalNetwork updatedAt } apiTokenRateLimit { remainingPoints resetsAt } customer { appliedCredits billingEmail creditBalance currentUsage defaultPaymentMethodId hasExhaustedFreePlan id isPrepaying isTrialing isUsageSubscriber isWithdrawingToCredits remainingUsageCreditBalance stripeCustomerId trialDaysRemaining } members { avatar email id name twoFactorAuthEnabled } partnerProfile { category description slug website } referredUsers { code id } team { adoptionLevel avatar createdAt id name preferredRegion slackChannelId updatedAt } } }"""
        variables: dict[str, Any] = {
            "code": _prepare_input(code),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Workspace.model_validate(self._execute(query, variables).get("workspaceByCode"))

    def workspace_identity_providers(self, workspace_id: str, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, last: Optional[int] = None) -> "QueryWorkspaceIdentityProvidersConnection":
        query = """query($after: String, $before: String, $first: Int, $last: Int, $workspaceId: String!) { workspaceIdentityProviders(after: $after, before: $before, first: $first, last: $last, workspaceId: $workspaceId) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "first": _prepare_input(first),
            "last": _prepare_input(last),
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryWorkspaceIdentityProvidersConnection.model_validate(self._execute(query, variables).get("workspaceIdentityProviders"))

    def workspace_policy(self, workspace_id: str) -> Optional["WorkspacePolicy"]:
        query = """query($workspaceId: String!) { workspacePolicy(workspaceId: $workspaceId) { id restrictPublicTcpProxies restrictRailwayDomainGeneration } }"""
        variables: dict[str, Any] = {
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("workspacePolicy")
        return WorkspacePolicy.model_validate(_data) if _data else None

    def workspace_templates(self, workspace_id: str, *, after: Optional[str] = None, before: Optional[str] = None, first: Optional[int] = None, last: Optional[int] = None) -> "QueryWorkspaceTemplatesConnection":
        query = """query($after: String, $before: String, $first: Int, $last: Int, $workspaceId: String!) { workspaceTemplates(after: $after, before: $before, first: $first, last: $last, workspaceId: $workspaceId) { edges { cursor } pageInfo { endCursor hasNextPage hasPreviousPage startCursor } } }"""
        variables: dict[str, Any] = {
            "after": _prepare_input(after),
            "before": _prepare_input(before),
            "first": _prepare_input(first),
            "last": _prepare_input(last),
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return QueryWorkspaceTemplatesConnection.model_validate(self._execute(query, variables).get("workspaceTemplates"))

    # ── Mutations ──────────────────────────────────────────

    def api_token_create(self, name: str, *, workspace_id: Optional[str] = None) -> str:
        query = """mutation($input: ApiTokenCreateInput!) { apiTokenCreate(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(ApiTokenCreateInput(name=name, workspace_id=workspace_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("apiTokenCreate")

    def api_token_delete(self, id: str) -> bool:
        query = """mutation($id: String!) { apiTokenDelete(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("apiTokenDelete")

    def base_environment_override(self, id: str, *, base_environment_override_id: Optional[str] = None) -> bool:
        query = """mutation($id: String!, $input: BaseEnvironmentOverrideInput!) { baseEnvironmentOverride(id: $id, input: $input) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "input": _prepare_input(BaseEnvironmentOverrideInput(base_environment_override_id=base_environment_override_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("baseEnvironmentOverride")

    def bucket_create(self, project_id: str, *, environment_id: Optional[str] = None, name: Optional[str] = None) -> "Bucket":
        query = """mutation($input: BucketCreateInput!) { bucketCreate(input: $input) { createdAt id name projectId updatedAt project { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(BucketCreateInput(environment_id=environment_id, name=name, project_id=project_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Bucket.model_validate(self._execute(query, variables).get("bucketCreate"))

    def bucket_credentials_reset(self, bucket_id: str, environment_id: str, project_id: str) -> "BucketS3CompatibleCredentials":
        query = """mutation($bucketId: String!, $environmentId: String!, $projectId: String!) { bucketCredentialsReset(bucketId: $bucketId, environmentId: $environmentId, projectId: $projectId) { accessKeyId bucketName createdAt endpoint region secretAccessKey urlStyle } }"""
        variables: dict[str, Any] = {
            "bucketId": _prepare_input(bucket_id),
            "environmentId": _prepare_input(environment_id),
            "projectId": _prepare_input(project_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return BucketS3CompatibleCredentials.model_validate(self._execute(query, variables).get("bucketCredentialsReset"))

    def bucket_update(self, id: str, name: str) -> "Bucket":
        query = """mutation($id: String!, $input: BucketUpdateInput!) { bucketUpdate(id: $id, input: $input) { createdAt id name projectId updatedAt project { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "input": _prepare_input(BucketUpdateInput(name=name)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Bucket.model_validate(self._execute(query, variables).get("bucketUpdate"))

    def canvas_view_merge(self, source_environment_id: str, target_environment_id: str) -> bool:
        query = """mutation($sourceEnvironmentId: String!, $targetEnvironmentId: String!) { canvasViewMerge(sourceEnvironmentId: $sourceEnvironmentId, targetEnvironmentId: $targetEnvironmentId) }"""
        variables: dict[str, Any] = {
            "sourceEnvironmentId": _prepare_input(source_environment_id),
            "targetEnvironmentId": _prepare_input(target_environment_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("canvasViewMerge")

    def cli_event_track(self, arch: str, cli_version: str, command: str, duration_ms: int, is_ci: bool, os: str, success: bool, *, error_message: Optional[str] = None, sub_command: Optional[str] = None) -> bool:
        query = """mutation($input: CliEventTrackInput!) { cliEventTrack(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(CliEventTrackInput(arch=arch, cli_version=cli_version, command=command, duration_ms=duration_ms, error_message=error_message, is_ci=is_ci, os=os, sub_command=sub_command, success=success)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("cliEventTrack")

    def custom_domain_create(self, domain: str, environment_id: str, project_id: str, service_id: str, *, target_port: Optional[int] = None) -> "CustomDomain":
        query = """mutation($input: CustomDomainCreateInput!) { customDomainCreate(input: $input) { cdnMode createdAt deletedAt domain edgeId environmentId id projectId serviceId targetPort updatedAt cnameCheck { link message } status { certificateErrorMessage certificateRetryable verificationDnsHost verificationToken verified } } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(CustomDomainCreateInput(domain=domain, environment_id=environment_id, project_id=project_id, service_id=service_id, target_port=target_port)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return CustomDomain.model_validate(self._execute(query, variables).get("customDomainCreate"))

    def custom_domain_delete(self, id: str) -> bool:
        query = """mutation($id: String!) { customDomainDelete(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("customDomainDelete")

    def custom_domain_update(self, environment_id: str, id: str, *, target_port: Optional[int] = None) -> bool:
        query = """mutation($environmentId: String!, $id: String!, $targetPort: Int) { customDomainUpdate(environmentId: $environmentId, id: $id, targetPort: $targetPort) }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "id": _prepare_input(id),
            "targetPort": _prepare_input(target_port),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("customDomainUpdate")

    def customer_create_free_plan_subscription(self, id: str) -> bool:
        query = """mutation($id: String!) { customerCreateFreePlanSubscription(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("customerCreateFreePlanSubscription")

    def customer_toggle_payouts_to_credits(self, customer_id: str, is_withdrawing_to_credits: bool) -> bool:
        query = """mutation($customerId: String!, $input: customerTogglePayoutsToCreditsInput!) { customerTogglePayoutsToCredits(customerId: $customerId, input: $input) }"""
        variables: dict[str, Any] = {
            "customerId": _prepare_input(customer_id),
            "input": _prepare_input(customerTogglePayoutsToCreditsInput(is_withdrawing_to_credits=is_withdrawing_to_credits)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("customerTogglePayoutsToCredits")

    def deployment_approve(self, id: str) -> bool:
        query = """mutation($id: String!) { deploymentApprove(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("deploymentApprove")

    def deployment_cancel(self, id: str) -> bool:
        query = """mutation($id: String!) { deploymentCancel(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("deploymentCancel")

    def deployment_instance_execution_create(self, service_instance_id: str) -> bool:
        query = """mutation($input: DeploymentInstanceExecutionCreateInput!) { deploymentInstanceExecutionCreate(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(DeploymentInstanceExecutionCreateInput(service_instance_id=service_instance_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("deploymentInstanceExecutionCreate")

    def deployment_redeploy(self, id: str, *, use_previous_image_tag: Optional[bool] = None) -> "Deployment":
        query = """mutation($id: String!, $usePreviousImageTag: Boolean) { deploymentRedeploy(id: $id, usePreviousImageTag: $usePreviousImageTag) { canRedeploy canRollback createdAt deploymentStopped diagnosis environmentId id meta projectId serviceId snapshotId staticUrl statusUpdatedAt suggestAddServiceDomain updatedAt url creator { avatar email id name } environment { canAccess createdAt deletedAt id isEphemeral name projectId unmergedChangesCount updatedAt } instances { id } service { createdAt deletedAt hasHiddenRegistryCredentialsFromTemplate icon id name projectId templateId templateServiceId templateThreadSlug updatedAt } sockets { ipv6 port processName updatedAt } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "usePreviousImageTag": _prepare_input(use_previous_image_tag),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Deployment.model_validate(self._execute(query, variables).get("deploymentRedeploy"))

    def deployment_remove(self, id: str) -> bool:
        query = """mutation($id: String!) { deploymentRemove(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("deploymentRemove")

    def deployment_restart(self, id: str) -> bool:
        query = """mutation($id: String!) { deploymentRestart(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("deploymentRestart")

    def deployment_rollback(self, id: str) -> bool:
        query = """mutation($id: String!) { deploymentRollback(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("deploymentRollback")

    def deployment_stop(self, id: str) -> bool:
        query = """mutation($id: String!) { deploymentStop(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("deploymentStop")

    def deployment_trigger_create(self, branch: str, environment_id: str, project_id: str, provider: str, repository: str, service_id: str, *, check_suites: Optional[bool] = None, root_directory: Optional[str] = None) -> "DeploymentTrigger":
        query = """mutation($input: DeploymentTriggerCreateInput!) { deploymentTriggerCreate(input: $input) { baseEnvironmentOverrideId branch checkSuites environmentId id projectId provider repository serviceId validCheckSuites } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(DeploymentTriggerCreateInput(branch=branch, check_suites=check_suites, environment_id=environment_id, project_id=project_id, provider=provider, repository=repository, root_directory=root_directory, service_id=service_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return DeploymentTrigger.model_validate(self._execute(query, variables).get("deploymentTriggerCreate"))

    def deployment_trigger_delete(self, id: str) -> bool:
        query = """mutation($id: String!) { deploymentTriggerDelete(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("deploymentTriggerDelete")

    def deployment_trigger_update(self, id: str, *, branch: Optional[str] = None, check_suites: Optional[bool] = None, repository: Optional[str] = None, root_directory: Optional[str] = None) -> "DeploymentTrigger":
        query = """mutation($id: String!, $input: DeploymentTriggerUpdateInput!) { deploymentTriggerUpdate(id: $id, input: $input) { baseEnvironmentOverrideId branch checkSuites environmentId id projectId provider repository serviceId validCheckSuites } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "input": _prepare_input(DeploymentTriggerUpdateInput(branch=branch, check_suites=check_suites, repository=repository, root_directory=root_directory)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return DeploymentTrigger.model_validate(self._execute(query, variables).get("deploymentTriggerUpdate"))

    def docker_compose_import(self, environment_id: str, project_id: str, yaml: str, *, skip_staging_patch: Optional[bool] = None) -> "DockerComposeImport":
        query = """mutation($environmentId: String!, $projectId: String!, $skipStagingPatch: Boolean, $yaml: String!) { dockerComposeImport(environmentId: $environmentId, projectId: $projectId, skipStagingPatch: $skipStagingPatch, yaml: $yaml) { errors patch } }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "projectId": _prepare_input(project_id),
            "skipStagingPatch": _prepare_input(skip_staging_patch),
            "yaml": _prepare_input(yaml),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return DockerComposeImport.model_validate(self._execute(query, variables).get("dockerComposeImport"))

    def egress_gateway_association_create(self, environment_id: str, service_id: str, *, region: Optional[str] = None) -> list["EgressGateway"]:
        query = """mutation($input: EgressGatewayCreateInput!) { egressGatewayAssociationCreate(input: $input) { ipv4 region } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(EgressGatewayCreateInput(environment_id=environment_id, region=region, service_id=service_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("egressGatewayAssociationCreate")
        return TypeAdapter(list["EgressGateway"]).validate_python(_data) if _data else []

    def egress_gateway_associations_clear(self, environment_id: str, service_id: str) -> bool:
        query = """mutation($input: EgressGatewayServiceTargetInput!) { egressGatewayAssociationsClear(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(EgressGatewayServiceTargetInput(environment_id=environment_id, service_id=service_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("egressGatewayAssociationsClear")

    def email_change_confirm(self, nonce: str) -> bool:
        query = """mutation($nonce: String!) { emailChangeConfirm(nonce: $nonce) }"""
        variables: dict[str, Any] = {
            "nonce": _prepare_input(nonce),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("emailChangeConfirm")

    def email_change_initiate(self, new_email: str) -> bool:
        query = """mutation($newEmail: String!) { emailChangeInitiate(newEmail: $newEmail) }"""
        variables: dict[str, Any] = {
            "newEmail": _prepare_input(new_email),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("emailChangeInitiate")

    def environment_create(self, name: str, project_id: str, *, apply_changes_in_background: Optional[bool] = None, ephemeral: Optional[bool] = None, skip_initial_deploys: Optional[bool] = None, source_environment_id: Optional[str] = None, stage_initial_changes: Optional[bool] = None) -> "Environment":
        query = """mutation($input: EnvironmentCreateInput!) { environmentCreate(input: $input) { canAccess createdAt deletedAt id isEphemeral name projectId unmergedChangesCount updatedAt meta { baseBranch branch latestSuccessfulGitHubDeploymentId prCommentId prNumber prRepo prTitle skippedResourceIds } } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(EnvironmentCreateInput(apply_changes_in_background=apply_changes_in_background, ephemeral=ephemeral, name=name, project_id=project_id, skip_initial_deploys=skip_initial_deploys, source_environment_id=source_environment_id, stage_initial_changes=stage_initial_changes)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Environment.model_validate(self._execute(query, variables).get("environmentCreate"))

    def environment_delete(self, id: str) -> bool:
        query = """mutation($id: String!) { environmentDelete(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("environmentDelete")

    def environment_patch_commit(self, environment_id: str, *, commit_message: Optional[str] = None, patch: Optional[Any] = None) -> str:
        query = """mutation($commitMessage: String, $environmentId: String!, $patch: EnvironmentConfig) { environmentPatchCommit(commitMessage: $commitMessage, environmentId: $environmentId, patch: $patch) }"""
        variables: dict[str, Any] = {
            "commitMessage": _prepare_input(commit_message),
            "environmentId": _prepare_input(environment_id),
            "patch": _prepare_input(patch),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("environmentPatchCommit")

    def environment_patch_commit_staged(self, environment_id: str, *, commit_message: Optional[str] = None, skip_deploys: Optional[bool] = None) -> str:
        query = """mutation($commitMessage: String, $environmentId: String!, $skipDeploys: Boolean) { environmentPatchCommitStaged(commitMessage: $commitMessage, environmentId: $environmentId, skipDeploys: $skipDeploys) }"""
        variables: dict[str, Any] = {
            "commitMessage": _prepare_input(commit_message),
            "environmentId": _prepare_input(environment_id),
            "skipDeploys": _prepare_input(skip_deploys),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("environmentPatchCommitStaged")

    def environment_rename(self, id: str, name: str) -> "Environment":
        query = """mutation($id: String!, $input: EnvironmentRenameInput!) { environmentRename(id: $id, input: $input) { canAccess createdAt deletedAt id isEphemeral name projectId unmergedChangesCount updatedAt meta { baseBranch branch latestSuccessfulGitHubDeploymentId prCommentId prNumber prRepo prTitle skippedResourceIds } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "input": _prepare_input(EnvironmentRenameInput(name=name)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Environment.model_validate(self._execute(query, variables).get("environmentRename"))

    def environment_stage_changes(self, environment_id: str, input: Any, *, merge: Optional[bool] = None) -> "EnvironmentPatch":
        query = """mutation($environmentId: String!, $input: EnvironmentConfig!, $merge: Boolean) { environmentStageChanges(environmentId: $environmentId, input: $input, merge: $merge) { appliedAt createdAt environmentId id lastAppliedError message updatedAt appliedBy { avatar email id name username } environment { canAccess createdAt deletedAt id isEphemeral name projectId unmergedChangesCount updatedAt } } }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "input": _prepare_input(input),
            "merge": _prepare_input(merge),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return EnvironmentPatch.model_validate(self._execute(query, variables).get("environmentStageChanges"))

    def environment_triggers_deploy(self, environment_id: str, project_id: str, service_id: str) -> bool:
        query = """mutation($input: EnvironmentTriggersDeployInput!) { environmentTriggersDeploy(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(EnvironmentTriggersDeployInput(environment_id=environment_id, project_id=project_id, service_id=service_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("environmentTriggersDeploy")

    def environment_unskip_service(self, environment_id: str, service_id: str) -> bool:
        query = """mutation($environmentId: String!, $serviceId: String!) { environmentUnskipService(environmentId: $environmentId, serviceId: $serviceId) }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "serviceId": _prepare_input(service_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("environmentUnskipService")

    def fair_use_agree(self, agree: bool) -> bool:
        query = """mutation($agree: Boolean!) { fairUseAgree(agree: $agree) }"""
        variables: dict[str, Any] = {
            "agree": _prepare_input(agree),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("fairUseAgree")

    def feature_flag_add(self, flag: "ActiveFeatureFlag") -> bool:
        query = """mutation($input: FeatureFlagToggleInput!) { featureFlagAdd(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(FeatureFlagToggleInput(flag=flag)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("featureFlagAdd")

    def feature_flag_remove(self, flag: "ActiveFeatureFlag") -> bool:
        query = """mutation($input: FeatureFlagToggleInput!) { featureFlagRemove(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(FeatureFlagToggleInput(flag=flag)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("featureFlagRemove")

    def github_repo_deploy(self, project_id: str, repo: str, *, branch: Optional[str] = None, environment_id: Optional[str] = None) -> str:
        query = """mutation($input: GitHubRepoDeployInput!) { githubRepoDeploy(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(GitHubRepoDeployInput(branch=branch, environment_id=environment_id, project_id=project_id, repo=repo)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("githubRepoDeploy")

    def github_repo_update(self, environment_id: str, project_id: str, service_id: str) -> bool:
        query = """mutation($input: GitHubRepoUpdateInput!) { githubRepoUpdate(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(GitHubRepoUpdateInput(environment_id=environment_id, project_id=project_id, service_id=service_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("githubRepoUpdate")

    def heroku_import_variables(self, environment_id: str, heroku_app_id: str, project_id: str, service_id: str) -> int:
        query = """mutation($input: HerokuImportVariablesInput!) { herokuImportVariables(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(HerokuImportVariablesInput(environment_id=environment_id, heroku_app_id=heroku_app_id, project_id=project_id, service_id=service_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("herokuImportVariables")

    def integration_create(self, config: Any, name: str, project_id: str, *, integration_auth_id: Optional[str] = None) -> "Integration":
        query = """mutation($input: IntegrationCreateInput!) { integrationCreate(input: $input) { config id name projectId } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(IntegrationCreateInput(config=config, integration_auth_id=integration_auth_id, name=name, project_id=project_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Integration.model_validate(self._execute(query, variables).get("integrationCreate"))

    def integration_delete(self, id: str) -> bool:
        query = """mutation($id: String!) { integrationDelete(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("integrationDelete")

    def integration_update(self, id: str, config: Any, name: str, project_id: str, *, integration_auth_id: Optional[str] = None) -> "Integration":
        query = """mutation($id: String!, $input: IntegrationUpdateInput!) { integrationUpdate(id: $id, input: $input) { config id name projectId } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "input": _prepare_input(IntegrationUpdateInput(config=config, integration_auth_id=integration_auth_id, name=name, project_id=project_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Integration.model_validate(self._execute(query, variables).get("integrationUpdate"))

    def invite_code_use(self, code: str) -> "Project":
        query = """mutation($code: String!) { inviteCodeUse(code: $code) { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId baseEnvironment { canAccess createdAt deletedAt id isEphemeral name projectId unmergedChangesCount updatedAt } members { avatar email id name } team { adoptionLevel avatar createdAt id name preferredRegion slackChannelId updatedAt } workspace { adoptionLevel allowDeprecatedRegions avatar banReason createdAt discordRole has2FAEnforcement hasGuardrailsAccess hasSAML id name preferredRegion redactedDueTo2FAPending slackChannelId subscriptionPlanLimit updatedAt usersWithout2FA } } }"""
        variables: dict[str, Any] = {
            "code": _prepare_input(code),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Project.model_validate(self._execute(query, variables).get("inviteCodeUse"))

    def job_application_create(self, email: str, job_id: str, name: str, why: str, resume: Any) -> bool:
        query = """mutation($input: JobApplicationCreateInput!, $resume: Upload!) { jobApplicationCreate(input: $input, resume: $resume) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(JobApplicationCreateInput(email=email, job_id=job_id, name=name, why=why)),
            "resume": _prepare_input(resume),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("jobApplicationCreate")

    def login_session_auth(self, code: str, *, hostname: Optional[str] = None) -> bool:
        query = """mutation($input: LoginSessionAuthInput!) { loginSessionAuth(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(LoginSessionAuthInput(code=code, hostname=hostname)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("loginSessionAuth")

    def login_session_cancel(self, code: str) -> bool:
        query = """mutation($code: String!) { loginSessionCancel(code: $code) }"""
        variables: dict[str, Any] = {
            "code": _prepare_input(code),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("loginSessionCancel")

    def login_session_consume(self, code: str) -> Optional[str]:
        query = """mutation($code: String!) { loginSessionConsume(code: $code) }"""
        variables: dict[str, Any] = {
            "code": _prepare_input(code),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("loginSessionConsume")

    def login_session_create(self) -> str:
        query = """mutation { loginSessionCreate }"""
        return self._execute(query).get("loginSessionCreate")

    def login_session_verify(self, code: str) -> bool:
        query = """mutation($code: String!) { loginSessionVerify(code: $code) }"""
        variables: dict[str, Any] = {
            "code": _prepare_input(code),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("loginSessionVerify")

    def notification_deliveries_mark_as_read(self, delivery_ids: list[str]) -> bool:
        query = """mutation($deliveryIds: [String!]!) { notificationDeliveriesMarkAsRead(deliveryIds: $deliveryIds) }"""
        variables: dict[str, Any] = {
            "deliveryIds": _prepare_input(delivery_ids),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("notificationDeliveriesMarkAsRead")

    def notification_rule_create(self, channel_configs: list[Any], event_types: list[str], workspace_id: str, *, ephemeral_environments: Optional[bool] = None, project_id: Optional[str] = None, severities: Optional[list["NotificationSeverity"]] = None) -> "NotificationRule":
        query = """mutation($input: CreateNotificationRuleInput!) { notificationRuleCreate(input: $input) { createdAt environmentId ephemeralEnvironments eventTypes id projectId serviceId updatedAt workspaceId channels { config createdAt id updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(CreateNotificationRuleInput(channel_configs=channel_configs, ephemeral_environments=ephemeral_environments, event_types=event_types, project_id=project_id, severities=severities, workspace_id=workspace_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return NotificationRule.model_validate(self._execute(query, variables).get("notificationRuleCreate"))

    def notification_rule_delete(self, id: str) -> bool:
        query = """mutation($id: String!) { notificationRuleDelete(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("notificationRuleDelete")

    def notification_rule_update(self, id: str, *, channel_configs: Optional[list[Any]] = None, ephemeral_environments: Optional[bool] = None, event_types: Optional[list[str]] = None, severities: Optional[list["NotificationSeverity"]] = None) -> "NotificationRule":
        query = """mutation($id: String!, $input: UpdateNotificationRuleInput!) { notificationRuleUpdate(id: $id, input: $input) { createdAt environmentId ephemeralEnvironments eventTypes id projectId serviceId updatedAt workspaceId channels { config createdAt id updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "input": _prepare_input(UpdateNotificationRuleInput(channel_configs=channel_configs, ephemeral_environments=ephemeral_environments, event_types=event_types, severities=severities)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return NotificationRule.model_validate(self._execute(query, variables).get("notificationRuleUpdate"))

    def observability_dashboard_create(self, environment_id: str, *, items: Optional[list["ObservabilityDashboardUpdateInput"]] = None) -> bool:
        query = """mutation($input: ObservabilityDashboardCreateInput!) { observabilityDashboardCreate(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(ObservabilityDashboardCreateInput(environment_id=environment_id, items=items)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("observabilityDashboardCreate")

    def observability_dashboard_reset(self, id: str) -> bool:
        query = """mutation($id: String!) { observabilityDashboardReset(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("observabilityDashboardReset")

    def observability_dashboard_update(self, _id: str, dashboard_item: "ObservabilityDashboardItemCreateInput", display_config: Any, id: str) -> bool:
        query = """mutation($id: String!, $input: [ObservabilityDashboardUpdateInput!]!) { observabilityDashboardUpdate(id: $id, input: $input) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(_id),
            "input": _prepare_input(ObservabilityDashboardUpdateInput(dashboard_item=dashboard_item, display_config=display_config, id=id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("observabilityDashboardUpdate")

    def passkey_delete(self, id: str) -> bool:
        query = """mutation($id: String!) { passkeyDelete(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("passkeyDelete")

    def plugin_create(self, name: str, project_id: str, *, environment_id: Optional[str] = None, friendly_name: Optional[str] = None) -> "Plugin":
        query = """mutation($input: PluginCreateInput!) { pluginCreate(input: $input) { createdAt deletedAt deprecatedAt friendlyName id logsEnabled migrationDatabaseServiceId project { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(PluginCreateInput(environment_id=environment_id, friendly_name=friendly_name, name=name, project_id=project_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Plugin.model_validate(self._execute(query, variables).get("pluginCreate"))

    def plugin_delete(self, id: str, *, environment_id: Optional[str] = None) -> bool:
        query = """mutation($environmentId: String, $id: String!) { pluginDelete(environmentId: $environmentId, id: $id) }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("pluginDelete")

    def plugin_reset(self, id: str, environment_id: str) -> bool:
        query = """mutation($id: String!, $input: ResetPluginInput!) { pluginReset(id: $id, input: $input) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "input": _prepare_input(ResetPluginInput(environment_id=environment_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("pluginReset")

    def plugin_reset_credentials(self, id: str, environment_id: str) -> str:
        query = """mutation($id: String!, $input: ResetPluginCredentialsInput!) { pluginResetCredentials(id: $id, input: $input) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "input": _prepare_input(ResetPluginCredentialsInput(environment_id=environment_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("pluginResetCredentials")

    def plugin_restart(self, id: str, *, environment_id: Optional[str] = None) -> "Plugin":
        query = """mutation($id: String!, $input: PluginRestartInput!) { pluginRestart(id: $id, input: $input) { createdAt deletedAt deprecatedAt friendlyName id logsEnabled migrationDatabaseServiceId project { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "input": _prepare_input(PluginRestartInput(environment_id=environment_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Plugin.model_validate(self._execute(query, variables).get("pluginRestart"))

    def plugin_start(self, id: str, *, environment_id: Optional[str] = None) -> bool:
        query = """mutation($id: String!, $input: PluginRestartInput!) { pluginStart(id: $id, input: $input) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "input": _prepare_input(PluginRestartInput(environment_id=environment_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("pluginStart")

    def plugin_update(self, id: str, friendly_name: str) -> "Plugin":
        query = """mutation($id: String!, $input: PluginUpdateInput!) { pluginUpdate(id: $id, input: $input) { createdAt deletedAt deprecatedAt friendlyName id logsEnabled migrationDatabaseServiceId project { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "input": _prepare_input(PluginUpdateInput(friendly_name=friendly_name)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Plugin.model_validate(self._execute(query, variables).get("pluginUpdate"))

    def preferences_update(self, *, build_failed_email: Optional[bool] = None, changelog_email: Optional[bool] = None, community_email: Optional[bool] = None, deploy_crashed_email: Optional[bool] = None, ephemeral_environment_email: Optional[bool] = None, marketing_email: Optional[bool] = None, subprocessor_updates_email: Optional[bool] = None, template_queue_email: Optional[bool] = None, token: Optional[str] = None, usage_email: Optional[bool] = None) -> "Preferences":
        query = """mutation($input: PreferencesUpdateData!) { preferencesUpdate(input: $input) { buildFailedEmail changelogEmail communityEmail deployCrashedEmail ephemeralEnvironmentEmail id marketingEmail subprocessorUpdatesEmail templateQueueEmail usageEmail } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(PreferencesUpdateData(build_failed_email=build_failed_email, changelog_email=changelog_email, community_email=community_email, deploy_crashed_email=deploy_crashed_email, ephemeral_environment_email=ephemeral_environment_email, marketing_email=marketing_email, subprocessor_updates_email=subprocessor_updates_email, template_queue_email=template_queue_email, token=token, usage_email=usage_email)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Preferences.model_validate(self._execute(query, variables).get("preferencesUpdate"))

    def private_network_create_or_get(self, environment_id: str, name: str, project_id: str, tags: list[str]) -> "PrivateNetwork":
        query = """mutation($input: PrivateNetworkCreateOrGetInput!) { privateNetworkCreateOrGet(input: $input) { createdAt deletedAt dnsName environmentId name networkId projectId publicId tags } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(PrivateNetworkCreateOrGetInput(environment_id=environment_id, name=name, project_id=project_id, tags=tags)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return PrivateNetwork.model_validate(self._execute(query, variables).get("privateNetworkCreateOrGet"))

    def private_network_endpoint_create_or_get(self, environment_id: str, private_network_id: str, service_id: str, service_name: str, tags: list[str]) -> "PrivateNetworkEndpoint":
        query = """mutation($input: PrivateNetworkEndpointCreateOrGetInput!) { privateNetworkEndpointCreateOrGet(input: $input) { createdAt deletedAt dnsName newDnsName privateIps publicId serviceInstanceId tags } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(PrivateNetworkEndpointCreateOrGetInput(environment_id=environment_id, private_network_id=private_network_id, service_id=service_id, service_name=service_name, tags=tags)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return PrivateNetworkEndpoint.model_validate(self._execute(query, variables).get("privateNetworkEndpointCreateOrGet"))

    def private_network_endpoint_delete(self, id: str) -> bool:
        query = """mutation($id: String!) { privateNetworkEndpointDelete(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("privateNetworkEndpointDelete")

    def private_network_endpoint_rename(self, dns_name: str, id: str, private_network_id: str) -> bool:
        query = """mutation($dnsName: String!, $id: String!, $privateNetworkId: String!) { privateNetworkEndpointRename(dnsName: $dnsName, id: $id, privateNetworkId: $privateNetworkId) }"""
        variables: dict[str, Any] = {
            "dnsName": _prepare_input(dns_name),
            "id": _prepare_input(id),
            "privateNetworkId": _prepare_input(private_network_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("privateNetworkEndpointRename")

    def private_networks_for_environment_delete(self, environment_id: str) -> bool:
        query = """mutation($environmentId: String!) { privateNetworksForEnvironmentDelete(environmentId: $environmentId) }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("privateNetworksForEnvironmentDelete")

    def project_claim(self, id: str, workspace_id: str) -> "Project":
        query = """mutation($id: String!, $workspaceId: String!) { projectClaim(id: $id, workspaceId: $workspaceId) { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId baseEnvironment { canAccess createdAt deletedAt id isEphemeral name projectId unmergedChangesCount updatedAt } members { avatar email id name } team { adoptionLevel avatar createdAt id name preferredRegion slackChannelId updatedAt } workspace { adoptionLevel allowDeprecatedRegions avatar banReason createdAt discordRole has2FAEnforcement hasGuardrailsAccess hasSAML id name preferredRegion redactedDueTo2FAPending slackChannelId subscriptionPlanLimit updatedAt usersWithout2FA } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Project.model_validate(self._execute(query, variables).get("projectClaim"))

    def project_create(self, *, default_environment_name: Optional[str] = None, description: Optional[str] = None, is_monorepo: Optional[bool] = None, is_public: Optional[bool] = None, name: Optional[str] = None, pr_deploys: Optional[bool] = None, repo: Optional["ProjectCreateRepo"] = None, runtime: Optional["PublicRuntime"] = None, workspace_id: Optional[str] = None) -> "Project":
        query = """mutation($input: ProjectCreateInput!) { projectCreate(input: $input) { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId baseEnvironment { canAccess createdAt deletedAt id isEphemeral name projectId unmergedChangesCount updatedAt } members { avatar email id name } team { adoptionLevel avatar createdAt id name preferredRegion slackChannelId updatedAt } workspace { adoptionLevel allowDeprecatedRegions avatar banReason createdAt discordRole has2FAEnforcement hasGuardrailsAccess hasSAML id name preferredRegion redactedDueTo2FAPending slackChannelId subscriptionPlanLimit updatedAt usersWithout2FA } } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(ProjectCreateInput(default_environment_name=default_environment_name, description=description, is_monorepo=is_monorepo, is_public=is_public, name=name, pr_deploys=pr_deploys, repo=repo, runtime=runtime, workspace_id=workspace_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Project.model_validate(self._execute(query, variables).get("projectCreate"))

    def project_delete(self, id: str) -> bool:
        query = """mutation($id: String!) { projectDelete(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("projectDelete")

    def project_feature_flag_add(self, flag: "ActiveProjectFeatureFlag", project_id: str) -> bool:
        query = """mutation($input: ProjectFeatureFlagToggleInput!) { projectFeatureFlagAdd(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(ProjectFeatureFlagToggleInput(flag=flag, project_id=project_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("projectFeatureFlagAdd")

    def project_feature_flag_remove(self, flag: "ActiveProjectFeatureFlag", project_id: str) -> bool:
        query = """mutation($input: ProjectFeatureFlagToggleInput!) { projectFeatureFlagRemove(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(ProjectFeatureFlagToggleInput(flag=flag, project_id=project_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("projectFeatureFlagRemove")

    def project_invitation_accept(self, code: str) -> "ProjectPermission":
        query = """mutation($code: String!) { projectInvitationAccept(code: $code) { id projectId userId } }"""
        variables: dict[str, Any] = {
            "code": _prepare_input(code),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return ProjectPermission.model_validate(self._execute(query, variables).get("projectInvitationAccept"))

    def project_invitation_create(self, id: str, email: str, role: "ProjectRole") -> "ProjectInvitation":
        query = """mutation($id: String!, $input: ProjectInvitee!) { projectInvitationCreate(id: $id, input: $input) { email expiresAt id isExpired inviter { email name } project { id name } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "input": _prepare_input(ProjectInvitee(email=email, role=role)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return ProjectInvitation.model_validate(self._execute(query, variables).get("projectInvitationCreate"))

    def project_invitation_delete(self, id: str) -> bool:
        query = """mutation($id: String!) { projectInvitationDelete(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("projectInvitationDelete")

    def project_invitation_resend(self, id: str) -> "ProjectInvitation":
        query = """mutation($id: String!) { projectInvitationResend(id: $id) { email expiresAt id isExpired inviter { email name } project { id name } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return ProjectInvitation.model_validate(self._execute(query, variables).get("projectInvitationResend"))

    def project_invite_user(self, id: str, email: str, link: str) -> bool:
        query = """mutation($id: String!, $input: ProjectInviteUserInput!) { projectInviteUser(id: $id, input: $input) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "input": _prepare_input(ProjectInviteUserInput(email=email, link=link)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("projectInviteUser")

    def project_leave(self, id: str) -> bool:
        query = """mutation($id: String!) { projectLeave(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("projectLeave")

    def project_member_add(self, project_id: str, role: "ProjectRole", user_id: str) -> "ProjectMember":
        query = """mutation($input: ProjectMemberAddInput!) { projectMemberAdd(input: $input) { avatar email id name } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(ProjectMemberAddInput(project_id=project_id, role=role, user_id=user_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return ProjectMember.model_validate(self._execute(query, variables).get("projectMemberAdd"))

    def project_member_remove(self, project_id: str, user_id: str) -> list["ProjectMember"]:
        query = """mutation($input: ProjectMemberRemoveInput!) { projectMemberRemove(input: $input) { avatar email id name } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(ProjectMemberRemoveInput(project_id=project_id, user_id=user_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("projectMemberRemove")
        return TypeAdapter(list["ProjectMember"]).validate_python(_data) if _data else []

    def project_member_update(self, project_id: str, role: "ProjectRole", user_id: str) -> "ProjectMember":
        query = """mutation($input: ProjectMemberUpdateInput!) { projectMemberUpdate(input: $input) { avatar email id name } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(ProjectMemberUpdateInput(project_id=project_id, role=role, user_id=user_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return ProjectMember.model_validate(self._execute(query, variables).get("projectMemberUpdate"))

    def project_schedule_delete(self, id: str) -> bool:
        query = """mutation($id: String!) { projectScheduleDelete(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("projectScheduleDelete")

    def project_schedule_delete_cancel(self, id: str) -> bool:
        query = """mutation($id: String!) { projectScheduleDeleteCancel(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("projectScheduleDeleteCancel")

    def project_schedule_delete_force(self, id: str) -> bool:
        query = """mutation($id: String!) { projectScheduleDeleteForce(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("projectScheduleDeleteForce")

    def project_token_create(self, environment_id: str, name: str, project_id: str) -> str:
        query = """mutation($input: ProjectTokenCreateInput!) { projectTokenCreate(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(ProjectTokenCreateInput(environment_id=environment_id, name=name, project_id=project_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("projectTokenCreate")

    def project_token_delete(self, id: str) -> bool:
        query = """mutation($id: String!) { projectTokenDelete(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("projectTokenDelete")

    def project_transfer(self, workspace_id: str, project_id: str) -> bool:
        query = """mutation($input: ProjectTransferInput!, $projectId: String!) { projectTransfer(input: $input, projectId: $projectId) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(ProjectTransferInput(workspace_id=workspace_id)),
            "projectId": _prepare_input(project_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("projectTransfer")

    def project_transfer_confirm(self, ownership_transfer_id: str, project_id: str, *, destination_workspace_id: Optional[str] = None) -> bool:
        query = """mutation($input: ProjectTransferConfirmInput!) { projectTransferConfirm(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(ProjectTransferConfirmInput(destination_workspace_id=destination_workspace_id, ownership_transfer_id=ownership_transfer_id, project_id=project_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("projectTransferConfirm")

    def project_transfer_initiate(self, member_id: str, project_id: str) -> bool:
        query = """mutation($input: ProjectTransferInitiateInput!) { projectTransferInitiate(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(ProjectTransferInitiateInput(member_id=member_id, project_id=project_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("projectTransferInitiate")

    def project_transfer_to_team(self, id: str, team_id: str) -> bool:
        query = """mutation($id: String!, $input: ProjectTransferToTeamInput!) { projectTransferToTeam(id: $id, input: $input) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "input": _prepare_input(ProjectTransferToTeamInput(team_id=team_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("projectTransferToTeam")

    def project_update(self, id: str, *, base_environment_id: Optional[str] = None, bot_pr_environments: Optional[bool] = None, description: Optional[str] = None, focused_pr_environments: Optional[bool] = None, is_public: Optional[bool] = None, name: Optional[str] = None, pr_deploys: Optional[bool] = None) -> "Project":
        query = """mutation($id: String!, $input: ProjectUpdateInput!) { projectUpdate(id: $id, input: $input) { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId baseEnvironment { canAccess createdAt deletedAt id isEphemeral name projectId unmergedChangesCount updatedAt } members { avatar email id name } team { adoptionLevel avatar createdAt id name preferredRegion slackChannelId updatedAt } workspace { adoptionLevel allowDeprecatedRegions avatar banReason createdAt discordRole has2FAEnforcement hasGuardrailsAccess hasSAML id name preferredRegion redactedDueTo2FAPending slackChannelId subscriptionPlanLimit updatedAt usersWithout2FA } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "input": _prepare_input(ProjectUpdateInput(base_environment_id=base_environment_id, bot_pr_environments=bot_pr_environments, description=description, focused_pr_environments=focused_pr_environments, is_public=is_public, name=name, pr_deploys=pr_deploys)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Project.model_validate(self._execute(query, variables).get("projectUpdate"))

    def provider_auth_remove(self, id: str) -> bool:
        query = """mutation($id: String!) { providerAuthRemove(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("providerAuthRemove")

    def recovery_code_generate(self) -> "RecoveryCodes":
        query = """mutation { recoveryCodeGenerate { recoveryCodes } }"""
        return RecoveryCodes.model_validate(self._execute(query).get("recoveryCodeGenerate"))

    def recovery_code_validate(self, code: str, *, two_factor_linking_key: Optional[str] = None) -> bool:
        query = """mutation($input: RecoveryCodeValidateInput!) { recoveryCodeValidate(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(RecoveryCodeValidateInput(code=code, two_factor_linking_key=two_factor_linking_key)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("recoveryCodeValidate")

    def referral_info_update(self, code: str, workspace_id: str) -> "ReferralInfo":
        query = """mutation($input: ReferralInfoUpdateInput!) { referralInfoUpdate(input: $input) { code id status referralStats { credited pending } } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(ReferralInfoUpdateInput(code=code, workspace_id=workspace_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return ReferralInfo.model_validate(self._execute(query, variables).get("referralInfoUpdate"))

    def service_connect(self, id: str, *, branch: Optional[str] = None, image: Optional[str] = None, repo: Optional[str] = None) -> "Service":
        query = """mutation($id: String!, $input: ServiceConnectInput!) { serviceConnect(id: $id, input: $input) { createdAt deletedAt hasHiddenRegistryCredentialsFromTemplate icon id name projectId templateId templateServiceId templateThreadSlug updatedAt project { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "input": _prepare_input(ServiceConnectInput(branch=branch, image=image, repo=repo)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Service.model_validate(self._execute(query, variables).get("serviceConnect"))

    def service_create(self, project_id: str, *, branch: Optional[str] = None, environment_id: Optional[str] = None, icon: Optional[str] = None, name: Optional[str] = None, registry_credentials: Optional["RegistryCredentialsInput"] = None, source: Optional["ServiceSourceInput"] = None, template_id: Optional[str] = None, template_service_id: Optional[str] = None, variables: Optional[Any] = None) -> "Service":
        query = """mutation($input: ServiceCreateInput!) { serviceCreate(input: $input) { createdAt deletedAt hasHiddenRegistryCredentialsFromTemplate icon id name projectId templateId templateServiceId templateThreadSlug updatedAt project { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(ServiceCreateInput(branch=branch, environment_id=environment_id, icon=icon, name=name, project_id=project_id, registry_credentials=registry_credentials, source=source, template_id=template_id, template_service_id=template_service_id, variables=variables)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Service.model_validate(self._execute(query, variables).get("serviceCreate"))

    def service_delete(self, id: str, *, environment_id: Optional[str] = None) -> bool:
        query = """mutation($environmentId: String, $id: String!) { serviceDelete(environmentId: $environmentId, id: $id) }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("serviceDelete")

    def service_disconnect(self, id: str) -> "Service":
        query = """mutation($id: String!) { serviceDisconnect(id: $id) { createdAt deletedAt hasHiddenRegistryCredentialsFromTemplate icon id name projectId templateId templateServiceId templateThreadSlug updatedAt project { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Service.model_validate(self._execute(query, variables).get("serviceDisconnect"))

    def service_domain_create(self, environment_id: str, service_id: str, *, target_port: Optional[int] = None) -> "ServiceDomain":
        query = """mutation($input: ServiceDomainCreateInput!) { serviceDomainCreate(input: $input) { cdnMode createdAt deletedAt domain edgeId environmentId id newDomainName newHostLabel projectId serviceId suffix targetPort updatedAt } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(ServiceDomainCreateInput(environment_id=environment_id, service_id=service_id, target_port=target_port)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return ServiceDomain.model_validate(self._execute(query, variables).get("serviceDomainCreate"))

    def service_domain_delete(self, id: str) -> bool:
        query = """mutation($id: String!) { serviceDomainDelete(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("serviceDomainDelete")

    def service_domain_update(self, domain: str, environment_id: str, service_domain_id: str, service_id: str, *, target_port: Optional[int] = None) -> bool:
        query = """mutation($input: ServiceDomainUpdateInput!) { serviceDomainUpdate(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(ServiceDomainUpdateInput(domain=domain, environment_id=environment_id, service_domain_id=service_domain_id, service_id=service_id, target_port=target_port)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("serviceDomainUpdate")

    def service_duplicate(self, environment_id: str, service_id: str) -> "Service":
        query = """mutation($environmentId: String!, $serviceId: String!) { serviceDuplicate(environmentId: $environmentId, serviceId: $serviceId) { createdAt deletedAt hasHiddenRegistryCredentialsFromTemplate icon id name projectId templateId templateServiceId templateThreadSlug updatedAt project { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "serviceId": _prepare_input(service_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Service.model_validate(self._execute(query, variables).get("serviceDuplicate"))

    def service_feature_flag_add(self, flag: "ActiveServiceFeatureFlag", service_id: str) -> bool:
        query = """mutation($input: ServiceFeatureFlagToggleInput!) { serviceFeatureFlagAdd(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(ServiceFeatureFlagToggleInput(flag=flag, service_id=service_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("serviceFeatureFlagAdd")

    def service_feature_flag_remove(self, flag: "ActiveServiceFeatureFlag", service_id: str) -> bool:
        query = """mutation($input: ServiceFeatureFlagToggleInput!) { serviceFeatureFlagRemove(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(ServiceFeatureFlagToggleInput(flag=flag, service_id=service_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("serviceFeatureFlagRemove")

    def service_instance_deploy(self, environment_id: str, service_id: str, *, commit_sha: Optional[str] = None, latest_commit: Optional[bool] = None) -> bool:
        query = """mutation($commitSha: String, $environmentId: String!, $latestCommit: Boolean, $serviceId: String!) { serviceInstanceDeploy(commitSha: $commitSha, environmentId: $environmentId, latestCommit: $latestCommit, serviceId: $serviceId) }"""
        variables: dict[str, Any] = {
            "commitSha": _prepare_input(commit_sha),
            "environmentId": _prepare_input(environment_id),
            "latestCommit": _prepare_input(latest_commit),
            "serviceId": _prepare_input(service_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("serviceInstanceDeploy")

    def service_instance_deploy_v2(self, environment_id: str, service_id: str, *, commit_sha: Optional[str] = None) -> str:
        query = """mutation($commitSha: String, $environmentId: String!, $serviceId: String!) { serviceInstanceDeployV2(commitSha: $commitSha, environmentId: $environmentId, serviceId: $serviceId) }"""
        variables: dict[str, Any] = {
            "commitSha": _prepare_input(commit_sha),
            "environmentId": _prepare_input(environment_id),
            "serviceId": _prepare_input(service_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("serviceInstanceDeployV2")

    def service_instance_limits_update(self, environment_id: str, service_id: str, *, memory_gb: Optional[float] = None, v_cp_us: Optional[float] = None) -> bool:
        query = """mutation($input: ServiceInstanceLimitsUpdateInput!) { serviceInstanceLimitsUpdate(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(ServiceInstanceLimitsUpdateInput(environment_id=environment_id, memory_gb=memory_gb, service_id=service_id, v_cp_us=v_cp_us)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("serviceInstanceLimitsUpdate")

    def service_instance_redeploy(self, environment_id: str, service_id: str) -> bool:
        query = """mutation($environmentId: String!, $serviceId: String!) { serviceInstanceRedeploy(environmentId: $environmentId, serviceId: $serviceId) }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "serviceId": _prepare_input(service_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("serviceInstanceRedeploy")

    def service_instance_update(self, service_id: str, *, environment_id: Optional[str] = None, build_command: Optional[str] = None, builder: Optional["Builder"] = None, cron_schedule: Optional[str] = None, dockerfile_path: Optional[str] = None, draining_seconds: Optional[int] = None, healthcheck_path: Optional[str] = None, healthcheck_timeout: Optional[int] = None, ipv6_egress_enabled: Optional[bool] = None, multi_region_config: Optional[Any] = None, nixpacks_plan: Optional[Any] = None, num_replicas: Optional[int] = None, overlap_seconds: Optional[int] = None, pre_deploy_command: Optional[list[str]] = None, railway_config_file: Optional[str] = None, region: Optional[str] = None, registry_credentials: Optional["RegistryCredentialsInput"] = None, restart_policy_max_retries: Optional[int] = None, restart_policy_type: Optional["RestartPolicyType"] = None, root_directory: Optional[str] = None, sleep_application: Optional[bool] = None, source: Optional["ServiceSourceInput"] = None, start_command: Optional[str] = None, watch_patterns: Optional[list[str]] = None) -> bool:
        query = """mutation($environmentId: String, $input: ServiceInstanceUpdateInput!, $serviceId: String!) { serviceInstanceUpdate(environmentId: $environmentId, input: $input, serviceId: $serviceId) }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "input": _prepare_input(ServiceInstanceUpdateInput(build_command=build_command, builder=builder, cron_schedule=cron_schedule, dockerfile_path=dockerfile_path, draining_seconds=draining_seconds, healthcheck_path=healthcheck_path, healthcheck_timeout=healthcheck_timeout, ipv6_egress_enabled=ipv6_egress_enabled, multi_region_config=multi_region_config, nixpacks_plan=nixpacks_plan, num_replicas=num_replicas, overlap_seconds=overlap_seconds, pre_deploy_command=pre_deploy_command, railway_config_file=railway_config_file, region=region, registry_credentials=registry_credentials, restart_policy_max_retries=restart_policy_max_retries, restart_policy_type=restart_policy_type, root_directory=root_directory, sleep_application=sleep_application, source=source, start_command=start_command, watch_patterns=watch_patterns)),
            "serviceId": _prepare_input(service_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("serviceInstanceUpdate")

    def service_remove_upstream_url(self, id: str) -> "Service":
        query = """mutation($id: String!) { serviceRemoveUpstreamUrl(id: $id) { createdAt deletedAt hasHiddenRegistryCredentialsFromTemplate icon id name projectId templateId templateServiceId templateThreadSlug updatedAt project { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Service.model_validate(self._execute(query, variables).get("serviceRemoveUpstreamUrl"))

    def service_update(self, id: str, *, icon: Optional[str] = None, name: Optional[str] = None) -> "Service":
        query = """mutation($id: String!, $input: ServiceUpdateInput!) { serviceUpdate(id: $id, input: $input) { createdAt deletedAt hasHiddenRegistryCredentialsFromTemplate icon id name projectId templateId templateServiceId templateThreadSlug updatedAt project { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "input": _prepare_input(ServiceUpdateInput(icon=icon, name=name)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Service.model_validate(self._execute(query, variables).get("serviceUpdate"))

    def session_delete(self, id: str) -> bool:
        query = """mutation($id: String!) { sessionDelete(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("sessionDelete")

    def shared_variable_configure(self, disabled_service_ids: list[str], enabled_service_ids: list[str], environment_id: str, name: str, project_id: str) -> "Variable":
        query = """mutation($input: SharedVariableConfigureInput!) { sharedVariableConfigure(input: $input) { createdAt environmentId id isSealed name pluginId references serviceId updatedAt environment { canAccess createdAt deletedAt id isEphemeral name projectId unmergedChangesCount updatedAt } plugin { createdAt deletedAt deprecatedAt friendlyName id logsEnabled migrationDatabaseServiceId } service { createdAt deletedAt hasHiddenRegistryCredentialsFromTemplate icon id name projectId templateId templateServiceId templateThreadSlug updatedAt } } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(SharedVariableConfigureInput(disabled_service_ids=disabled_service_ids, enabled_service_ids=enabled_service_ids, environment_id=environment_id, name=name, project_id=project_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Variable.model_validate(self._execute(query, variables).get("sharedVariableConfigure"))

    def ssh_public_key_create(self, name: str, public_key: str) -> "SshPublicKey":
        query = """mutation($input: SshPublicKeyCreateInput!) { sshPublicKeyCreate(input: $input) { createdAt fingerprint id name publicKey updatedAt } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(SshPublicKeyCreateInput(name=name, public_key=public_key)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return SshPublicKey.model_validate(self._execute(query, variables).get("sshPublicKeyCreate"))

    def ssh_public_key_delete(self, id: str) -> bool:
        query = """mutation($id: String!) { sshPublicKeyDelete(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("sshPublicKeyDelete")

    def tcp_proxy_create(self, application_port: int, environment_id: str, service_id: str) -> "TCPProxy":
        query = """mutation($input: TCPProxyCreateInput!) { tcpProxyCreate(input: $input) { applicationPort createdAt deletedAt domain environmentId id proxyPort serviceId updatedAt } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(TCPProxyCreateInput(application_port=application_port, environment_id=environment_id, service_id=service_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return TCPProxy.model_validate(self._execute(query, variables).get("tcpProxyCreate"))

    def tcp_proxy_delete(self, id: str) -> bool:
        query = """mutation($id: String!) { tcpProxyDelete(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("tcpProxyDelete")

    def template_clone(self, code: str, *, workspace_id: Optional[str] = None) -> "Template":
        query = """mutation($input: TemplateCloneInput!) { templateClone(input: $input) { activeProjects canvasConfig category code communityThreadSlug config createdAt demoProjectId description health id image isApproved isV2Template isVerified languages metadata name projects readme recentProjects serializedConfig supportHealthMetrics tags teamId totalPayout workspaceId creator { avatar hasPublicProfile name username } guides { post video } similarTemplates { code createdAt deploys description health image name teamId userId workspaceId } } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(TemplateCloneInput(code=code, workspace_id=workspace_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Template.model_validate(self._execute(query, variables).get("templateClone"))

    def template_delete(self, id: str, *, workspace_id: Optional[str] = None) -> bool:
        query = """mutation($id: String!, $input: TemplateDeleteInput!) { templateDelete(id: $id, input: $input) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "input": _prepare_input(TemplateDeleteInput(workspace_id=workspace_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("templateDelete")

    def template_deploy(self, services: list["TemplateDeployService"], *, environment_id: Optional[str] = None, project_id: Optional[str] = None, template_code: Optional[str] = None, workspace_id: Optional[str] = None) -> "TemplateDeployPayload":
        query = """mutation($input: TemplateDeployInput!) { templateDeploy(input: $input) { projectId workflowId } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(TemplateDeployInput(environment_id=environment_id, project_id=project_id, services=services, template_code=template_code, workspace_id=workspace_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return TemplateDeployPayload.model_validate(self._execute(query, variables).get("templateDeploy"))

    def template_deploy_v2(self, serialized_config: Any, template_id: str, *, environment_id: Optional[str] = None, project_id: Optional[str] = None, workspace_id: Optional[str] = None) -> "TemplateDeployPayload":
        query = """mutation($input: TemplateDeployV2Input!) { templateDeployV2(input: $input) { projectId workflowId } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(TemplateDeployV2Input(environment_id=environment_id, project_id=project_id, serialized_config=serialized_config, template_id=template_id, workspace_id=workspace_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return TemplateDeployPayload.model_validate(self._execute(query, variables).get("templateDeployV2"))

    def template_generate(self, project_id: str, *, environment_id: Optional[str] = None) -> "Template":
        query = """mutation($input: TemplateGenerateInput!) { templateGenerate(input: $input) { activeProjects canvasConfig category code communityThreadSlug config createdAt demoProjectId description health id image isApproved isV2Template isVerified languages metadata name projects readme recentProjects serializedConfig supportHealthMetrics tags teamId totalPayout workspaceId creator { avatar hasPublicProfile name username } guides { post video } similarTemplates { code createdAt deploys description health image name teamId userId workspaceId } } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(TemplateGenerateInput(environment_id=environment_id, project_id=project_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Template.model_validate(self._execute(query, variables).get("templateGenerate"))

    def template_publish(self, id: str, category: str, description: str, readme: str, *, demo_project_id: Optional[str] = None, image: Optional[str] = None, workspace_id: Optional[str] = None) -> "Template":
        query = """mutation($id: String!, $input: TemplatePublishInput!) { templatePublish(id: $id, input: $input) { activeProjects canvasConfig category code communityThreadSlug config createdAt demoProjectId description health id image isApproved isV2Template isVerified languages metadata name projects readme recentProjects serializedConfig supportHealthMetrics tags teamId totalPayout workspaceId creator { avatar hasPublicProfile name username } guides { post video } similarTemplates { code createdAt deploys description health image name teamId userId workspaceId } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "input": _prepare_input(TemplatePublishInput(category=category, demo_project_id=demo_project_id, description=description, image=image, readme=readme, workspace_id=workspace_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Template.model_validate(self._execute(query, variables).get("templatePublish"))

    def template_service_source_eject(self, project_id: str, repo_name: str, repo_owner: str, service_ids: list[str], upstream_url: str) -> bool:
        query = """mutation($input: TemplateServiceSourceEjectInput!) { templateServiceSourceEject(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(TemplateServiceSourceEjectInput(project_id=project_id, repo_name=repo_name, repo_owner=repo_owner, service_ids=service_ids, upstream_url=upstream_url)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("templateServiceSourceEject")

    def template_unpublish(self, id: str) -> bool:
        query = """mutation($id: String!) { templateUnpublish(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("templateUnpublish")

    def trusted_domain_create(self, domain_name: str, role: str, workspace_id: str) -> "TrustedDomain":
        query = """mutation($input: WorkspaceTrustedDomainCreateInput!) { trustedDomainCreate(input: $input) { domainName id role verificationType workspaceId verificationData { dnsHost token } } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(WorkspaceTrustedDomainCreateInput(domain_name=domain_name, role=role, workspace_id=workspace_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return TrustedDomain.model_validate(self._execute(query, variables).get("trustedDomainCreate"))

    def trusted_domain_delete(self, id: str) -> bool:
        query = """mutation($id: String!) { trustedDomainDelete(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("trustedDomainDelete")

    def trusted_domain_retrigger_verification(self, id: str) -> Optional["TrustedDomain"]:
        query = """mutation($id: String!) { trustedDomainRetriggerVerification(id: $id) { domainName id role verificationType workspaceId verificationData { dnsHost token } } }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        _data = self._execute(query, variables).get("trustedDomainRetriggerVerification")
        return TrustedDomain.model_validate(_data) if _data else None

    def two_factor_info_create(self, token: str) -> "RecoveryCodes":
        query = """mutation($input: TwoFactorInfoCreateInput!) { twoFactorInfoCreate(input: $input) { recoveryCodes } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(TwoFactorInfoCreateInput(token=token)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return RecoveryCodes.model_validate(self._execute(query, variables).get("twoFactorInfoCreate"))

    def two_factor_info_delete(self) -> bool:
        query = """mutation { twoFactorInfoDelete }"""
        return self._execute(query).get("twoFactorInfoDelete")

    def two_factor_info_secret(self) -> "TwoFactorInfoSecret":
        query = """mutation { twoFactorInfoSecret { secret uri } }"""
        return TwoFactorInfoSecret.model_validate(self._execute(query).get("twoFactorInfoSecret"))

    def two_factor_info_validate(self, token: str, *, two_factor_linking_key: Optional[str] = None) -> bool:
        query = """mutation($input: TwoFactorInfoValidateInput!) { twoFactorInfoValidate(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(TwoFactorInfoValidateInput(token=token, two_factor_linking_key=two_factor_linking_key)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("twoFactorInfoValidate")

    def upsert_slack_channel(self, workspace_id: str) -> bool:
        query = """mutation($workspaceId: String!) { upsertSlackChannel(workspaceId: $workspaceId) }"""
        variables: dict[str, Any] = {
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("upsertSlackChannel")

    def usage_limit_remove(self, customer_id: str) -> bool:
        query = """mutation($input: UsageLimitRemoveInput!) { usageLimitRemove(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(UsageLimitRemoveInput(customer_id=customer_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("usageLimitRemove")

    def usage_limit_set(self, customer_id: str, soft_limit_dollars: int, *, hard_limit_dollars: Optional[int] = None) -> bool:
        query = """mutation($input: UsageLimitSetInput!) { usageLimitSet(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(UsageLimitSetInput(customer_id=customer_id, hard_limit_dollars=hard_limit_dollars, soft_limit_dollars=soft_limit_dollars)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("usageLimitSet")

    def user_beta_leave(self) -> bool:
        query = """mutation { userBetaLeave }"""
        return self._execute(query).get("userBetaLeave")

    def user_delete(self) -> bool:
        query = """mutation { userDelete }"""
        return self._execute(query).get("userDelete")

    def user_discord_disconnect(self) -> bool:
        query = """mutation { userDiscordDisconnect }"""
        return self._execute(query).get("userDiscordDisconnect")

    def user_flags_remove(self, flags: list["UserFlag"], *, user_id: Optional[str] = None) -> bool:
        query = """mutation($input: UserFlagsRemoveInput!) { userFlagsRemove(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(UserFlagsRemoveInput(flags=flags, user_id=user_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("userFlagsRemove")

    def user_flags_set(self, flags: list["UserFlag"], *, user_id: Optional[str] = None) -> bool:
        query = """mutation($input: UserFlagsSetInput!) { userFlagsSet(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(UserFlagsSetInput(flags=flags, user_id=user_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("userFlagsSet")

    def user_profile_update(self, is_public: bool, *, bio: Optional[str] = None, website: Optional[str] = None) -> bool:
        query = """mutation($input: UserProfileUpdateInput!) { userProfileUpdate(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(UserProfileUpdateInput(bio=bio, is_public=is_public, website=website)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("userProfileUpdate")

    def user_terms_update(self) -> Optional["User"]:
        query = """mutation { userTermsUpdate { agreedFairUse avatar banReason createdAt email githubProviderId githubUsername has2FA hasPasskeys id isAdmin isConductor isVerified lastLogin name riskLevel termsAgreedOn username apiTokenRateLimit { remainingPoints resetsAt } profile { bio isPublic website } workspace { adoptionLevel allowDeprecatedRegions avatar banReason createdAt discordRole has2FAEnforcement hasGuardrailsAccess hasSAML id name preferredRegion redactedDueTo2FAPending slackChannelId subscriptionPlanLimit updatedAt usersWithout2FA } workspaces { adoptionLevel allowDeprecatedRegions avatar banReason createdAt discordRole has2FAEnforcement hasGuardrailsAccess hasSAML id name preferredRegion redactedDueTo2FAPending slackChannelId subscriptionPlanLimit updatedAt usersWithout2FA } } }"""
        _data = self._execute(query).get("userTermsUpdate")
        return User.model_validate(_data) if _data else None

    def variable_collection_upsert(self, environment_id: str, project_id: str, variables: Any, *, replace: Optional[bool] = None, service_id: Optional[str] = None, skip_deploys: Optional[bool] = None) -> bool:
        query = """mutation($input: VariableCollectionUpsertInput!) { variableCollectionUpsert(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(VariableCollectionUpsertInput(environment_id=environment_id, project_id=project_id, replace=replace, service_id=service_id, skip_deploys=skip_deploys, variables=variables)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("variableCollectionUpsert")

    def variable_delete(self, environment_id: str, name: str, project_id: str, *, service_id: Optional[str] = None) -> bool:
        query = """mutation($input: VariableDeleteInput!) { variableDelete(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(VariableDeleteInput(environment_id=environment_id, name=name, project_id=project_id, service_id=service_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("variableDelete")

    def variable_upsert(self, environment_id: str, name: str, project_id: str, value: str, *, service_id: Optional[str] = None, skip_deploys: Optional[bool] = None) -> bool:
        query = """mutation($input: VariableUpsertInput!) { variableUpsert(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(VariableUpsertInput(environment_id=environment_id, name=name, project_id=project_id, service_id=service_id, skip_deploys=skip_deploys, value=value)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("variableUpsert")

    def volume_create(self, mount_path: str, project_id: str, *, environment_id: Optional[str] = None, region: Optional[str] = None, service_id: Optional[str] = None) -> "Volume":
        query = """mutation($input: VolumeCreateInput!) { volumeCreate(input: $input) { createdAt id name projectId project { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(VolumeCreateInput(environment_id=environment_id, mount_path=mount_path, project_id=project_id, region=region, service_id=service_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Volume.model_validate(self._execute(query, variables).get("volumeCreate"))

    def volume_delete(self, volume_id: str) -> bool:
        query = """mutation($volumeId: String!) { volumeDelete(volumeId: $volumeId) }"""
        variables: dict[str, Any] = {
            "volumeId": _prepare_input(volume_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("volumeDelete")

    def volume_instance_backup_create(self, volume_instance_id: str, *, name: Optional[str] = None) -> "WorkflowId":
        query = """mutation($name: String, $volumeInstanceId: String!) { volumeInstanceBackupCreate(name: $name, volumeInstanceId: $volumeInstanceId) { workflowId } }"""
        variables: dict[str, Any] = {
            "name": _prepare_input(name),
            "volumeInstanceId": _prepare_input(volume_instance_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return WorkflowId.model_validate(self._execute(query, variables).get("volumeInstanceBackupCreate"))

    def volume_instance_backup_delete(self, volume_instance_backup_id: str, volume_instance_id: str) -> "WorkflowId":
        query = """mutation($volumeInstanceBackupId: String!, $volumeInstanceId: String!) { volumeInstanceBackupDelete(volumeInstanceBackupId: $volumeInstanceBackupId, volumeInstanceId: $volumeInstanceId) { workflowId } }"""
        variables: dict[str, Any] = {
            "volumeInstanceBackupId": _prepare_input(volume_instance_backup_id),
            "volumeInstanceId": _prepare_input(volume_instance_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return WorkflowId.model_validate(self._execute(query, variables).get("volumeInstanceBackupDelete"))

    def volume_instance_backup_lock(self, volume_instance_backup_id: str, volume_instance_id: str) -> bool:
        query = """mutation($volumeInstanceBackupId: String!, $volumeInstanceId: String!) { volumeInstanceBackupLock(volumeInstanceBackupId: $volumeInstanceBackupId, volumeInstanceId: $volumeInstanceId) }"""
        variables: dict[str, Any] = {
            "volumeInstanceBackupId": _prepare_input(volume_instance_backup_id),
            "volumeInstanceId": _prepare_input(volume_instance_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("volumeInstanceBackupLock")

    def volume_instance_backup_restore(self, volume_instance_backup_id: str, volume_instance_id: str) -> "WorkflowId":
        query = """mutation($volumeInstanceBackupId: String!, $volumeInstanceId: String!) { volumeInstanceBackupRestore(volumeInstanceBackupId: $volumeInstanceBackupId, volumeInstanceId: $volumeInstanceId) { workflowId } }"""
        variables: dict[str, Any] = {
            "volumeInstanceBackupId": _prepare_input(volume_instance_backup_id),
            "volumeInstanceId": _prepare_input(volume_instance_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return WorkflowId.model_validate(self._execute(query, variables).get("volumeInstanceBackupRestore"))

    def volume_instance_backup_schedule_update(self, kinds: list["VolumeInstanceBackupScheduleKind"], volume_instance_id: str) -> bool:
        query = """mutation($kinds: [VolumeInstanceBackupScheduleKind!]!, $volumeInstanceId: String!) { volumeInstanceBackupScheduleUpdate(kinds: $kinds, volumeInstanceId: $volumeInstanceId) }"""
        variables: dict[str, Any] = {
            "kinds": _prepare_input(kinds),
            "volumeInstanceId": _prepare_input(volume_instance_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("volumeInstanceBackupScheduleUpdate")

    def volume_instance_update(self, volume_id: str, *, environment_id: Optional[str] = None, mount_path: Optional[str] = None, service_id: Optional[str] = None, state: Optional["VolumeState"] = None) -> bool:
        query = """mutation($environmentId: String, $input: VolumeInstanceUpdateInput!, $volumeId: String!) { volumeInstanceUpdate(environmentId: $environmentId, input: $input, volumeId: $volumeId) }"""
        variables: dict[str, Any] = {
            "environmentId": _prepare_input(environment_id),
            "input": _prepare_input(VolumeInstanceUpdateInput(mount_path=mount_path, service_id=service_id, state=state)),
            "volumeId": _prepare_input(volume_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("volumeInstanceUpdate")

    def volume_update(self, volume_id: str, *, name: Optional[str] = None) -> "Volume":
        query = """mutation($input: VolumeUpdateInput!, $volumeId: String!) { volumeUpdate(input: $input, volumeId: $volumeId) { createdAt id name projectId project { baseEnvironmentId botPrEnvironments createdAt deletedAt description expiredAt focusedPrEnvironments id isPublic isTempProject name prDeploys subscriptionPlanLimit teamId updatedAt workspaceId } } }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(VolumeUpdateInput(name=name)),
            "volumeId": _prepare_input(volume_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Volume.model_validate(self._execute(query, variables).get("volumeUpdate"))

    def webhook_test(self, payload: str, url: str) -> int:
        query = """mutation($payload: String!, $url: String!) { webhookTest(payload: $payload, url: $url) }"""
        variables: dict[str, Any] = {
            "payload": _prepare_input(payload),
            "url": _prepare_input(url),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("webhookTest")

    def workspace_delete(self, id: str) -> bool:
        query = """mutation($id: String!) { workspaceDelete(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("workspaceDelete")

    def workspace_invite_code_create(self, role: str, workspace_id: str) -> str:
        query = """mutation($input: WorkspaceInviteCodeCreateInput!, $workspaceId: String!) { workspaceInviteCodeCreate(input: $input, workspaceId: $workspaceId) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(WorkspaceInviteCodeCreateInput(role=role)),
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("workspaceInviteCodeCreate")

    def workspace_invite_code_use(self, code: str) -> "Workspace":
        query = """mutation($code: String!) { workspaceInviteCodeUse(code: $code) { adoptionLevel allowDeprecatedRegions avatar banReason createdAt discordRole has2FAEnforcement hasGuardrailsAccess hasSAML id name preferredRegion redactedDueTo2FAPending slackChannelId subscriptionPlanLimit updatedAt usersWithout2FA adoptionHistory { adoptionLevel createdAt deltaLevel id matchedIcpEmail monthlyEstimatedUsage numConfigFile numCronSchedule numDeploys numEnvs numFailedDeploys numHealthcheck numIconConfig numRegion numReplicas numRootDirectory numSeats numServices numVariables numWatchPatterns totalCores totalDisk totalNetwork updatedAt } apiTokenRateLimit { remainingPoints resetsAt } customer { appliedCredits billingEmail creditBalance currentUsage defaultPaymentMethodId hasExhaustedFreePlan id isPrepaying isTrialing isUsageSubscriber isWithdrawingToCredits remainingUsageCreditBalance stripeCustomerId trialDaysRemaining } members { avatar email id name twoFactorAuthEnabled } partnerProfile { category description slug website } referredUsers { code id } team { adoptionLevel avatar createdAt id name preferredRegion slackChannelId updatedAt } } }"""
        variables: dict[str, Any] = {
            "code": _prepare_input(code),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return Workspace.model_validate(self._execute(query, variables).get("workspaceInviteCodeUse"))

    def workspace_leave(self, id: str) -> bool:
        query = """mutation($id: String!) { workspaceLeave(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("workspaceLeave")

    def workspace_permission_change(self, role: "TeamRole", user_id: str, workspace_id: str) -> bool:
        query = """mutation($input: WorkspacePermissionChangeInput!) { workspacePermissionChange(input: $input) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(WorkspacePermissionChangeInput(role=role, user_id=user_id, workspace_id=workspace_id)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("workspacePermissionChange")

    def workspace_policy_item_update(self, enabled: bool, policy: "WorkspacePolicyName", workspace_id: str, *, _enabled: Optional[bool] = None, _policy: Optional["WorkspacePolicyName"] = None) -> bool:
        query = """mutation($enabled: Boolean, $input: WorkspacePolicyItemUpdateInput, $policy: WorkspacePolicyName, $workspaceId: String!) { workspacePolicyItemUpdate(enabled: $enabled, input: $input, policy: $policy, workspaceId: $workspaceId) }"""
        variables: dict[str, Any] = {
            "enabled": _prepare_input(_enabled),
            "input": _prepare_input(WorkspacePolicyItemUpdateInput(enabled=enabled, policy=policy)),
            "policy": _prepare_input(_policy),
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("workspacePolicyItemUpdate")

    def workspace_two_factor_enforcement_update(self, enabled: bool, workspace_id: str) -> bool:
        query = """mutation($enabled: Boolean!, $workspaceId: String!) { workspaceTwoFactorEnforcementUpdate(enabled: $enabled, workspaceId: $workspaceId) }"""
        variables: dict[str, Any] = {
            "enabled": _prepare_input(enabled),
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("workspaceTwoFactorEnforcementUpdate")

    def workspace_update(self, id: str, *, avatar: Optional[str] = None, name: Optional[str] = None, preferred_region: Optional[str] = None) -> bool:
        query = """mutation($id: String!, $input: WorkspaceUpdateInput!) { workspaceUpdate(id: $id, input: $input) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
            "input": _prepare_input(WorkspaceUpdateInput(avatar=avatar, name=name, preferred_region=preferred_region)),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("workspaceUpdate")

    def workspace_upsert_slack_channel(self, id: str) -> bool:
        query = """mutation($id: String!) { workspaceUpsertSlackChannel(id: $id) }"""
        variables: dict[str, Any] = {
            "id": _prepare_input(id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("workspaceUpsertSlackChannel")

    def workspace_user_invite(self, code: str, email: str, workspace_id: str) -> bool:
        query = """mutation($input: WorkspaceUserInviteInput!, $workspaceId: String!) { workspaceUserInvite(input: $input, workspaceId: $workspaceId) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(WorkspaceUserInviteInput(code=code, email=email)),
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("workspaceUserInvite")

    def workspace_user_remove(self, user_id: str, workspace_id: str) -> bool:
        query = """mutation($input: WorkspaceUserRemoveInput!, $workspaceId: String!) { workspaceUserRemove(input: $input, workspaceId: $workspaceId) }"""
        variables: dict[str, Any] = {
            "input": _prepare_input(WorkspaceUserRemoveInput(user_id=user_id)),
            "workspaceId": _prepare_input(workspace_id),
        }
        variables = {k: v for k, v in variables.items() if v is not None}
        return self._execute(query, variables).get("workspaceUserRemove")
