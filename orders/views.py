from django.contrib import messages
from django.shortcuts import render

from orders.forms import OrderNewForm
from orders.models import Order
from robots.models import Robot


def order_new(request):
    if request.method == 'POST':
        form = OrderNewForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            order = Order.create_by_email(**data)
            in_stock = Robot.objects.filter(serial=order.robot_serial)
            if in_stock:
                messages.success(request, f'Заказ размещён. Робот {order.robot_serial} доступен в наличии!')
            else:
                messages.warning(
                    request=request,
                    message=f'Заказ размещён. Однако робота {order.robot_serial} в данный момент нет в наличии. '
                            f'Мы пришлём вам письмо, когда он появится!',
                )
    else:
        form = OrderNewForm()

    context = {
        'title': '🤖 Новый заказ на робота',
        'form': form,
    }
    return render(request, 'orders/order_new.html', context)
