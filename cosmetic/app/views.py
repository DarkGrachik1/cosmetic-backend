import requests
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.utils.dateparse import parse_datetime
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from .jwt_helper import *
from .permissions import *
from .serializers import *
from .utils import identity_user


def get_draft_cosmetic(request):
    user = identity_user(request)

    if user is None:
        return None

    cosmetic = Cosmetic.objects.filter(owner_id=user.pk).filter(status=1).first()

    if cosmetic is None:
        return None

    return cosmetic


@api_view(["GET"])
def search_substances(request):
    query = request.GET.get("query", "")

    substances = Substance.objects.filter(status=1).filter(name__icontains=query)

    serializer = SubstanceSerializer(substances, many=True)

    draft_cosmetic = get_draft_cosmetic(request)

    resp = {
        "substances": serializer.data,
        "draft_cosmetic_id": draft_cosmetic.pk if draft_cosmetic else None
    }

    return Response(resp)


@api_view(["GET"])
def get_substance_by_id(request, substance_id):
    if not Substance.objects.filter(pk=substance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    substance = Substance.objects.get(pk=substance_id)
    serializer = SubstanceSerializer(substance)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_substance(request, substance_id):
    if not Substance.objects.filter(pk=substance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    substance = Substance.objects.get(pk=substance_id)
    serializer = SubstanceSerializer(substance, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsModerator])
def create_substance(request):
    substance = Substance.objects.create()

    serializer = SubstanceSerializer(substance)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_substance(request, substance_id):
    if not Substance.objects.filter(pk=substance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    substance = Substance.objects.get(pk=substance_id)
    substance.status = 5
    substance.save()

    substances = Substance.objects.filter(status=1)
    serializer = SubstanceSerializer(substances, many=True)

    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def add_substance_to_cosmetic(request, substance_id):
    if not Substance.objects.filter(pk=substance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    substance = Substance.objects.get(pk=substance_id)

    draft_cosmetic = get_draft_cosmetic(request)

    if draft_cosmetic is None:
        draft_cosmetic = Cosmetic.objects.create()
        draft_cosmetic.owner = identity_user(request)
        draft_cosmetic.save()

    if SubCosm.objects.filter(cosmetic=draft_cosmetic, substance=substance).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    cons = SubCosm.objects.create()
    cons.cosmetic = draft_cosmetic
    cons.substance = substance
    cons.save()

    serializer = CosmeticSerializer(draft_cosmetic)

    return Response(serializer.data)


@api_view(["GET"])
def get_substance_image(request, substance_id):
    if not Substance.objects.filter(pk=substance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    substance = Substance.objects.get(pk=substance_id)

    return HttpResponse(substance.image, content_type="image/png")


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_substance_image(request, substance_id):
    if not Substance.objects.filter(pk=substance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    substance = Substance.objects.get(pk=substance_id)
    serializer = SubstanceSerializer(substance, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def search_cosmetics(request):
    user = identity_user(request)

    status_id = int(request.GET.get("status", -1))
    date_start = request.GET.get("date_start", -1)
    date_end = request.GET.get("date_end", -1)

    cosmetics = Cosmetic.objects.exclude(status__in=[1, 5])

    if not user.is_moderator:
        cosmetics = cosmetics.filter(owner_id=user.pk)

    if status_id != -1:
        cosmetics = cosmetics.filter(status=status_id)

    if date_start:
        cosmetics = cosmetics.filter(date_formation__gte=parse_datetime(date_start))

    if date_end:
        cosmetics = cosmetics.filter(date_formation__lte=parse_datetime(date_end))

    serializer = CosmeticsSerializer(cosmetics, many=True)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_cosmetic_by_id(request, cosmetic_id):
    if not Cosmetic.objects.filter(pk=cosmetic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    cosmetic = Cosmetic.objects.get(pk=cosmetic_id)
    serializer = CosmeticSerializer(cosmetic)

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_cosmetic(request, cosmetic_id):
    if not Cosmetic.objects.filter(pk=cosmetic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    cosmetic = Cosmetic.objects.get(pk=cosmetic_id)
    serializer = CosmeticSerializer(cosmetic, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsRemoteService])
def update_cosmetic_clinical_trial(request, cosmetic_id):
    if not Cosmetic.objects.filter(pk=cosmetic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    cosmetic = Cosmetic.objects.get(pk=cosmetic_id)
    serializer = CosmeticSerializer(cosmetic, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_status_user(request, cosmetic_id):
    if not Cosmetic.objects.filter(pk=cosmetic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    cosmetic = Cosmetic.objects.get(pk=cosmetic_id)

    cosmetic.owner = identity_user(request)
    cosmetic.status = 2
    cosmetic.date_formation = timezone.now()
    cosmetic.save()

    calculate_clinical_trial(cosmetic_id)

    serializer = CosmeticSerializer(cosmetic)

    return Response(serializer.data)


def calculate_clinical_trial(cosmetic_id):
    data = {
        "cosmetic_id": cosmetic_id
    }

    requests.post("http://localhost:8070/calc_clinical_trial/", json=data, timeout=3)


@api_view(["PUT"])
@permission_classes([IsModerator])
def update_status_admin(request, cosmetic_id):
    if not Cosmetic.objects.filter(pk=cosmetic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = int(request.data["status"])

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    cosmetic = Cosmetic.objects.get(pk=cosmetic_id)

    if cosmetic.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    cosmetic.moderator = identity_user(request)
    cosmetic.status = request_status
    cosmetic.date_complete = timezone.now()
    cosmetic.save()

    serializer = CosmeticSerializer(cosmetic)

    return Response(serializer.data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_cosmetic(request, cosmetic_id):
    if not Cosmetic.objects.filter(pk=cosmetic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    cosmetic = Cosmetic.objects.get(pk=cosmetic_id)

    if cosmetic.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    cosmetic.status = 5
    cosmetic.save()

    return Response(status=status.HTTP_200_OK)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_substance_from_cosmetic(request, cosmetic_id, substance_id):
    if not SubCosm.objects.filter(cosmetic_id=cosmetic_id, substance_id=substance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = SubCosm.objects.get(cosmetic_id=cosmetic_id, substance_id=substance_id)
    item.delete()

    cosmetic = Cosmetic.objects.get(pk=cosmetic_id)

    serializer = CosmeticSerializer(cosmetic)

    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_substance_in_cosmetic(request, cosmetic_id, substance_id):
    if not SubCosm.objects.filter(substance_id=substance_id, cosmetic_id=cosmetic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = SubCosm.objects.get(substance_id=substance_id, cosmetic_id=cosmetic_id)
    return Response(item.percent_in)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_substance_in_cosmetic(request, cosmetic_id, substance_id):
    if not SubCosm.objects.filter(substance_id=substance_id, cosmetic_id=cosmetic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = SubCosm.objects.get(substance_id=substance_id, cosmetic_id=cosmetic_id)

    serializer = SubCosmSerializer(item, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@swagger_auto_schema(method='post', request_body=UserLoginSerializer)
@api_view(["POST"])
def login(request):
    serializer = UserLoginSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    user = authenticate(**serializer.data)
    if user is None:
        message = {"message": "Введенные данные невалидны"}
        return Response(message, status=status.HTTP_401_UNAUTHORIZED)

    access_token = create_access_token(user.id)

    serializer = UserSerializer(
        user,
        context={
            "access_token": access_token
        }
    )

    response = Response(serializer.data, status=status.HTTP_200_OK)

    response.set_cookie('access_token', access_token, httponly=False, expires=settings.JWT["ACCESS_TOKEN_LIFETIME"])

    return response


@api_view(["POST"])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(status=status.HTTP_409_CONFLICT)

    user = serializer.save()

    access_token = create_access_token(user.id)

    message = {
        'message': 'Пользователь успешно зарегистрирован',
        'user_id': user.id,
        "access_token": access_token
    }

    response = Response(message, status=status.HTTP_201_CREATED)

    response.set_cookie('access_token', access_token, httponly=False, expires=settings.JWT["ACCESS_TOKEN_LIFETIME"])

    return response


@api_view(["POST"])
def check(request):
    user = identity_user(request)

    user = CustomUser.objects.get(pk=user.pk)
    serializer = UserSerializer(user)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request):
    access_token = get_access_token(request)

    if access_token not in cache:
        cache.set(access_token, settings.JWT["ACCESS_TOKEN_LIFETIME"])

    message = {"message": "Вы успешно вышли из аккаунта"}
    response = Response(message, status=status.HTTP_200_OK)

    response.delete_cookie('access_token')

    return response
