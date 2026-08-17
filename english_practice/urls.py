from django.urls import include, path


urlpatterns = [
    path("", include(("practice.urls", "practice"), namespace="practice")),
]
