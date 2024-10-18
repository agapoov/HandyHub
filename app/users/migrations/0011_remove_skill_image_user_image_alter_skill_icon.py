# Generated by Django 4.0 on 2024-10-17 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_user_about_me'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skill',
            name='image',
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(default='static/deps/icons/No-image-found.svg', upload_to='media/users_images'),
        ),
        migrations.AlterField(
            model_name='skill',
            name='icon',
            field=models.ImageField(blank=True, default='static/deps/icons/No-image-found.svg', null=True, upload_to='static/deps/skills_images'),
        ),
    ]
