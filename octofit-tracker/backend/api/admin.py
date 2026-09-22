from django.contrib import admin

from .models import Activity, LeaderboardEntry, Team, Workout


admin.site.register(Activity)
admin.site.register(LeaderboardEntry)
admin.site.register(Team)
admin.site.register(Workout)