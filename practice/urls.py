from django.urls import path

from . import views


app_name = "practice"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("test/", views.test_page, name="test"),
    path("api/tests/start/", views.start_test, name="test-start"),
    path("api/tests/<str:test_id>/answer/", views.answer_test, name="test-answer"),
    path("api/tests/<str:test_id>/results/", views.test_results, name="test-results"),
    path("api/tests/<str:test_id>/retry/", views.retry_test, name="test-retry"),
]
