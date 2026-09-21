"""
AIOps Analysis Service.

WHAT IS AIOPS?
--------------
AIOps applies AI/ML to IT operations. Instead of engineers manually
diagnosing every alert, AI analyzes patterns across:
  - Metrics (CPU, memory, error rates)
  - Logs (application errors, stack traces)
  - Traces (slow requests, bottlenecks)
  - Kubernetes events (pod restarts, OOMKilled)
  - Recent deployments (did something just change?)

SAFETY RULE: NEVER auto-remediate without human approval.
The AI suggests — humans decide.

FLOW:
-----
Alert fires → POST /api/v1/aiops/analyze/ → AI analyzes → Returns:
  {root_cause, evidence, impact, recommendation, confidence, remediation}
    → Human reviews → Approves → Optional remediation
"""
import logging
from django.conf import settings
from .models import Incident

logger = logging.getLogger(__name__)


class AIOpsAnalyzer:
    """Core AIOps analysis engine."""

    def analyze(self, metrics: dict, logs: list = None, context: dict = None) -> dict:
        """
        Analyze metrics + logs to determine root cause.

        Args:
            metrics: Dict of current metric values
                     e.g. {"cpu_percent": 95, "memory_percent": 78, "error_rate": 0.05}
            logs: Optional list of recent log lines
            context: Optional extra context (recent deployments, k8s events)

        Returns: Analysis dict with root_cause, evidence, recommendation, etc.
        """
        logs = logs or []
        context = context or {}

        # Try AI analysis first, fall back to rule-based
        try:
            if getattr(settings, 'OPENAI_API_KEY', ''):
                return self._ai_analysis(metrics, logs, context)
        except Exception as exc:
            logger.warning('AI analysis failed, using rule-based: %s', exc)

        return self._rule_based_analysis(metrics, logs, context)

    def _ai_analysis(self, metrics: dict, logs: list, context: dict) -> dict:
        import openai
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

        prompt = self._build_prompt(metrics, logs, context)
        response = client.chat.completions.create(
            model='gpt-4o',
            messages=[
                {
                    'role': 'system',
                    'content': (
                        'You are an expert SRE (Site Reliability Engineer) analyzing production incidents. '
                        'Respond with structured JSON only. Never suggest automatic destructive actions.'
                    ),
                },
                {'role': 'user', 'content': prompt},
            ],
            response_format={'type': 'json_object'},
            max_tokens=1000,
            temperature=0.2,
        )
        import json
        result = json.loads(response.choices[0].message.content)
        result['analysis_method'] = 'ai'
        return result

    def _build_prompt(self, metrics: dict, logs: list, context: dict) -> str:
        log_sample = '\n'.join(logs[:20]) if logs else 'No logs provided'
        return f"""Analyze this production incident and respond with JSON:

METRICS:
{metrics}

RECENT LOGS (last 20 lines):
{log_sample}

CONTEXT:
{context}

Respond with this exact JSON structure:
{{
  "root_cause": "One sentence root cause",
  "severity": "critical|high|medium|low",
  "evidence": ["evidence point 1", "evidence point 2", "evidence point 3"],
  "impact": "What is affected and how many users",
  "recommendation": "Step-by-step recommended actions",
  "confidence": 0.0-1.0,
  "suggested_remediation": "Safe remediation command or action (never destructive)",
  "requires_human_approval": true
}}"""

    def _rule_based_analysis(self, metrics: dict, logs: list, context: dict) -> dict:
        """Fallback rule-based analysis when AI is unavailable."""
        cpu = metrics.get('cpu_percent', 0)
        memory = metrics.get('memory_percent', 0)
        error_rate = metrics.get('error_rate', 0)
        pod_restarts = metrics.get('pod_restarts', 0)

        issues = []
        evidence = []
        recommendations = []

        if cpu > 90:
            issues.append('High CPU utilization')
            evidence.append(f'CPU at {cpu}% (threshold: 90%)')
            recommendations.append('Scale horizontally: kubectl scale deployment <name> --replicas=<n>')

        if memory > 85:
            issues.append('High memory utilization')
            evidence.append(f'Memory at {memory}% (threshold: 85%)')
            recommendations.append('Check for memory leaks. Consider increasing resource limits.')

        if error_rate > 0.05:
            issues.append('Elevated error rate')
            evidence.append(f'Error rate at {error_rate*100:.1f}% (threshold: 5%)')
            recommendations.append('Check application logs for stack traces. Review recent deployments.')

        if pod_restarts > 5:
            issues.append('Pod crash loop detected')
            evidence.append(f'{pod_restarts} pod restarts in last hour')
            recommendations.append('kubectl describe pod <name> to check OOMKilled or CrashLoopBackOff')

        # Determine severity
        if cpu > 95 or memory > 95 or error_rate > 0.2:
            severity = 'critical'
            confidence = 0.9
        elif issues:
            severity = 'high'
            confidence = 0.75
        else:
            severity = 'low'
            confidence = 0.5
            issues = ['No significant issues detected']
            evidence = [f'CPU: {cpu}%, Memory: {memory}%, Error rate: {error_rate*100:.1f}%']
            recommendations = ['Continue monitoring. All metrics within normal ranges.']

        return {
            'root_cause': ' | '.join(issues) if issues else 'System within normal parameters',
            'severity': severity,
            'evidence': evidence,
            'impact': f'Affects service performance. {len(issues)} issue(s) detected.',
            'recommendation': '\n'.join(f'{i+1}. {r}' for i, r in enumerate(recommendations)),
            'confidence': confidence,
            'suggested_remediation': recommendations[0] if recommendations else '',
            'requires_human_approval': True,
            'analysis_method': 'rule_based',
        }
