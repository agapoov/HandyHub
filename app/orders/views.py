from decimal import Decimal

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from users.models import Skill, User

from .models import Order, Transaction


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
        use_points = request.POST.get('use_points') == 'on'
        points_used = Decimal(request.POST.get('points_used') or 0)
        cash_payment = request.POST.get('cash_payment') == 'on'
        if not skill_id or not description or not amount:
            messages.warning(request, 'Заполните все поля.')
            return redirect('orders:create_order', username=username)

        skill = get_object_or_404(Skill, id=skill_id)

        if use_points and points_used > request.user.points:
            messages.warning(request, 'Недостаточно баллов для списания.')
            return redirect('orders:create_order', username=username)

        if not cash_payment:
            if use_points:
                amount -= points_used

            if request.user.balance < amount:
                messages.warning(
                    request,
                    f'Для создания заказа необходимо {amount} руб., а у вас всего {request.user.balance} руб.'
                )
                return redirect('orders:create_order', username=username)

            request.user.balance -= amount
            request.user.points -= points_used
            request.user.save()

        order = Order.objects.create(
            client=request.user,
            worker=worker,
            skill=skill,
            description=description,
            amount=amount + points_used,
            points_used=points_used,
            cash_payment=cash_payment,
            status='pending'
        )

        if not cash_payment:
            Transaction.objects.create(
                user=request.user,
                order=order,
                amount=amount + points_used,
                transaction_type='reserved',
                description=f'Резервирование средств для заказа {order.id}',
            )

        if cash_payment:
            messages.success(request, 'Заказ успешно создан! Оплата наличными при выполнении.')
        else:
            messages.success(request, 'Заказ успешно создан! Средства зарезервированы.')

        return redirect('users:profile')


class OrderActionView(View):
    def post(self, request, pk, action):
        order = get_object_or_404(Order, pk=pk)
        transaction = Transaction.objects.get(order=order)

        if action == 'accept':
            order.worker = request.user
            order.status = 'accepted'
            order.worker.is_free = False
            order.worker.save()
            order.save()
            messages.success(request, "Вы приняли заказ.")

        elif action == 'reject':
            # return the reserved money to the employer if the worker refuses the order.
            order.client.balance += order.amount - order.points_used
            order.client.points += order.points_used
            order.status = 'rejected'
            transaction.transaction_type = 'cancellation'
            transaction.description = 'Отказ от заказа, возврат денег работодателю.'

            transaction.save()
            order.client.save()
            order.save()
            messages.warning(request, "Вы отказались от заказа.")

        elif action == 'complete':
            if request.user != order.client:
                messages.warning(request, "У вас нет прав завершать этот заказ.")
                return redirect('users:profile')

            # We calculate the commission and transfer money to the worker
            commission = order.amount * Decimal('0.01')  # Change if we want to earn more money: 0.01 = 1%, etc.
            amount_to_worker = order.amount - commission

            order.worker.balance += amount_to_worker
            order.worker.is_free = True

            order.status = 'completed'
            transaction.transaction_type = 'payment'

            transaction.description = 'Успешная оплата за заказ'
            transaction.save()
            order.worker.save()
            order.save()

            Transaction.objects.create(
                user=order.worker,
                order=order,
                amount=amount_to_worker,
                transaction_type='payment',
                description='Поздравляем с выполнением заказа.',
            )
            messages.success(request, "Заказ успешно завершён!")

        return redirect('users:profile')
