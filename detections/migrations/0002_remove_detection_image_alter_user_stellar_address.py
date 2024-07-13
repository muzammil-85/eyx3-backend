# Generated by Django 4.2.14 on 2024-07-13 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detections', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detection',
            name='image',
        ),
        migrations.AlterField(
            model_name='user',
            name='stellar_address',
            field=models.CharField(blank=True, max_length=56, null=True, unique=True),
        ),
    ]