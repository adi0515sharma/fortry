# Generated by Django 3.0.8 on 2020-08-03 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HR_expenses', '0002_auto_20200803_1113'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='approved',
            field=models.BooleanField(null=True),
        ),
    ]
