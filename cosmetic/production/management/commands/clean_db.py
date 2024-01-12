from django.core.management.base import BaseCommand
from production.models import *


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        SubCosm.objects.all().delete()
        Cosmetic.objects.all().delete()
        Substance.objects.all().delete()
        # User.objects.all().delete()