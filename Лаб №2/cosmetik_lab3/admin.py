from django.contrib import admin
from .models import Cosmetic
from .models import SubCosm
from .models import Substance
##from .models import Users

##admin.site.register(Users)
admin.site.register(Substance)
admin.site.register(SubCosm)
admin.site.register(Cosmetic)
