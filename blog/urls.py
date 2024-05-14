from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.Register.as_view(), name="register"),
    path("new/", views.BlogCreate.as_view(), name="new"),
    path("blogs/", views.BlogListView.as_view(), name="blogs"),
]
