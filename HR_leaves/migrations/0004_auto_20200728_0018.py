# Generated by Django 3.0.8 on 2020-07-27 18:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HR_user_profiles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('HR_leaves', '0003_leaveapplication_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaveapplication',
            name='approved',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='assign',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='HR_user_profiles.Profile', verbose_name='Assign work to'),
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Leave',
        ),
    ]
