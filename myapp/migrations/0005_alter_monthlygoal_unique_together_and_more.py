# Generated by Django 4.2.4 on 2024-06-06 15:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0004_alter_longtermgoal_profile_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="monthlygoal",
            unique_together={("yearly_goal", "month")},
        ),
        migrations.AlterUniqueTogether(
            name="weeklygoal",
            unique_together={("monthly_goal", "week")},
        ),
        migrations.AlterUniqueTogether(
            name="yearlygoal",
            unique_together={("profile", "year")},
        ),
    ]
