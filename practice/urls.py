from django.urls import path

from . import course_views, views


app_name = "practice"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("daily-challenge/", views.daily_challenge, name="daily-challenge"),
    path("courses/", course_views.course_list, name="courses"),
    path("courses/<slug:course_slug>/", course_views.course_detail, name="course-detail"),
    path("courses/<slug:course_slug>/<slug:lesson_slug>/", course_views.course_lesson, name="course-lesson"),
    path("test/", views.test_page, name="test"),
    path("robots.txt", views.robots_txt, name="robots-txt"),
    path("sitemap.xml", views.sitemap_xml, name="sitemap-xml"),
    path(".well-known/api-catalog", views.api_catalog, name="api-catalog"),
    path(".well-known/oauth-protected-resource", views.oauth_protected_resource, name="oauth-protected-resource"),
    path(".well-known/oauth-authorization-server", views.oauth_authorization_server, name="oauth-authorization-server"),
    path(".well-known/openid-configuration", views.openid_configuration, name="openid-configuration"),
    path(".well-known/jwks.json", views.jwks_json, name="jwks-json"),
    path(".well-known/mcp/server-card.json", views.mcp_server_card, name="mcp-server-card"),
    path(".well-known/mcp/server-cards.json", views.mcp_server_card, name="mcp-server-cards"),
    path(".well-known/agent-skills/index.json", views.agent_skills_index, name="agent-skills-index"),
    path(".well-known/skills/index.json", views.agent_skills_index, name="skills-index"),
    path(".well-known/agent-skills/english-practice/SKILL.md", views.agent_skill_file, name="agent-skill-file"),
    path(".well-known/ai-catalog.json", views.ai_catalog, name="ai-catalog"),
    path("auth.md", views.auth_md, name="auth-md"),
    path("llms.txt", views.llms_txt, name="llms-txt"),
    path("api/tests/start/", views.start_test, name="test-start"),
    path("api/tests/<str:test_id>/answer/", views.answer_test, name="test-answer"),
    path("api/tests/<str:test_id>/results/", views.test_results, name="test-results"),
    path("api/tests/<str:test_id>/retry/", views.retry_test, name="test-retry"),
    path("api/vocabulary/sample/", views.vocabulary_sample, name="vocabulary-sample"),
    path("api/vocabulary/lookup/", views.vocabulary_lookup, name="vocabulary-lookup"),
]
