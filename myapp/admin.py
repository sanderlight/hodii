from django.contrib import admin
from .models import Profile, LongTermGoal, YearlyGoal, MonthlyGoal, WeeklyGoal, DailyGoal, Goal

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(LongTermGoal)
class LongTermGoalAdmin(admin.ModelAdmin):
    pass

@admin.register(YearlyGoal)
class YearlyGoalAdmin(admin.ModelAdmin):
    pass

@admin.register(MonthlyGoal)
class MonthlyGoalAdmin(admin.ModelAdmin):
    pass

@admin.register(WeeklyGoal)
class WeeklyGoalAdmin(admin.ModelAdmin):
    pass

@admin.register(DailyGoal)
class DailyGoalAdmin(admin.ModelAdmin):
    pass


@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    pass



