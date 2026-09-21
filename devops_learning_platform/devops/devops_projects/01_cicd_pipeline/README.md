# CI/CD Pipeline with Jenkins

This project demonstrates a Jenkins declarative pipeline for a Python application. A GitHub Actions workflow is also included as an alternative.

Pipeline stages:
1. Check out source code
2. Install Python
3. Install dependencies
4. Run tests
5. Build a distributable artifact

The Jenkins pipeline is stored in `Jenkinsfile`. It creates an isolated Python virtual environment, installs `requirements-dev.txt`, runs the tests, and publishes a JUnit test report.

## Jenkins setup

1. Install Jenkins with the Pipeline and Git plugins.
2. Ensure the Jenkins agent has `python3`, `python3-venv`, and Git installed.
3. Create a Pipeline job.
4. Select **Pipeline script from SCM**.
5. Select Git, enter the repository URL, and set the script path to `devops/devops_projects/01_cicd_pipeline/Jenkinsfile` when this folder is inside the larger learning repository.
6. Build the job.

For a repository containing only this project, use `Jenkinsfile` as the script path.

The Jenkins pipeline expects a Linux agent because it uses POSIX commands and the `python3` executable.

## GitHub Actions alternative

The equivalent GitHub Actions workflow is stored in `.github/workflows/ci.yml`.

