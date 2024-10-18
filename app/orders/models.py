from django.db import models
from users.models import User


class Order(models.Model):
    worker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_orders')
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_orders')
    skill = models.ForeignKey('users.Skill', on_delete=models.SET_NULL, null=True)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'В ожидании'), ('accepted', 'Принято'), ('rejected', 'Отклонено'),
                 ('completed', 'Выполнено')],
        default='pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Работодатель: {self.client} | Рабочий: {self.worker} | Навык: {self.skill}'