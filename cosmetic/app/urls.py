from django.urls import path
from .views import *

urlpatterns = [
    # Набор методов для услуг
    path('api/substances/search/', search_substances),  # GET
    path('api/substances/<int:substance_id>/', get_substance_by_id),  # GET
    path('api/substances/<int:substance_id>/image/', get_substance_image),  # GET
    path('api/substances/<int:substance_id>/update/', update_substance),  # PUT
    path('api/substances/<int:substance_id>/update_image/', update_substance_image),  # PUT
    path('api/substances/<int:substance_id>/delete/', delete_substance),  # DELETE
    path('api/substances/create/', create_substance),  # POST
    path('api/substances/<int:substance_id>/add_to_cosmetic/', add_substance_to_cosmetic),  # POST

    # Набор методов для заявок
    path('api/cosmetics/search/', search_cosmetics),  # GET
    path('api/cosmetics/<int:cosmetic_id>/', get_cosmetic_by_id),  # GET
    path('api/cosmetics/<int:cosmetic_id>/update/', update_cosmetic),  # PUT
    path('api/cosmetics/<int:cosmetic_id>/update_clinical_trial/', update_cosmetic_clinical_trial),  # PUT
    path('api/cosmetics/<int:cosmetic_id>/update_status_user/', update_status_user),  # PUT
    path('api/cosmetics/<int:cosmetic_id>/update_status_admin/', update_status_admin),  # PUT
    path('api/cosmetics/<int:cosmetic_id>/delete/', delete_cosmetic),  # DELETE

    # м-м
    path('api/cosmetics/<int:cosmetic_id>/substances/<int:substance_id>/', get_substance_in_cosmetic),  # GET
    path('api/cosmetics/<int:cosmetic_id>/update_substance/<int:substance_id>/', update_substance_in_cosmetic),  # PUT
    path('api/cosmetics/<int:cosmetic_id>/delete_substance/<int:substance_id>/', delete_substance_from_cosmetic),  # DELETE

    # Набор методов для аутентификации и авторизации
    path("api/register/", register),
    path("api/login/", login),
    path("api/check/", check),
    path("api/logout/", logout)
]
