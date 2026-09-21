"""
Root URL Configuration.

WHAT ARE URLS?
--------------
URL patterns map incoming HTTP requests to Django views.
When a browser visits /api/v1/courses/, Django walks this list
top-to-bottom and calls the first matching view.

URL STRUCTURE FOR THIS PROJECT:
--------------------------------
/                         → Learning dashboard (HTML)
/admin/                   → Django admin interface
/accounts/                → Login, register, profile HTML pages
/api/v1/accounts/         → Authentication REST API
/api/v1/courses/          → Courses REST API
/api/v1/lessons/          → Lessons REST API
/api/v1/labs/             → Labs REST API
/api/v1/projects/         → Projects REST API
/api/v1/architecture/     → Architecture generator API
/api/v1/quizzes/          → Quiz system API
/api/v1/progress/         → Learning progress API
/api/v1/ai/               → AI assistant API
/api/v1/rag/              → RAG document & query API
/api/v1/aiops/            → AIOps incident analysis API
/api/v1/monitoring/       → Metrics & observability API
/api/v1/deployments/      → Deployment tracking API
/api/v1/notifications/    → User notifications API
/api/v1/audit/            → Audit log API
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.views.generic import TemplateView
from apps.courses.web_views import course_detail, lesson_detail, lesson_section


# Customize admin site
admin.site.site_header = '🚀 DevOps Learning Platform'
admin.site.site_title = 'DevOps Platform Admin'
admin.site.index_title = 'Platform Administration'

urlpatterns = [
    # ─── Admin ────────────────────────────────────────
    path('admin/', admin.site.urls),

    # ─── Frontend HTML views ───────────────────────────
    path('', TemplateView.as_view(template_name='dashboard/index.html'), name='home'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard/index.html'), name='dashboard'),
    path('accounts/', include('apps.accounts.auth_urls')),
    path('courses/', TemplateView.as_view(template_name='courses/list.html'), name='courses'),
    path('courses/<slug:slug>/', course_detail, name='web-course-detail'),
    path('courses/<slug:slug>/lessons/<int:order>/', lesson_detail, name='web-lesson-detail'),
    path('courses/<slug:slug>/lessons/<int:order>/<slug:section>/', lesson_section, name='web-lesson-section'),
    path('ai-chat/', TemplateView.as_view(template_name='ai_assistant/chat.html'), name='ai-chat'),
    path('architecture/', TemplateView.as_view(template_name='architecture/generator.html'), name='architecture'),

    # ─── REST API v1 ──────────────────────────────────
    path('api/v1/accounts/', include('apps.accounts.urls')),
    path('api/v1/courses/', include('apps.courses.urls')),
    path('api/v1/lessons/', include('apps.lessons.urls')),
    path('api/v1/labs/', include('apps.labs.urls')),
    path('api/v1/projects/', include('apps.projects.urls')),
    path('api/v1/architecture/', include('apps.architecture.urls')),
    path('api/v1/quizzes/', include('apps.quizzes.urls')),
    path('api/v1/progress/', include('apps.progress.urls')),
    path('api/v1/ai/', include('apps.ai_assistant.urls')),
    path('api/v1/rag/', include('apps.rag.urls')),
    path('api/v1/aiops/', include('apps.aiops.urls')),
    path('api/v1/monitoring/', include('apps.monitoring.urls')),
    path('api/v1/deployments/', include('apps.deployments.urls')),
    path('api/v1/notifications/', include('apps.notifications.urls')),
    path('api/v1/audit/', include('apps.audit.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Debug toolbar (development only — package only installed in development.txt)
if settings.DEBUG:
    urlpatterns += [path('library/<path:path>', serve, {'document_root': settings.BASE_DIR / 'devops'})]
    try:
        import debug_toolbar
        urlpatterns = [path('__debug__/', include(debug_toolbar.urls))] + urlpatterns
    except ImportError:
        pass  # debug_toolbar not installed (e.g. production image)
