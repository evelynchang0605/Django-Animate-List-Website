from django.urls import path
from . import views

app_name = "animate"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path('<int:pk>/', views.DetailView.as_view(), name="detail"),
    path('<int:pk>/recommend/', views.ResultsView.as_view(), name="results"),
    path('<int:animate_id>/vote/', views.vote, name="vote"),
    path('export/csv/', views.export_mylist_csv, name="export_mylist_csv"),
    path('export/img', views.change_mylist_csv_to_img, name="change_mylist_csv_to_img"),
]
