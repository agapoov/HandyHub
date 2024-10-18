from django.contrib.auth.models import AbstractUser
from django.db import models
from decimal import Decimal


class Skill(models.Model):
    name = models.CharField(max_length=128)
    icon = models.ImageField(upload_to='static/deps/skills_images', blank=True, null=True)
    slug = models.SlugField(max_length=256, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name


class User(AbstractUser):
    ROLE_CHOICES = (
        ('worker', 'Рабочий'),
        ('employer', 'Работодатель')
    )
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to='media/users_images', null=True, blank=True)
    about_me = models.TextField(max_length=1024, blank=True, null=True, default='')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='worker')
    surname = models.CharField(max_length=128)
    phone = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
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
