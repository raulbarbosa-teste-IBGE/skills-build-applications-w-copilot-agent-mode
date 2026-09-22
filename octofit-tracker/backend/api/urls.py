from django.http import JsonResponse
from django.urls import path

from .models import Activity, LeaderboardEntry, Team, Workout


def api_root(request):
    return JsonResponse({
        'users': '/admin/auth/user/',
        'activities': '/api/activities/',
        'teams': '/api/teams/',
        'leaderboard': '/api/leaderboard/',
        'workouts': '/api/workouts/',
    })


def serialize(items):
    return [{'id': item.id, 'name': str(item)} for item in items]


def activities(request):
    return JsonResponse({'activities': [
        {
            'id': item.id,
            'user': item.user.username,
            'activity_type': item.activity_type,
            'duration_minutes': item.duration_minutes,
            'points': item.points,
            'recorded_at': item.recorded_at.isoformat(),
        }
        for item in Activity.objects.select_related('user')
    ]})


def teams(request):
    return JsonResponse({'teams': serialize(Team.objects.all())})


def leaderboard(request):
    return JsonResponse({'leaderboard': [
        {'rank': item.rank, 'team': item.team.name, 'points': item.points}
        for item in LeaderboardEntry.objects.select_related('team')
    ]})


def workouts(request):
    return JsonResponse({'workouts': [
        {'id': item.id, 'title': item.title, 'description': item.description,
         'level': item.level, 'focus': item.focus}
        for item in Workout.objects.all()
    ]})


urlpatterns = [
    path('', api_root, name='api-root'),
    path('activities/', activities),
    path('teams/', teams),
    path('leaderboard/', leaderboard),
    path('workouts/', workouts),
]