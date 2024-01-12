from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import *
from .models import *


def get_draft_cosmetic():
    cosmetic = Cosmetic.objects.filter(status=1).first()

    if cosmetic is None:
        return None

    return cosmetic


@api_view(["GET"])
def search_substance(request):
    name = request.GET.get('query', '')

    substance = Substance.objects.filter(status=1).filter(name__icontains=name)

    serializer = SubstanceSerializer(substance, many=True)

    draft_cosmetic = get_draft_cosmetic()

    data = {
        "substances": serializer.data,
        "draft_cosmetic": draft_cosmetic.pk if draft_cosmetic else None
    }

    return Response(data)


@api_view(['GET'])
def get_substance_by_id(request, substance_id):
    if not Substance.objects.filter(pk=substance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    substance = Substance.objects.get(pk=substance_id)

    serializer = SubstanceSerializer(substance, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
def update_substance(request, substance_id):
    if not Substance.objects.filter(pk=substance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    substance = Substance.objects.get(pk=substance_id)
    serializer = SubstanceSerializer(substance, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def create_substance(request):
    Substance.objects.create()

    substances = Substance.objects.all()
    serializer = SubstanceSerializer(substances, many=True)

    return Response(serializer.data)


@api_view(["DELETE"])
def delete_substance(request, substance_id):
    if not Substance.objects.filter(pk=substance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    substance = Substance.objects.get(pk=substance_id)
    substance.status = 2
    substance.save()

    substances = Substance.objects.filter(status=1)
    serializer = SubstanceSerializer(substances, many=True)

    return Response(serializer.data)


@api_view(["POST"])
def add_substance_to_cosmetic(request, substance_id):
    if not Substance.objects.filter(pk=substance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    substance = Substance.objects.get(pk=substance_id)

    draft_cosmetic = get_draft_cosmetic()

    if draft_cosmetic is None:
        draft_cosmetic = Cosmetic.objects.create()

    if SubCosm.objects.filter(cosmetic=draft_cosmetic, substance=substance).exists():
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    cons = SubCosm.objects.create()
    cons.cosmetic = draft_cosmetic
    cons.substance = substance
    cons.save()

    serializer = CosmeticSerializer(draft_cosmetic, many=False)

    return Response(serializer.data["substances"])


@api_view(["GET"])
def get_substance_image(request, substance_id):
    if not Substance.objects.filter(pk=substance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    service = Substance.objects.get(pk=substance_id)

    if not service.image:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return HttpResponse(service.image, content_type="image/png")


@api_view(["PUT"])
def update_substance_image(request, substance_id):
    if not Substance.objects.filter(pk=substance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    substance = Substance.objects.get(pk=substance_id)

    serializer = SubstanceSerializer(substance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()

    return HttpResponse(substance.image, content_type="image/png", status=status.HTTP_200_OK)


@api_view(["GET"])
def search_cosmetics(request):
    cosmetics = Cosmetic.objects.all()

    request_status = request.GET.get("status")
    if request_status:
        cosmetics = cosmetics.filter(status=request_status)

    serializer = CosmeticSerializer(cosmetics, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def get_cosmetic_by_id(request, cosmetic_id):
    if not Cosmetic.objects.filter(pk=cosmetic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    cosmetic = Cosmetic.objects.get(pk=cosmetic_id)
    serializer = CosmeticSerializer(cosmetic, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_cosmetic(request, cosmetic_id):
    if not Cosmetic.objects.filter(pk=cosmetic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    cosmetic = Cosmetic.objects.get(pk=cosmetic_id)
    serializer = CosmeticSerializer(cosmetic, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    cosmetic.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_cosmetic_clinical_trial(request, cosmetic_id):
    if not Cosmetic.objects.filter(pk=cosmetic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    cosmetic = Cosmetic.objects.get(pk=cosmetic_id)
    serializer = CosmeticSerializer(cosmetic, data=request.data, many=False, partial=True)

    if serializer.is_valid():
        serializer.save()

    cosmetic.save()

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_user(request, cosmetic_id):
    if not Cosmetic.objects.filter(pk=cosmetic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    cosmetic = Cosmetic.objects.get(pk=cosmetic_id)

    if cosmetic.status != 1:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    cosmetic.status = 2
    cosmetic.date_of_formation = timezone.now()
    cosmetic.save()

    serializer = CosmeticSerializer(cosmetic, many=False)

    return Response(serializer.data)


@api_view(["PUT"])
def update_status_admin(request, cosmetic_id):
    if not Cosmetic.objects.filter(pk=cosmetic_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    request_status = request.data["status"]

    if request_status not in [3, 4]:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    cosmetic = Cosmetic.objects.get(pk=cosmetic_id)

    if cosmetic.status != 2:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    cosmetic.status = request_status
    cosmetic.date_complete = timezone.now()
    cosmetic.save()

    serializer = CosmeticSerializer(cosmetic, many=False)

    return Response(serializer.data)


@api_view(["DELETE"])
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
def delete_substance_from_cosmetic(request, cosmetic_id, substance_id):
    if not SubCosm.objects.filter(cosmetic_id=cosmetic_id, substance_id=substance_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)

    item = SubCosm.objects.get(cosmetic_id=cosmetic_id, substance_id=substance_id)
    item.delete()

    cosmetic = Cosmetic.objects.get(pk=cosmetic_id)

    serializer = CosmeticSerializer(cosmetic, many=False)

    return Response(serializer.data["substances"])