from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.views.generic import TemplateView

from accounts import views as accounts_views
from tasks import views as task_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    # accounts
    path("login/", accounts_views.login_view, name="login"),
    path("register/", accounts_views.register_view, name="register"),
    path("logout/", LogoutView.as_view(), name="logout"),
    # tasks
    path("dashboard/", task_views.dashboard, name="dashboard"),
    path("api/tasks/", task_views.task_list, name="api_tasks"),
    path("api/tasks/<int:pk>/", task_views.task_detail, name="api_task"),
]
