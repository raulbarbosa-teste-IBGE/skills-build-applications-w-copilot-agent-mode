from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils import timezone

from api.models import Activity, LeaderboardEntry, Team, Workout


class Command(BaseCommand):
    help = 'Create the sample Octofit Tracker data using the Django ORM.'

    def handle(self, *args, **options):
        team_data = [
            ('Trailblazers', 'Every step counts.'),
            ('Power Paws', 'Strong together.'),
        ]
        teams = {name: Team.objects.update_or_create(name=name, defaults={'motto': motto})[0]
                 for name, motto in team_data}

        users = []
        for username, first_name, team_name in (
            ('alex', 'Alex', 'Trailblazers'),
            ('jamie', 'Jamie', 'Trailblazers'),
            ('riley', 'Riley', 'Power Paws'),
            ('sam', 'Sam', 'Power Paws'),
        ):
            user, _ = User.objects.update_or_create(
                username=username,
                defaults={'first_name': first_name, 'email': f'{username}@octofit.example'},
            )
            users.append(user)

        now = timezone.now()
        activity_data = [
            (users[0], 'running', 30, 60),
            (users[1], 'walking', 45, 45),
            (users[2], 'strength', 40, 80),
            (users[3], 'running', 25, 50),
        ]
        for index, (user, activity_type, duration, points) in enumerate(activity_data):
            activity = Activity.objects.filter(
                user=user, activity_type=activity_type
            ).order_by('id').first()
            defaults = {
                'duration_minutes': duration,
                'points': points,
                'recorded_at': now - timedelta(days=index),
            }
            if activity is None:
                Activity.objects.create(user=user, activity_type=activity_type, **defaults)
            else:
                for field, value in defaults.items():
                    setattr(activity, field, value)
                activity.save(update_fields=(*defaults.keys(),))
                Activity.objects.filter(
                    user=user, activity_type=activity_type
                ).exclude(pk=activity.pk).delete()

        team_points = {'Trailblazers': 105, 'Power Paws': 130}
        for rank, (team_name, points) in enumerate(
            sorted(team_points.items(), key=lambda item: item[1], reverse=True), start=1
        ):
            LeaderboardEntry.objects.update_or_create(
                team=teams[team_name], defaults={'points': points, 'rank': rank}
            )

        workout_data = [
            ('Starter Run', 'A steady run with a gentle warm-up and cool-down.', 'beginner', 'cardio'),
            ('Full Body Circuit', 'Three rounds of squats, push-ups, lunges, and planks.', 'intermediate', 'strength'),
            ('Mobility Reset', 'A short mobility routine for hips, shoulders, and ankles.', 'beginner', 'mobility'),
        ]
        for title, description, level, focus in workout_data:
            Workout.objects.update_or_create(
                title=title,
                defaults={'description': description, 'level': level, 'focus': focus},
            )

        self.stdout.write(self.style.SUCCESS('Octofit Tracker database populated successfully.'))