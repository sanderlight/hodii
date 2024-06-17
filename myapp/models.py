from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Goal(models.Model):
    goal_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.goal_text


class GeneratedGoal(models.Model):
    user_response = models.ForeignKey(Goal, on_delete=models.CASCADE)
    goal_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.user.username
    
class YearlyGoal(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    year = models.PositiveIntegerField()
    title = models.CharField(max_length=100, default="Default Title" )

    

class LongTermGoal(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE,default=None)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description[:50]  #
    
    
    
class MonthlyGoal(models.Model):
    yearly_goal = models.ForeignKey(YearlyGoal, on_delete=models.CASCADE, null=True, blank=True, default=None)
  
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    month = models.PositiveIntegerField()



class WeeklyGoal(models.Model):
    monthly_goal = models.ForeignKey(MonthlyGoal, on_delete=models.CASCADE)
   
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    week = models.PositiveIntegerField()

  


class DailyGoal(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    yearly_goal = models.ForeignKey(YearlyGoal, on_delete=models.CASCADE)
    monthly_goal = models.ForeignKey(MonthlyGoal, on_delete=models.CASCADE)
    weekly_goal = models.ForeignKey(WeeklyGoal, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()