from django.urls import path
from . import views
app_name = 'apps.core'

urlpatterns = [
    path('', views.Index, name="index"),
    path('<int:id>', views.Profile, name="perfil"),
    path('/ext/<str:usuario>', views.Extender, name="extender")
]