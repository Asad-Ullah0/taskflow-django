import json

from django.contrib.auth.decorators import login_required
from django.db.models import Case, F, IntegerField, Q, When
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from .models import Task


def serialize(t):
    today = timezone.localdate()
    return {
        "id": t.id,
        "title": t.title,
        "description": t.description,
        "priority": t.priority,
        "status": t.status,
        "due_date": t.due_date.isoformat() if t.due_date else None,
        "overdue": bool(t.due_date and t.due_date < today and t.status != "done"),
    }


def stats_for(user):
    qs = Task.objects.filter(user=user)
    total = qs.count()
    done = qs.filter(status="done").count()
    return {
        "total": total,
        "todo": qs.filter(status="todo").count(),
        "doing": qs.filter(status="doing").count(),
        "done": done,
        "percent": round(done * 100 / total) if total else 0,
    }


def _body(request):
    try:
        return json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return {}


def _apply(task, data):
    errors = {}
    if "title" in data:
        title = (data["title"] or "").strip()
        if not title:
            errors["title"] = "Title is required."
        else:
            task.title = title[:200]
    if "description" in data:
        task.description = (data["description"] or "").strip()
    if data.get("priority") in Task.Priority.values:
        task.priority = data["priority"]
    if data.get("status") in Task.Status.values:
        task.status = data["status"]
    if "due_date" in data:
        task.due_date = parse_date(data["due_date"]) if data["due_date"] else None
    return errors


@login_required
@ensure_csrf_cookie
def dashboard(request):
    return render(request, "dashboard.html")


@login_required
@require_http_methods(["GET", "POST"])
def task_list(request):
    if request.method == "POST":
        data = _body(request)
        task = Task(user=request.user)
        errors = _apply(task, data)
        if "title" not in data:
            errors["title"] = "Title is required."
        if errors:
            return JsonResponse({"errors": errors}, status=400)
        task.save()
        return JsonResponse(
            {"task": serialize(task), "stats": stats_for(request.user)}, status=201
        )

    qs = Task.objects.filter(user=request.user)
    if request.GET.get("status") in Task.Status.values:
        qs = qs.filter(status=request.GET["status"])
    if request.GET.get("priority") in Task.Priority.values:
        qs = qs.filter(priority=request.GET["priority"])
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

    sort = request.GET.get("sort", "new")
    if sort == "due":
        qs = qs.order_by(F("due_date").asc(nulls_last=True), "-created_at")
    elif sort == "priority":
        qs = qs.annotate(
            rank=Case(
                When(priority="high", then=0),
                When(priority="medium", then=1),
                default=2,
                output_field=IntegerField(),
            )
        ).order_by("rank", "-created_at")

    return JsonResponse(
        {"tasks": [serialize(t) for t in qs], "stats": stats_for(request.user)}
    )


@login_required
@require_http_methods(["PATCH", "DELETE"])
def task_detail(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == "DELETE":
        task.delete()
        return JsonResponse({"ok": True, "stats": stats_for(request.user)})
    errors = _apply(task, _body(request))
    if errors:
        return JsonResponse({"errors": errors}, status=400)
    task.save()
    return JsonResponse({"task": serialize(task), "stats": stats_for(request.user)})
