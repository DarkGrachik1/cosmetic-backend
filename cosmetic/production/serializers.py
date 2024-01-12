from .models import *
from rest_framework import serializers


class SubstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Substance
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'id')


class CosmeticSerializer(serializers.ModelSerializer):
    substances = serializers.SerializerMethodField()
    owner = UserSerializer(read_only=True, many=False)
    moderator = UserSerializer(read_only=True, many=False)

    def get_substances(self, cosmetic):
        items = SubCosm.objects.filter(cosmetic=cosmetic)
        return SubstanceSerializer([item.substance for item in items], many=True).data

    class Meta:
        model = Cosmetic
        fields = '__all__'
