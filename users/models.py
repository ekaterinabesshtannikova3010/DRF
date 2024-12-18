from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from materials.models import Course, Lesson


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)  # Поле для телефона
    city = models.CharField(max_length=50, blank=True, null=True)  # Поле для города
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Поле для аватарки

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta():
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='payments')
    payment_date = models.DateTimeField(auto_now_add=True)  # Дата оплаты
    paid_course = models.ForeignKey(Course, null=True, blank=True, on_delete=models.SET_NULL)  # Оплаченный курс
    paid_lesson = models.ForeignKey(Lesson, null=True, blank=True, on_delete=models.SET_NULL)  # Оплаченный урок
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Сумма оплаты
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)  # Способ оплаты

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f'Платеж {self.id} от {self.user} на сумму {self.amount} ({self.payment_method})'
