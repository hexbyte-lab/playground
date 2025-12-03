from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create-checkout-session/", views.create_checkout_session, name="create_checkout_session"),

    # success page after payment
    path("success/<str:pack_id>/<str:session_id>/", views.success, name="success"),

    # download package only if paid
    path("download/<str:pack_id>/<str:session_id>/", views.download_package, name="download_package"),
]
