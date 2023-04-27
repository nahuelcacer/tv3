from django.urls import path
from . import views
from iniciar import Extender
app_name = 'apps.core'

urlpatterns = [
    path('', views.Index, name="index"),
    path('<int:id>', views.Profile, name="perfil"),
    path('ext/<str:usuario>', views.Extender, name="extender"),
    path('crear', views.Crear, name="crear"),
    path('modificar', views.Modificar, name="modificar"),
    path('<int:id>/acortar', views.Acortar , name="acortar" )
]