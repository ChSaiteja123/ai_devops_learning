"""
Architecture Diagram Generation using AI.

HOW IT WORKS:
-------------
1. User submits a natural-language prompt, e.g.:
   "A microservices e-commerce platform on AWS with RDS, ElastiCache, SQS, ECS Fargate"

2. We call GPT-4o asking for a structured JSON diagram definition that describes:
   - Components (services, databases, queues, load balancers, etc.)
   - Connections between them
   - AWS/GCP/Azure resource types
   - Network topology (VPCs, subnets, AZs)

3. The JSON diagram_data can be rendered in the frontend with a diagram library
   (e.g. React Flow, Mermaid, or d2lang).

4. Graceful fallback: if OpenAI is unavailable, returns a minimal skeleton diagram
   so the frontend never receives an error.

DIAGRAM DATA SCHEMA:
--------------------
{
  "nodes": [
    {"id": "lb", "type": "load_balancer", "label": "Application Load Balancer",
     "provider": "aws", "service": "alb", "tier": "ingress"}
  ],
  "edges": [
    {"from": "lb", "to": "ecs", "label": "HTTP/HTTPS", "protocol": "https"}
  ],
  "groups": [
    {"id": "vpc", "label": "VPC 10.0.0.0/16", "children": ["lb", "ecs", "rds"]}
  ],
  "metadata": {
    "cloud_provider": "aws",
    "region": "us-east-1",
    "estimated_monthly_cost_usd": 450
  }
}
"""
import json
import logging
from django.conf import settings
from .reference_architecture import ENTERPRISE_REFERENCE_ARCHITECTURE

logger = logging.getLogger(__name__)


class ArchitectureGenerator:
    """Generate cloud architecture diagrams using AI."""

    def __init__(self):
        self.model = getattr(settings, 'OPENAI_MODEL', 'gpt-4o')

    def generate(self, prompt: str, cloud_provider: str = 'aws') -> dict:
        """
        Generate an architecture diagram from a text prompt.

        Args:
            prompt: Natural language description of the architecture.
            cloud_provider: Target cloud provider (aws, gcp, azure, multi).

        Returns:
            dict with keys: diagram_data, description, cloud_provider, mermaid_diagram.
        """
        if getattr(settings, 'OPENAI_API_KEY', ''):
            try:
                return self._ai_generate(prompt, cloud_provider)
            except Exception as exc:
                logger.warning('AI architecture generation failed, using fallback: %s', exc)

        return self._fallback_diagram(prompt, cloud_provider)

    # ─────────────────────────────────────────────
    # AI generation
    # ─────────────────────────────────────────────

    def _ai_generate(self, prompt: str, cloud_provider: str) -> dict:
        import openai
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

        system_prompt = self._build_system_prompt(cloud_provider)
        user_prompt = self._build_user_prompt(prompt, cloud_provider)

        response = client.chat.completions.create(
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user',   'content': user_prompt},
            ],
            response_format={'type': 'json_object'},
            max_tokens=2000,
            temperature=0.4,
        )

        raw = response.choices[0].message.content
        data = json.loads(raw)

        # Guarantee required top-level keys exist
        diagram_data = {
            'nodes':    data.get('nodes', []),
            'edges':    data.get('edges', []),
            'groups':   data.get('groups', []),
            'metadata': data.get('metadata', {'cloud_provider': cloud_provider}),
        }

        return {
            'diagram_data':    diagram_data,
            'description':     data.get('description', f'Architecture for: {prompt}'),
            'cloud_provider':  cloud_provider,
            'mermaid_diagram': self._to_mermaid(diagram_data),
            'architecture_reference': data.get('architecture_reference', ENTERPRISE_REFERENCE_ARCHITECTURE),
        }

    def _build_system_prompt(self, cloud_provider: str) -> str:
        provider_context = {
            'aws':   'Use AWS service names (EC2, RDS, S3, ALB, ECS, Lambda, SQS, SNS, ElastiCache, CloudFront, Route53, VPC, etc.)',
            'gcp':   'Use GCP service names (GKE, Cloud SQL, Cloud Storage, Cloud Load Balancing, Pub/Sub, Cloud Run, etc.)',
            'azure': 'Use Azure service names (AKS, Azure SQL, Blob Storage, Application Gateway, Service Bus, Azure Functions, etc.)',
                    'architecture_reference': data.get('architecture_reference', ENTERPRISE_REFERENCE_ARCHITECTURE),
            'multi': 'Use generic cloud-agnostic service names and label the provider for each node.',
        }.get(cloud_provider, 'Use AWS service names.')

        return f"""You are a cloud architecture expert. Generate a structured JSON diagram definition
for a production-grade cloud architecture.

{provider_context}

Always respond with valid JSON matching this exact schema:
{{
  "description": "Brief one-paragraph description of the architecture",
  "nodes": [
    {{
      "id": "unique_snake_case_id",
      "type": "one of: load_balancer|web_server|app_server|database|cache|queue|storage|cdn|dns|firewall|gateway|function|container|kubernetes|monitoring|logging",
      "label": "Human-readable name",
      "provider": "{cloud_provider}",
      "service": "specific service name e.g. rds-postgres, elasticache-redis",
      "tier": "one of: ingress|compute|data|network|security|observability",
      "specs": {{"note": "optional sizing or config details"}}
    }}
  ],
  "edges": [
    {{
      "from": "source_node_id",
      "to": "target_node_id",
      "label": "protocol or description",
      "protocol": "https|http|tcp|grpc|amqp|jdbc|redis"
    }}
  ],
  "groups": [
    {{
      "id": "group_id",
      "label": "Group label e.g. VPC, Private Subnet",
      "children": ["node_id_1", "node_id_2"]
    }}
  ],
  "metadata": {{
    "cloud_provider": "{cloud_provider}",
    "region": "primary region",
    "high_availability": true,
    "estimated_monthly_cost_usd": 0,
    "security_notes": ["note1", "note2"],
    "scaling_notes": ["note1"]
  }}
}}

Rules:
- Every node id referenced in edges/groups must exist in nodes.
- Use realistic, production-ready designs with HA where appropriate.
- Include security considerations (WAF, security groups, private subnets).
- Keep nodes to 5-15 for clarity."""

    def _build_user_prompt(self, prompt: str, cloud_provider: str) -> str:
        return (
            f'Generate a {cloud_provider.upper()} architecture diagram for the following requirement:\n\n'
            f'{prompt}\n\n'
            f'Include appropriate security, networking, observability, AI/RAG, reliability, and disaster-recovery components.'
        )

    # ─────────────────────────────────────────────
    # Mermaid conversion (for text-based rendering)
    # ─────────────────────────────────────────────

    def _to_mermaid(self, diagram_data: dict) -> str:
        """Convert diagram_data JSON to a Mermaid flowchart string."""
        lines = ['flowchart TD']

        # Node type → Mermaid shape
        shape_map = {
            'load_balancer': ('([', '])'),
            'database':      ('[(',  ')]'),
            'cache':         ('[(',  ')]'),
            'queue':         ('[',   ']'),
            'storage':       ('[',   ']'),
            'cdn':           ('([',  '])'),
            'gateway':       ('{',   '}'),
            'function':      ('[[',  ']]'),
            'kubernetes':    ('[',   ']'),
        }

        for node in diagram_data.get('nodes', []):
            nid   = node['id']
            label = node.get('label', nid)
            service = node.get('service', '')
            display = f'{label}\\n{service}' if service else label
            open_s, close_s = shape_map.get(node.get('type', ''), ('[', ']'))
            lines.append(f'    {nid}{open_s}"{display}"{close_s}')

        for edge in diagram_data.get('edges', []):
            label = edge.get('label', '')
            arrow = f'-->|"{label}"|' if label else '-->'
            lines.append(f'    {edge["from"]} {arrow} {edge["to"]}')

        return '\n'.join(lines)

    # ─────────────────────────────────────────────
    # Fallback (no API key)
    # ─────────────────────────────────────────────

    def _fallback_diagram(self, prompt: str, cloud_provider: str) -> dict:
        """Return a minimal skeleton diagram when AI is unavailable."""
        diagram_data = {
            'nodes': [
                {'id': 'client',  'type': 'cdn',          'label': 'Client / CDN',      'provider': cloud_provider, 'service': 'cloudfront', 'tier': 'ingress'},
                {'id': 'lb',      'type': 'load_balancer', 'label': 'Load Balancer',     'provider': cloud_provider, 'service': 'alb',         'tier': 'ingress'},
                {'id': 'app',     'type': 'app_server',    'label': 'Application Layer', 'provider': cloud_provider, 'service': 'ecs-fargate', 'tier': 'compute'},
                {'id': 'db',      'type': 'database',      'label': 'Primary Database',  'provider': cloud_provider, 'service': 'rds-postgres','tier': 'data'},
                {'id': 'cache',   'type': 'cache',         'label': 'Cache Layer',       'provider': cloud_provider, 'service': 'elasticache', 'tier': 'data'},
            ],
            'edges': [
                {'from': 'client', 'to': 'lb',    'label': 'HTTPS',  'protocol': 'https'},
                {'from': 'lb',     'to': 'app',   'label': 'HTTP',   'protocol': 'http'},
                {'from': 'app',    'to': 'db',    'label': 'SQL',    'protocol': 'jdbc'},
                {'from': 'app',    'to': 'cache', 'label': 'Redis',  'protocol': 'redis'},
            ],
            'groups': [
                {'id': 'vpc', 'label': 'VPC', 'children': ['lb', 'app', 'db', 'cache']},
            ],
            'metadata': {
                'cloud_provider': cloud_provider,
                'note': 'Skeleton diagram — add OPENAI_API_KEY for AI-generated designs',
            },
        }
        return {
            'diagram_data':    diagram_data,
            'description':     f'Skeleton architecture for: {prompt}. Configure OPENAI_API_KEY for a detailed AI-generated diagram.',
            'cloud_provider':  cloud_provider,
            'mermaid_diagram': self._to_mermaid(diagram_data),
            'architecture_reference': ENTERPRISE_REFERENCE_ARCHITECTURE,
        }
