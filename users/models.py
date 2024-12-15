from django.contrib.auth.models import AbstractUser
from django.db import models


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


# class UserManager(BaseUserManager):
#     def create_user(self, email, password=None, **extra_fields):
#         """Создание обычного пользователя"""
#         if not email:
#             raise ValueError("Поле email обязательно.")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, password=None, **extra_fields):
#         """Создание суперпользователя"""
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#
#         return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)  # Поле для телефона
    city = models.CharField(max_length=50, blank=True, null=True)  # Поле для города
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)  # Поле для аватарки

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # objects = UserManager()

    USERNAME_FIELD = 'email'  # Поле, используемое для авторизации
    REQUIRED_FIELDS = []  # Дополнительные обязательные поля (пустой список)


    class Meta():
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email