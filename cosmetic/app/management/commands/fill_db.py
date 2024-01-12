import random

from django.core import management
from django.core.management.base import BaseCommand
from ...models import *
from .utils import random_date, random_timedelta
from ...utils import random_text


def add_substances():
    Substance.objects.create(
        name="4-терт-бутил циклогексанол",
        description="Он является инновационным синтетическим соединением с выраженной противовоспалительной активностью.",
        image="substances/1.png"
    )
    Substance.objects.create(
        name="Massocare",
        description="Жидкий неионногенный ПАВ для гидрофильных масел, со-эмульгатор для эмульсий вода-в-масле.",
        image="substances/2.png"
    )
    Substance.objects.create(
        name="Protein HPTW",
        description="Гидролизованные протеины пшеницы обладают сродством к кератину из которого состоит волос.",
        image="substances/3.png"
    )
    Substance.objects.create(
        name="Ацетил тетрапептид-40",
        description="Ацетил тетрапептид-40 обладает противовоспалительным эффектом.",
        image="substances/4.png"
    )
    Substance.objects.create(
        name="Гидроксипинаколона ретиноат",
        description="Гидроксипинаколона ретиноат – одна из наиболее современных форм ретиноидов.",
        image="substances/5.png"
    )
    Substance.objects.create(
        name="Protein VEG",
        description="Гидролизованные растительные протеины обладают сродством к кератину из которого состоит волос.",
        image="substances/6.png"
    )
    Substance.objects.create(
        name="Тетрабутан",
        description="Технологичный акрилатный эмульгатор и загуститель.",
        image="substances/7.png"
    )

    print("Услуги добавлены")


def add_cosmetics():
    users = CustomUser.objects.filter(is_superuser=False)
    moderators = CustomUser.objects.filter(is_superuser=True)

    if len(users) == 0 or len(moderators) == 0:
        print("Заявки не могут быть добавлены. Сначала добавьте пользователей с помощью команды add_users")
        return

    substances = Substance.objects.all()

    for _ in range(30):
        cosmetic = Cosmetic.objects.create()
        cosmetic.name = "Косметика №" + str(cosmetic.pk)
        cosmetic.description = random_text(10)
        cosmetic.status = random.randint(2, 5)
        cosmetic.owner = random.choice(users)

        if random.randint(0, 10) > 3:
            cosmetic.clinical_trial = random.randint(0, 1)

        if cosmetic.status in [3, 4]:
            cosmetic.date_complete = random_date()
            cosmetic.date_formation = cosmetic.date_complete - random_timedelta()
            cosmetic.date_created = cosmetic.date_formation - random_timedelta()
            cosmetic.moderator = random.choice(moderators)
            cosmetic.clinical_trial = random.randint(0, 1)
        else:
            cosmetic.date_formation = random_date()
            cosmetic.date_created = cosmetic.date_formation - random_timedelta()

        for i in range(random.randint(1, 3)):
            try:
                item = SubCosm.objects.create()
                item.cosmetic = cosmetic
                item.substance = random.choice(substances)
                item.percent_in = random.randint(1, 100)
                item.save()
            except Exception as e:
                print(e)

        cosmetic.save()

    print("Заявки добавлены")


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        management.call_command("clean_db")
        management.call_command("add_users")

        add_substances()
        add_cosmetics()









