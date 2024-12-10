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
    use_points = models.BooleanField(default=False)
    points_used = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cash_payment = models.BooleanField(default=False, verbose_name='Оплата наличными')

    def __str__(self):
        return f'Работодатель: {self.client} | Рабочий: {self.worker} | Навык: {self.skill}'


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=None)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=[
        ('deposit', 'Пополнение'),
        ('withdrawal', 'Вывод'),
        ('reserved', 'Резервирование'),
        ('cancellation', 'Отмена'),
        ('payment', 'Оплата'),
    ])
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
