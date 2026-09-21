DEEP_DIVE_LESSONS = [
    {
        'title': '01. DevOps Mindset and Delivery Flow',
        'content': '''# DevOps Mindset and Delivery Flow

DevOps is a delivery and operations system where development and operations share ownership of customer outcomes. The goal is not simply to deploy faster; it is to deliver useful changes safely, learn from production, and reduce the time between an idea and customer value.

## The loop

Discover a need, plan a small change, code and review it, build and test it, release it, observe it in production, then improve the next change. Keep batches small, automate the reliable path, and version application code, infrastructure, policy, and documentation together.

## Engineering metrics

Track lead time, deployment frequency, change failure rate, and time to restore service. Pair delivery metrics with product and reliability outcomes so speed does not become reckless change.''',
        'objectives': ['Explain DevOps as a delivery system', 'Describe the software delivery loop', 'Identify useful delivery and reliability metrics'],
        'commands': [{'command': 'git log --oneline --decorate -10', 'explanation': 'Inspect recent delivery history.', 'expected_output': 'A readable list of recent commits'}],
    },
    {
        'title': '02. Linux, Shell, and Process Fundamentals',
        'content': '''# Linux, Shell, and Process Fundamentals

Linux is the operating environment behind most production platforms. Learn processes, filesystems, permissions, networking tools, service managers, logs, and shell composition before relying on higher-level platforms.

Use `set -euo pipefail` in automation, check exit codes, quote variables, and make scripts idempotent. Troubleshoot from evidence to hypothesis: inspect service state, read recent logs, verify listening ports, test dependencies, and change one thing at a time.''',
        'objectives': ['Diagnose a process or service failure', 'Use shell pipelines safely', 'Inspect permissions, ports, and logs'],
        'commands': [{'command': 'ps aux --sort=-%cpu | head', 'explanation': 'Find processes consuming the most CPU.', 'expected_output': 'A sorted process list'}, {'command': 'ss -tulpn', 'explanation': 'Inspect listening sockets.', 'expected_output': 'Listening services and ports'}, {'command': 'journalctl -u nginx --since "30 minutes ago"', 'explanation': 'Read recent service logs.', 'expected_output': 'Timestamped service events'}],
    },
    {
        'title': '03. Git, Collaboration, and Trunk-Based Development',
        'content': '''# Git, Collaboration, and Trunk-Based Development

Git helps teams maintain a trustworthy history. Keep commits focused and reversible, use short-lived branches, protect the default branch, require green checks, and make releases traceable with tags. Store secrets outside Git and rotate anything that is committed accidentally.

Trunk-based development integrates small changes frequently. Feature flags allow incomplete work to merge without exposing it to users, reducing long-running branch drift and integration risk.''',
        'objectives': ['Create reviewable commits', 'Resolve merge conflicts safely', 'Explain protected branches and feature flags'],
        'commands': [{'command': 'git switch -c feature/health-check', 'explanation': 'Create a focused branch.', 'expected_output': 'Switched to a new branch'}, {'command': 'git diff --check', 'explanation': 'Find whitespace errors before review.', 'expected_output': 'No output when clean'}],
    },
    {
        'title': '04. Networking, HTTP, DNS, and TLS',
        'content': '''# Networking, HTTP, DNS, and TLS

Trace a request from client to DNS, TCP, TLS, load balancer, application, and dependencies. DNS maps names to addresses, TCP creates a connection, TLS authenticates and encrypts, and HTTP carries the request and response.

Distinguish DNS failure, connection timeout, TLS failure, HTTP 4xx, HTTP 5xx, and application errors. Use private networks, explicit firewall rules, health checks, timeouts, bounded retries with backoff, and idempotent handlers. Unbounded retries can amplify an outage.''',
        'objectives': ['Trace an HTTP request through network layers', 'Distinguish common connectivity failures', 'Design safe timeouts and retries'],
        'commands': [{'command': 'curl -I https://example.com', 'explanation': 'Inspect status and headers.', 'expected_output': 'HTTP response headers'}, {'command': 'dig example.com', 'explanation': 'Inspect DNS resolution.', 'expected_output': 'DNS answer records'}],
    },
    {
        'title': '05. Containers and Docker Image Engineering',
        'content': '''# Containers and Docker Image Engineering

A container is an isolated process with a filesystem, network namespace, resource limits, and a declared image. Use a trusted small base, pin versions, order Dockerfile layers for cache reuse, run as non-root, add health checks, and use multi-stage builds to keep toolchains out of runtime images.

Configuration belongs in environment variables or a secret manager. Logs go to standard output. Persistent state belongs in managed storage, not a disposable container filesystem. Compose is excellent for local multi-service development.''',
        'objectives': ['Build a reproducible container image', 'Explain image layers and multi-stage builds', 'Separate configuration, logs, and persistent data'],
        'commands': [{'command': 'docker build --pull --tag devops-api:local .', 'explanation': 'Build the image.', 'expected_output': 'Successfully built and tagged image'}, {'command': 'docker image inspect devops-api:local', 'explanation': 'Inspect image metadata.', 'expected_output': 'JSON image configuration'}],
    },
    {
        'title': '06. Kubernetes Core Objects and Scheduling',
        'content': '''# Kubernetes Core Objects and Scheduling

Kubernetes continuously reconciles desired state with observed cluster state. A Pod is the smallest scheduled unit, a Deployment manages replicas and rollouts, a Service provides a stable endpoint, and an Ingress or Gateway exposes routes.

Requests and limits influence scheduling. Readiness controls traffic; liveness controls restarts. A process can be alive but not ready. Use namespaces, ConfigMaps, Secrets, RBAC, quotas, and network policies to establish operational boundaries.''',
        'objectives': ['Describe Kubernetes reconciliation', 'Choose readiness and liveness behavior', 'Debug a failed rollout'],
        'commands': [{'command': 'kubectl get pods -A', 'explanation': 'List pods across namespaces.', 'expected_output': 'Pod status and age'}, {'command': 'kubectl rollout status deployment/devops-api', 'explanation': 'Check rollout progress.', 'expected_output': 'Successful rollout or failure'}, {'command': 'kubectl describe pod <pod-name>', 'explanation': 'Inspect events and container state.', 'expected_output': 'Pod details and events'}],
    },
    {
        'title': '07. Infrastructure as Code with Terraform',
        'content': '''# Infrastructure as Code with Terraform

Terraform describes desired resources, builds a dependency graph, previews changes, and stores state so later changes remain controlled. Format and validate first, review plans in code review, apply from a controlled identity, and store state remotely with locking and encryption.

Use modules for standards, variables for inputs, outputs for contracts, and policy checks for secure defaults. Never commit cloud credentials or sensitive state. Drift detection is useful only when the team has an owned reconciliation process.''',
        'objectives': ['Explain Terraform state and planning', 'Structure reusable modules', 'Identify drift and protect state'],
        'commands': [{'command': 'terraform fmt -check -recursive', 'explanation': 'Verify canonical formatting.', 'expected_output': 'No changes required'}, {'command': 'terraform validate', 'explanation': 'Validate configuration.', 'expected_output': 'Success message'}, {'command': 'terraform plan', 'explanation': 'Preview infrastructure changes.', 'expected_output': 'A reviewed execution plan'}],
    },
    {
        'title': '08. CI/CD Pipelines and Release Strategies',
        'content': '''# CI/CD Pipelines and Release Strategies

Continuous integration validates every change quickly. Continuous delivery keeps software releasable; continuous deployment promotes approved changes automatically. A strong pipeline checks out code, lints, tests, scans, builds an immutable artifact, deploys it, runs smoke tests, and provides promotion and rollback gates.

Rolling releases replace instances gradually. Blue-green releases switch between complete environments. Canary releases expose a small traffic percentage first. Every strategy needs health checks and a tested rollback path.''',
        'objectives': ['Design a staged delivery pipeline', 'Compare rolling, blue-green, and canary releases', 'Define promotion and rollback gates'],
        'commands': [{'command': 'python -m pytest', 'explanation': 'Run automated tests in CI.', 'expected_output': 'Passing test report'}, {'command': 'docker tag devops-api:local registry.example/devops-api:$GIT_SHA', 'explanation': 'Tag an immutable artifact.', 'expected_output': 'Tagged image ready to publish'}],
    },
    {
        'title': '09. Cloud Architecture and Reliability Patterns',
        'content': '''# Cloud Architecture and Reliability Patterns

Cloud design makes failure boundaries explicit. Separate tiers, isolate blast radius, use managed services where they remove undifferentiated work, and design for the recovery objective the business needs.

Common patterns include stateless application instances behind a load balancer, managed databases with tested restores, object storage for durable blobs, queues for asynchronous work, caches with correctness fallbacks, and private subnets with least-privilege identities. Availability is not durability, and backups are not a recovery plan until restoration is rehearsed.''',
        'objectives': ['Design a multi-tier cloud system', 'Explain availability, durability, and scalability', 'Choose asynchronous boundaries and recovery controls'],
        'commands': [{'command': 'aws sts get-caller-identity', 'explanation': 'Confirm the active cloud identity.', 'expected_output': 'Account and principal details'}, {'command': 'aws cloudformation validate-template --template-body file://template.yaml', 'explanation': 'Validate a template.', 'expected_output': 'Template validation success'}],
    },
    {
        'title': '10. DevSecOps and Supply Chain Security',
        'content': '''# DevSecOps and Supply Chain Security

Security is a continuous property of the delivery system. Protect source with review and secret scanning, build reproducibly with pinned dependencies and isolated runners, sign artifacts, scan images, run workloads as non-root, and enforce runtime RBAC, network policies, admission controls, encryption, and audit logging.

Prioritize vulnerabilities using exploitability and exposure, not scanner count alone. A critical package in an internet-facing runtime deserves a different response from an unreachable development dependency.''',
        'objectives': ['Add security checks to a delivery pipeline', 'Apply least privilege to workloads', 'Prioritize vulnerability findings'],
        'commands': [{'command': 'trivy image --severity HIGH,CRITICAL devops-api:local', 'explanation': 'Scan an image.', 'expected_output': 'Vulnerability report'}, {'command': 'git secrets --scan', 'explanation': 'Check for committed credentials.', 'expected_output': 'No secrets detected'}],
    },
    {
        'title': '11. Observability with Metrics, Logs, and Traces',
        'content': '''# Observability with Metrics, Logs, and Traces

Monitoring reports known conditions. Observability helps investigate unknown failures by connecting signals to system behavior and user impact. Metrics are efficient for trends and alerts, structured logs provide detail and correlation IDs, and traces show where a request spends time across services.

Instrument user journeys, not only infrastructure saturation. Alerts should be actionable, routed to an owner, and linked to a runbook. Control label cardinality so metrics remain affordable and queryable.''',
        'objectives': ['Select the right signal for an investigation', 'Create actionable alerts', 'Connect logs and traces with correlation context'],
        'commands': [{'command': 'curl http://localhost:8000/metrics', 'explanation': 'Inspect Prometheus metrics.', 'expected_output': 'Metric names and samples'}, {'command': 'kubectl logs deployment/devops-api --since=10m', 'explanation': 'Review recent logs.', 'expected_output': 'Timestamped log events'}],
    },
    {
        'title': '12. SRE, SLOs, Incident Response, and AIOps',
        'content': '''# SRE, SLOs, Incident Response, and AIOps

Site Reliability Engineering applies software engineering to operations. Define a service level indicator, set a service level objective, and use the error budget to balance reliability work with feature delivery.

During incidents, declare early, assign an incident commander, separate coordination from investigation, communicate status, mitigate before perfect diagnosis, and write a blameless review with owned follow-up work. AIOps can correlate signals and suggest causes, but impactful remediation should require human approval and remain reversible, observable, and permission-limited.''',
        'objectives': ['Define an SLI and SLO', 'Run structured incident response', 'Evaluate safe boundaries for AIOps automation'],
        'commands': [{'command': 'kubectl rollout undo deployment/devops-api', 'explanation': 'Rollback to a safer version.', 'expected_output': 'Deployment rollback initiated'}, {'command': 'git tag incident-checkpoint', 'explanation': 'Record a traceable incident checkpoint.', 'expected_output': 'Tag created'}],
    },
]
