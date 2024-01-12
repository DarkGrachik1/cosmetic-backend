from datetime import datetime

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Услуга
class Substance(models.Model):
    STATUS_CHOICES = (
        (1, 'Действует'),
        (2, 'Удалена'),
    )

    name = models.CharField(verbose_name="Название", default="Название вещества")
    description = models.TextField(verbose_name="Описание", default="Описание косметики")

    status = models.IntegerField( verbose_name="Статус", choices=STATUS_CHOICES, default=1)
    image = models.ImageField(verbose_name="Картинка", upload_to="substances/", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Вещество"
        verbose_name_plural = "Вещества"


# Заявка
class Cosmetic(models.Model):
    STATUS_CHOICES = (
        (1, 'Введён'),
        (2, 'В работе'),
        (3, 'Завершен'),
        (4, 'Отклонен'),
        (5, 'Удален'),
    )

    CLINICAL_TRIAL_CHOICES = (
        (0, 'Одобрено'),
        (1, 'Отказано')
    )

    name = models.CharField(verbose_name="Название", default="Название косметики")
    description = models.TextField(verbose_name="Описание", default="Описание косметики", blank=True, null=True)
    clinical_trial = models.IntegerField(verbose_name="Результат клинических испытаний", choices=CLINICAL_TRIAL_CHOICES, blank=True, null=True)

    status = models.IntegerField(verbose_name="Статус", choices=STATUS_CHOICES, default=1)
    date_created = models.DateTimeField(verbose_name="Дата создания", default=timezone.now())
    date_of_formation = models.DateTimeField(verbose_name="Дата формирования", blank=True, null=True)
    date_complete = models.DateTimeField(verbose_name="Дата завершения", blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Создатель", related_name='owner', null=True)
    moderator = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Модератор", related_name='moderator', null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Косметика"
        verbose_name_plural = "Косметика"


# м-м
class SubCosm(models.Model):
    substance = models.ForeignKey(Substance, models.CASCADE, blank=True, null=True)
    cosmetic = models.ForeignKey(Cosmetic, models.CASCADE, blank=True, null=True)
    percent_in = models.FloatField(verbose_name="Процентное содержание", default=0.5)

    def __str__(self):
        return "Вещество-КRосметика №" + str(self.pk)

    class Meta:
        verbose_name = "Вещество-Косметика"
        verbose_name_plural = "Вещества-Косметика"