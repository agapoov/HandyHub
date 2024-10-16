from django.contrib.auth.models import AbstractUser
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=128)
    icon = models.ImageField(upload_to='static/deps/skills_images', blank=True, null=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLE_CHOICES = (
        ('worker', 'Рабочий'),
        ('employer', 'Работодатель')
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='worker')
    surname = models.CharField(max_length=128)
    phone = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    balance = models.FloatField(default=0.0)
    points = models.IntegerField(default=0)
    rating = models.FloatField(default=0.0)
    is_free = models.BooleanField(default=False)
    skills = models.ManyToManyField(Skill, blank=True, related_name='users')

    def get_role_display(self):
        return dict(self.ROLE_CHOICES).get(self.role, self.role)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('id',)

    def __str__(self):
        return self.username
