# Generated by Django 4.2.4 on 2024-06-06 01:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0003_alter_monthlygoal_yearly_goal"),
    ]

    operations = [
        migrations.AlterField(
            model_name="longtermgoal",
            name="profile",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="myapp.profile",
            ),
        ),
        migrations.AlterField(
            model_name="monthlygoal",
            name="yearly_goal",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="myapp.yearlygoal",
            ),
        ),
    ]
