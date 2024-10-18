from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from users.models import User
from .models import Order
from users.models import Skill
from django.contrib import messages
from decimal import Decimal


class CreateOrderView(View):
    def get(self, request, username):
        worker = get_object_or_404(User, username=username)
        skills = worker.skills.all()
        return render(request, 'orders/create_order.html', {
            'worker': worker,
            'skills': skills
        })

    def post(self, request, username):
        worker = get_object_or_404(User, username=username)
        skill_id = request.POST.get('skill')
        description = request.POST.get('description')
        amount = Decimal(request.POST.get('amount'))

        if not skill_id or not description or not amount:
            messages.warning(request, 'Заполните все поля.')
            return redirect('orders:create_order', username=username)

        skill = get_object_or_404(Skill, id=skill_id)

        # check the users balance
        if request.user.balance < amount:
            messages.warning(request, 'У вас недостаточно средств для создания заказа.')
            return redirect('orders:create_order', username=username)

        # Write off funds
        request.user.balance -= amount
        request.user.save()

        # creating order
        order = Order.objects.create(
            client=request.user,
            worker=worker,
            skill=skill,
            description=description,
            amount=amount,
            status='pending'
        )

        messages.success(request, 'Заказ успешно создан! Средства зарезервированы.')
        return redirect('users:profile')


class OrderActionView(View):
    def post(self, request, pk, action):
        order = get_object_or_404(Order, pk=pk)

        if action == 'accept':
            order.worker = request.user
            order.status = 'accepted'
            order.worker.is_free = False
            order.worker.save()
            order.save()
            messages.success(request, "Вы приняли заказ.")

        elif action == 'reject':
            # return the reserved money to the employer if the worker refuses the order.
            order.client.balance += order.amount
            order.client.save()

            order.status = 'rejected'
            order.save()
            messages.error(request, "Вы отказались от заказа.")

        elif action == 'complete':
            if request.user != order.client:
                messages.error(request, "У вас нет прав завершать этот заказ.")
                return redirect('users:profile')

            # We calculate the commission and transfer money to the worker
            commission = order.amount * Decimal('0.05')
            amount_to_worker = order.amount - commission

            order.worker.balance += amount_to_worker
            order.worker.is_free = True
            order.worker.save()

            order.status = 'completed'

            order.save()

            messages.success(request, "Заказ успешно завершён!")

        return redirect('users:profile')
