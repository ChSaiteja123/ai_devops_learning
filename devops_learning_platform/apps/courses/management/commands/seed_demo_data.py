from django.core.management.base import BaseCommand

from apps.accounts.models import User
from apps.courses.models import Category, Course
from apps.lessons.models import Lesson
from apps.labs.models import Lab
from apps.quizzes.models import Quiz, Question, Answer
from apps.progress.models import Enrollment
from apps.projects.models import Project, ProjectSubmission
from apps.notifications.models import Notification, NotificationPreference
from apps.monitoring.models import MetricSnapshot, AlertRule, Alert, HealthCheck
from apps.courses.management.deep_dive_content import DEEP_DIVE_LESSONS
from apps.courses.platform_deep_dive_content import PLATFORM_LESSONS


class Command(BaseCommand):
    help = 'Seed demo learning data and the complete DevOps Deep Dive curriculum.'

    def handle(self, *args, **options):
        categories = self._seed_categories()
        user, admin_user = self._seed_users()
        courses = self._seed_courses(categories)
        self._seed_lessons(courses)
        self._seed_labs(courses)
        self._seed_quiz(courses['Docker Fundamentals'])
        self._seed_projects(courses, user)
        self._seed_notifications(user)
        self._seed_monitoring(admin_user)

        for course in courses.values():
            Enrollment.objects.get_or_create(user=user, course=course, defaults={'completed': False})

        self.stdout.write(self.style.SUCCESS('Demo learning data and DevOps Deep Dive curriculum created successfully.'))
        self.stdout.write('Admin login: admin / admin123')

    def _seed_categories(self):
        data = [
            ('Docker', 'Container basics and image workflows', 'fa-docker', '#60a5fa'),
            ('Kubernetes', 'Deployments, services, and cluster operations', 'fa-server', '#22d3ee'),
            ('Cloud', 'AWS, architecture, and resilience design', 'fa-cloud', '#34d399'),
            ('DevOps', 'End-to-end delivery, automation, security, and reliability', 'fa-infinity', '#f59e0b'),
        ]
        categories = {}
        for order, (name, description, icon, color) in enumerate(data, start=1):
            categories[name], _ = Category.objects.get_or_create(
                name=name,
                defaults={'description': description, 'icon': icon, 'color': color, 'order': order},
            )
        return categories

    def _seed_users(self):
        user, _ = User.objects.get_or_create(
            username='demo_user',
            defaults={'email': 'demo@example.com', 'first_name': 'Demo', 'last_name': 'User', 'skill_level': 'intermediate', 'is_active': True},
        )
        admin_user, _ = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@example.com', 'first_name': 'Platform', 'last_name': 'Admin', 'is_staff': True, 'is_superuser': True, 'is_active': True},
        )
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.set_password('admin123')
        admin_user.save()
        return user, admin_user

    def _seed_courses(self, categories):
        data = [
            ('Docker Fundamentals', 'Docker', 'beginner', 'level1', 'Learn containerization, image layers, networking, volumes, and Compose workflows.', 'Build and run containers locally with confidence.'),
            ('Kubernetes Operations', 'Kubernetes', 'intermediate', 'level2', 'Deploy workloads, troubleshoot failures, and manage cluster state in Kubernetes.', 'Understand pods, services, and rolling deployments.'),
            ('Cloud Architecture Essentials', 'Cloud', 'advanced', 'level3', 'Design scalable, secure, and observable cloud systems using AWS patterns.', 'Model resilient multi-tier cloud services.'),
            ('DevOps Deep Dive', 'DevOps', 'intermediate', 'level3', 'A complete curriculum covering Linux, Git, networking, containers, Kubernetes, infrastructure as code, CI/CD, cloud, security, observability, SRE, and incident response.', 'Move from code commit to reliable production operations.'),
        ]
        courses = {}
        for title, category_name, difficulty, level, description, short_description in data:
            courses[title], _ = Course.objects.get_or_create(
                title=title,
                defaults={
                    'category': categories[category_name], 'difficulty': difficulty, 'platform_level': level,
                    'description': description, 'short_description': short_description,
                    'what_you_learn': ['Plan reliable systems', 'Automate delivery', 'Operate production safely'],
                    'prerequisites': ['Basic programming', 'Command-line familiarity'],
                    'is_published': True, 'is_featured': title == 'DevOps Deep Dive', 'estimated_duration_hours': 12.0 if title == 'DevOps Deep Dive' else 4.5,
                },
            )
            if title == 'DevOps Deep Dive':
                courses[title].estimated_duration_hours = 21.75
                courses[title].what_you_learn = [
                    'Design and operate production DevOps systems',
                    'Build secure APIs, workers, AI, RAG, and data services',
                    'Deploy, observe, troubleshoot, and recover platform workloads',
                ]
                courses[title].save(update_fields=['estimated_duration_hours', 'what_you_learn', 'updated_at'])
        return courses

    def _seed_lessons(self, courses):
        standard_lessons = [
            ('Docker Fundamentals', 'Docker Overview', 'Learn what containers are and how they compare with virtual machines.', 'text', 1),
            ('Docker Fundamentals', 'Running Containers', 'Use docker run, build, and logs to deliver a simple application.', 'lab', 2),
            ('Kubernetes Operations', 'Pods and Deployments', 'Understand how Kubernetes schedules and manages workloads.', 'interactive', 1),
            ('Kubernetes Operations', 'Service Discovery', 'Learn how services expose pods and route traffic.', 'video', 2),
            ('Cloud Architecture Essentials', 'Designing for Availability', 'Build fault-tolerant systems with redundancy and autoscaling.', 'text', 1),
        ]
        for course_name, title, content, content_type, order in standard_lessons:
            Lesson.objects.get_or_create(course=courses[course_name], title=title, defaults={'content_type': content_type, 'content': content, 'duration_minutes': 25, 'order': order, 'is_published': True, 'objectives': ['Learn the concept', 'Apply the idea'], 'commands': []})
        for order, lesson in enumerate(DEEP_DIVE_LESSONS, start=1):
            Lesson.objects.get_or_create(
                course=courses['DevOps Deep Dive'], title=lesson['title'],
                defaults={'content_type': 'interactive' if order in {1, 4, 6, 11, 12} else 'text', 'content': lesson['content'], 'duration_minutes': 45, 'order': order, 'is_free_preview': order == 1, 'is_published': True, 'objectives': lesson['objectives'], 'commands': lesson['commands']},
            )
        for order, lesson in enumerate(PLATFORM_LESSONS, start=13):
            Lesson.objects.get_or_create(
                course=courses['DevOps Deep Dive'], title=lesson['title'],
                defaults={'content_type': 'interactive', 'content': lesson['content'], 'duration_minutes': 45, 'order': order, 'is_published': True, 'objectives': lesson['objectives'], 'commands': lesson['commands']},
            )

    def _seed_labs(self, courses):
        data = [
            ('Docker Fundamentals', 'Build a Docker image', 'docker', 'docker build -t demo-app .'),
            ('Kubernetes Operations', 'Deploy a sample workload', 'kubernetes', 'kubectl apply -f deployment.yaml'),
            ('Cloud Architecture Essentials', 'Design a resilient AWS app', 'aws', 'aws architecture diagram'),
        ]
        for course_name, title, technology, command in data:
            Lab.objects.get_or_create(title=title, defaults={'course': courses[course_name], 'technology': technology, 'difficulty': 'beginner' if technology == 'docker' else 'intermediate', 'objective': 'Practice the core workflow for this learning module.', 'prerequisites': ['Read the lesson notes'], 'estimated_minutes': 30, 'steps': [{'step_number': 1, 'title': 'Setup', 'description': 'Review the task', 'command': command, 'expected_output': 'Success'}], 'common_errors': [{'error': 'Wrong command', 'cause': 'Not following the lesson', 'fix': 'Repeat the setup steps'}], 'interview_questions': ['What problem does this solve?'], 'is_published': True, 'order': 1})

    def _seed_quiz(self, course):
        quiz, _ = Quiz.objects.get_or_create(title='Docker Basics Quiz', course=course, defaults={'description': 'Quick check on Docker fundamentals.', 'passing_score': 70, 'is_published': True})
        questions = [('What does Docker use to package an application?', 'A container image', 'A VM snapshot'), ('What command shows running containers?', 'docker ps', 'docker list')]
        for text, correct, incorrect in questions:
            question, _ = Question.objects.get_or_create(quiz=quiz, text=text, defaults={'question_type': 'mcq', 'explanation': f'The correct answer is {correct}.'})
            Answer.objects.get_or_create(question=question, text=correct, is_correct=True)
            Answer.objects.get_or_create(question=question, text=incorrect, is_correct=False)

    def _seed_projects(self, courses, user):
        data = [(1, 'Containerized Django API', 'docker', courses['Docker Fundamentals']), (2, 'Kubernetes Rolling Deployment', 'kubernetes', courses['Kubernetes Operations']), (3, 'Highly Available Cloud Platform', 'aws', courses['Cloud Architecture Essentials'])]
        for number, title, technology, course in data:
            project, _ = Project.objects.get_or_create(number=number, defaults={'title': title, 'tech_stack': technology, 'description': 'Build and operate a production-style DevOps system.', 'objectives': ['Plan the implementation', 'Document operational decisions'], 'steps': [{'step_number': 1, 'title': 'Plan', 'description': 'Create the design and delivery checklist.'}], 'architecture_diagram': 'flowchart LR\n Client --> API\n API --> Data', 'estimated_hours': 6.0, 'course': course, 'is_published': True})
            ProjectSubmission.objects.get_or_create(project=project, user=user, defaults={'github_url': 'https://github.com/example/devops-learning-project', 'notes': 'Demo submission for admin review.'})

    def _seed_notifications(self, user):
        NotificationPreference.objects.get_or_create(user=user)
        data = [('achievement', 'high', 'Docker course started', 'Your learning path is underway.'), ('deployment', 'normal', 'Demo deployment succeeded', 'The sample platform deployment completed successfully.'), ('alert', 'critical', 'API latency needs attention', 'The demo API latency alert is currently firing.')]
        for notification_type, priority, title, message in data:
            Notification.objects.get_or_create(recipient=user, title=title, defaults={'notification_type': notification_type, 'priority': priority, 'message': message, 'action_url': '/dashboard/', 'action_label': 'Open dashboard'})

    def _seed_monitoring(self, admin_user):
        rule, _ = AlertRule.objects.get_or_create(name='Learning API high latency', defaults={'description': 'Warn when learning API p99 latency exceeds the service objective.', 'service_name': 'learning-api', 'metric': 'latency_p99_ms', 'operator': 'gt', 'threshold': 500.0, 'severity': 'warning', 'is_active': True, 'created_by': admin_user})
        MetricSnapshot.objects.get_or_create(service_name='learning-api', namespace='dev', cpu_percent=42.5, memory_percent=61.0, defaults={'source': 'prometheus', 'request_rate': 18.4, 'error_rate': 0.012, 'latency_p50_ms': 82.0, 'latency_p99_ms': 642.0, 'pod_count': 3, 'pod_restarts': 1, 'raw_metrics': {'environment': 'demo', 'region': 'local'}})
        Alert.objects.get_or_create(rule=rule, service_name='learning-api', status='firing', defaults={'severity': 'warning', 'message': 'P99 latency is above the 500 ms threshold.', 'metric_value': 642.0, 'labels': {'namespace': 'dev', 'team': 'platform'}, 'annotations': {'runbook': 'Review API dependency latency and recent deployments.'}})
        HealthCheck.objects.get_or_create(service_name='learning-api', endpoint='https://example.com/health/', defaults={'status': 'healthy', 'response_time_ms': 84.0, 'status_code': 200})
