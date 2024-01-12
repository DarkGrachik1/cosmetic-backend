from rest_framework import serializers

from .models import *


class SubstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Substance
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    access_token = serializers.SerializerMethodField()

    def get_access_token(self, user):
        return self.context.get("access_token", "")

    class Meta:
        model = CustomUser
        fields = ('id', 'name', 'email', 'is_moderator', 'access_token')


class CosmeticSerializer(serializers.ModelSerializer):
    substances = serializers.SerializerMethodField()
    owner = UserSerializer(read_only=True, many=False)
    moderator = UserSerializer(read_only=True, many=False)

    def get_substances(self, cosmetic):
        items = SubCosm.objects.filter(cosmetic_id=cosmetic.pk)
        return SubstanceSerializer([item.substance for item in items], many=True).data

    class Meta:
        model = Cosmetic
        fields = "__all__"


class CosmeticsSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True, many=False)
    moderator = UserSerializer(read_only=True, many=False)

    class Meta:
        model = Cosmetic
        fields = "__all__"


class SubCosmSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCosm
        fields = "__all__"


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = CustomUser.objects.create(
            email=validated_data['email'],
            name=validated_data['name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)


