# Gradle Quality and Security Pipeline

This project demonstrates a Jenkins pipeline using:

- Gradle for build and tests
- SonarQube for static code quality analysis
- Trivy for filesystem and container vulnerability scanning
- Prometheus and Alertmanager for CI monitoring notifications

## Jenkins prerequisites

Install or configure these on the Jenkins controller/agent:

- JDK 17+
- Git
- Docker, if running the Trivy image scan
- Trivy CLI
- Gradle 8+ configured in Jenkins with the tool name `gradle8`
- Jenkins plugins: Pipeline, Git, JUnit, SonarQube Scanner

Configure a Jenkins SonarQube installation named `sonarqube` and provide the project token as a protected credential. Do not commit tokens to source control.

## Run locally

```powershell
gradle test
```

## Start local quality services

```powershell
docker compose -f monitoring-compose.yaml up -d
```

- SonarQube: `http://localhost:9000`
- Prometheus: `http://localhost:9090`
- Alertmanager: `http://localhost:9093`

The default service configuration is for local learning only. Change credentials and storage settings before shared or production use.
