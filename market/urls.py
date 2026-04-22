from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/price", views.api_price, name="api_price"),
    path("api/history", views.api_history, name="api_history"),
    path("api/history.csv", views.api_history_csv, name="api_history_csv"),
]
