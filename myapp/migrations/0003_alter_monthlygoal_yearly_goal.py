# Generated by Django 4.2.4 on 2024-06-05 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0002_yearlygoal_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="monthlygoal",
            name="yearly_goal",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="myapp.yearlygoal",
            ),
        ),
    ]
