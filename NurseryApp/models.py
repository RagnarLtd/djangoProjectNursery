from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    """
    Расширение данных пользователя
    """
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    shelter = models.CharField(max_length=100, verbose_name='приют')
    address = models.CharField(max_length=150, verbose_name='адрес')


class Pet(models.Model):
    """
    Модель питомца с параметрами
    """
    nickname = models.CharField(max_length=20, verbose_name='кличка')
    age = models.PositiveIntegerField(verbose_name='возраст')
    date_in = models.DateField(auto_now_add=True, verbose_name='дата заезда в приют')
    weight = models.PositiveIntegerField(verbose_name='вес')
    growth = models.PositiveIntegerField(verbose_name='рост')
    is_active = models.BooleanField(default=True)
    special_signs = models.CharField(max_length=1000, blank=True, verbose_name='особые приметы')
    shelter = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
