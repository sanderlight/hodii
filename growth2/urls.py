"""
URL configuration for growth2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name='index'),
    
    path('generate_long_term_goal/<int:id>', views.generate_long_term_goal, name='generate_long_term_goal'),
    path('login/', views.user_login, name='login'),
    path("register/", views.register, name='register'),
    path('long_term_goal/', views.generate_long_term, name='long_term_goal'),
    path('option_selection/<int:id>/', views.generate_options, name='generate_options'),
    path('goal_display/', views.generate_long_term_goals, name='generate_long_term_goals'),
    path('year_plan/<int:id>/', views.generate_year_plan, name='generate_year_plan'),
    path('month/<int:id>/', views.generate_month_to_month_plans_view, name='generate_month_to_month_plans'),
     path('week/<int:id>', views.generate_week_to_week_plans_view, name='generate_week_to_week_plans'),
    path('daily_goals/<int:id>/', views.generate_daily_goal_view, name='daily_goals'),
    path('profile/', views.profile_view, name='profile'),
     
]
