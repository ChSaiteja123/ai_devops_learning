"""
AI Assistant Service.

ARCHITECTURE:
-------------
User → Django API → AIAssistantService → OpenAI GPT-4o → Response
                          ↓
                  Conversation stored in PostgreSQL

WHAT IS A SYSTEM PROMPT?
--------------------------
The system prompt tells the LLM who it is and what it should do.
We set it to be an expert DevOps tutor so responses are focused
on technical education rather than general topics.

HOW IT WORKS:
-------------
1. User sends message via POST /api/v1/ai/chat/
2. Django retrieves conversation history from DB
3. Builds messages array: [system, ...history, new_user_msg]
4. Calls OpenAI chat.completions.create()
5. Stores both user message and assistant response
6. Returns assistant response
"""
import logging
from django.conf import settings
from .models import Conversation, Message

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an expert AI-powered DevOps and Cloud Architecture tutor for a learning platform.

Your expertise covers:
🐧 Linux & Shell Scripting
🔀 Git & GitHub
🐳 Docker & Containers
☸️  Kubernetes & Helm
☁️  AWS Cloud (EC2, EKS, RDS, S3, IAM, ALB, ECR, VPC)
🏗️  Terraform Infrastructure as Code
🔄 CI/CD (Jenkins, GitHub Actions)
🔒 DevSecOps (SonarQube, Trivy, RBAC, Network Policies)
📊 Monitoring (Prometheus, Grafana, Loki, OpenTelemetry)
🤖 AI Engineering (LLMs, Embeddings, RAG, Vector Databases)
🚨 AIOps (Incident Analysis, Root Cause Analysis)
🐍 Python & Django REST Framework

Teaching style:
- Use simple analogies for complex concepts
- Provide real-world examples
- Include CLI commands with explanations
- Show before/after comparisons
- Mention common mistakes and how to avoid them
- Reference what level (Beginner/Intermediate/Advanced) concepts belong to
- Use emojis to make explanations engaging
- Always explain WHY, not just HOW
"""


class AIAssistantService:
    def __init__(self):
        self.model = getattr(settings, 'OPENAI_MODEL', 'gpt-4o')
        self.api_key = getattr(settings, 'OPENAI_API_KEY', '')

    def chat(self, conversation: Conversation, user_message: str) -> str:
        """Send user message to LLM, store both messages, return reply."""
        # Build message history
        history = []
        messages = conversation.messages.all().order_by('created_at')
        recent_messages = list(messages)[-20:] if messages.exists() else []
        for msg in recent_messages:
            history.append({'role': msg.role, 'content': msg.content})

        messages = [{'role': 'system', 'content': SYSTEM_PROMPT}] + history + [
            {'role': 'user', 'content': user_message}
        ]

        # Store user message first
        Message.objects.create(
            conversation=conversation,
            role='user',
            content=user_message,
        )

        try:
            reply = self._call_openai(messages)
        except Exception as exc:
            logger.warning('OpenAI call failed: %s — using fallback', exc)
            reply = self._fallback_response(user_message)

        # Store assistant reply
        Message.objects.create(
            conversation=conversation,
            role='assistant',
            content=reply,
        )

        # Update conversation title from first message
        if not conversation.title and user_message:
            conversation.title = user_message[:80]
            conversation.save(update_fields=['title', 'updated_at'])

        return reply

    def _call_openai(self, messages: list) -> str:
        """Call OpenAI API. Requires OPENAI_API_KEY in settings."""
        import openai
        client = openai.OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=1500,
            temperature=0.7,
        )
        return response.choices[0].message.content

    def _fallback_response(self, user_message: str) -> str:
        """Fallback when OpenAI is not configured — returns educational content."""
        msg = user_message.lower()
        if 'docker' in msg:
            return (
                "🐳 **Docker** is a container platform that packages your application "
                "and all its dependencies into a portable container.\n\n"
                "**Key commands:**\n"
                "```bash\n"
                "docker build -t myapp .        # Build image from Dockerfile\n"
                "docker run -p 8000:8000 myapp  # Run container\n"
                "docker ps                       # List running containers\n"
                "docker logs <container_id>      # View logs\n"
                "```\n\n"
                "**Why Docker?** 'It works on my machine' is no longer an excuse. "
                "Containers run identically everywhere: laptop, CI, production.\n\n"
                "*(Configure OPENAI_API_KEY for full AI responses)*"
            )
        if 'kubernetes' in msg or 'k8s' in msg:
            return (
                "☸️ **Kubernetes** orchestrates containers across a cluster of machines.\n\n"
                "**Core objects:**\n"
                "- **Pod** — smallest deployable unit (one or more containers)\n"
                "- **Deployment** — manages desired state and rolling updates\n"
                "- **Service** — stable network endpoint for pods\n"
                "- **Ingress** — routes external HTTP traffic to services\n\n"
                "```bash\n"
                "kubectl get pods              # List pods\n"
                "kubectl describe pod <name>   # Debug a pod\n"
                "kubectl logs <pod>            # View logs\n"
                "kubectl apply -f deploy.yaml  # Apply manifest\n"
                "```\n\n"
                "*(Configure OPENAI_API_KEY for full AI responses)*"
            )
        return (
            "👋 I'm your DevOps & Cloud Architecture AI tutor!\n\n"
            "I can help you learn:\n"
            "🐳 Docker | ☸️ Kubernetes | ☁️ AWS | 🏗️ Terraform | "
            "🔄 CI/CD | 🔒 DevSecOps | 📊 Monitoring | 🤖 AI Engineering\n\n"
            "Ask me anything like:\n"
            "- *'Explain Kubernetes pods vs deployments'*\n"
            "- *'How do I set up a Jenkins CI pipeline?'*\n"
            "- *'What is a RAG system and how does it work?'*\n\n"
            "*(Configure OPENAI_API_KEY in .env for full AI responses)*"
        )
