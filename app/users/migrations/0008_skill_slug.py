# Generated by Django 4.0 on 2024-10-17 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='skill',
            name='slug',
            field=models.SlugField(blank=True, max_length=256, null=True, unique=True),
        ),
    ]
