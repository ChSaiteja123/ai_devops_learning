DEVOPS NOTES
================================================================================

COLORED BROWSER VERSION
--------------------------------------------------------------------------------
Open `../devops_notes_html/index.html` in a browser for colored headings,
styled command blocks, highlighted callouts, and improved spacing. The `.txt`
files remain the portable plain-text source documents.

PURPOSE / OVERVIEW
--------------------------------------------------------------------------------
These notes are structured plain-text learning documents for studying DevOps,
cloud infrastructure, delivery automation, and operational reliability.

FORMATTING LEGEND
--------------------------------------------------------------------------------

TITLE
The first line identifies the subject. The line of equals signs separates the
title from the document body.

PURPOSE / OVERVIEW
This opening paragraph gives the main context and explains why the subject
matters.

NUMBERED SECTION HEADINGS
Numbered headings divide the document into a readable learning sequence. A line
of hyphens under each heading makes sections easy to scan in a terminal or text
editor.

COMMANDS
This heading marks shell commands, command examples, and task-oriented command
lists. Read the command, identify its target, and then explain its effect before
running it.

EXAMPLE
This heading marks configuration, pipeline, YAML, or other implementation
examples. Treat examples as patterns to understand, not as production defaults.

CALLOUTS
[IMPORTANT] Marks a concept or practice that should be remembered.
[SECURITY] Marks identity, secrets, access, vulnerability, or data-protection
guidance.
[WARNING] Marks a risk, failure mode, or action requiring extra care.
[PRODUCTION] Marks guidance that matters when operating real workloads.
[EXAMPLE] Marks a concrete example or scenario.

HOW TO STUDY THE NOTES
--------------------------------------------------------------------------------

1. Read the PURPOSE / OVERVIEW section before taking notes.
2. Read each numbered section in order and write a one-sentence summary.
3. Convert important vocabulary into flashcards.
4. For COMMANDS sections, explain each command and its expected result.
5. For EXAMPLE sections, identify inputs, outputs, dependencies, and risks.
6. Recreate small examples in a disposable lab environment.
7. Review [SECURITY] and [PRODUCTION] callouts before using a pattern at work.
8. After practice, explain the complete workflow without looking at the notes.

RECOMMENDED STUDY ORDER
--------------------------------------------------------------------------------

1. Introduction to DevOps
2. Linux fundamentals
3. Shell scripting
4. Git and GitHub
5. CI/CD
6. Docker
7. Kubernetes
8. Terraform
9. Ansible
10. Cloud computing
11. AWS core services
12. EC2 and security groups
13. S3, IAM, and CloudWatch
14. RDS, ElastiCache, and DynamoDB
15. VPC and networking
16. Route 53 and load balancing
17. Monitoring and observability
18. Jenkins, Gradle, SonarQube, Trivy, and Alertmanager

REVIEW CHECKLIST
--------------------------------------------------------------------------------

- Can you describe the purpose of the technology in plain language?
- Can you identify its inputs, outputs, dependencies, and failure modes?
- Can you explain the security boundary and least-privilege requirements?
- Can you run or adapt the included commands in a safe environment?
- Can you connect the topic to version control, automation, and monitoring?
- Can you name the operational signal that shows the workflow is healthy?

Use the notes as a reference during practice, then return to the callouts and
examples during review. The goal is understanding the decisions behind each
tool, not memorizing isolated commands.