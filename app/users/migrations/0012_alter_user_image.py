# Generated by Django 4.0 on 2024-10-17 11:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_remove_skill_image_user_image_alter_skill_icon'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='static/deps/icons/default_image.webp', upload_to='media/users_images'),
        ),
    ]
