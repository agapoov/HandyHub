# Generated by Django 4.0 on 2024-10-18 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_skill_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='static/deps/default_images/default_logo.jpg', upload_to='media/users_images'),
        ),
    ]