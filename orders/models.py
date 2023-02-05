from django.core.mail import send_mass_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from R4C.settings import EMAIL_HOST_USER
from robots.models import Robot
from customers.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    robot_serial = models.CharField(max_length=5, blank=False, null=False)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['pk']

    @classmethod
    def create_by_email(cls, email: str = '', robot_serial: str = None):
        email = email.lower()
        try:
            customer = Customer.objects.get(email=email)
        except:
            customer = Customer.objects.create(email=email)
        return cls.objects.create(customer=customer, robot_serial=robot_serial)


@receiver(post_save, sender=Robot)
def mailing_by_orders_when_create_robot(instance: Robot, created, **kwargs):
    """
        Если создали нового робота в БД, то отправляется письмо клиентам, которые его заказывали.
        Я бы ещё добавил поле finished = BooleanField, чтобы отправлять письма только тем, кто ожидает заказ.
        Но, насколько я понял, менять модели нельзя в этом задании.
    """
    if created:
        robot_serial = instance.serial
        emails = Order.objects.filter(robot_serial=robot_serial) \
            .select_related('customer') \
            .order_by('customer__email') \
            .distinct() \
            .values_list('customer__email', flat=True)
        message = f'Роботы {robot_serial} появились в наличии!'
        mails = (
            (
                message,
                f'{message}\nСвяжитесь с нами для заказа.',
                EMAIL_HOST_USER,
                list(emails)
            ),
        )
        send_mass_mail(mails)

