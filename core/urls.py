from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('index/', views.index, name='index'),
    path('registrar/', views.registrar_propiedad, name='registrar_propiedad'),
    path('listar/', views.listar_propiedades, name='listar_propiedades'),
    #path('editar/<int:id>/', views.editar_propiedad, name='editar_propiedad'),
    #path('eliminar/<int:id>/', views.eliminar_propiedad, name='eliminar_propiedad'),
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('registrar_solicitante/', views.registrar_solicitante, name='registrar_solicitante'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('listar_solicitantes/', views.listar_solicitantes, name='listar_solicitantes'),
    path('registrar_movimientos/', views.registrar_movimiento, name='registrar_movimiento'),
    path('cargar_movimientos_por_propiedad/<int:propiedad_id>/', views.cargar_movimientos_por_propiedad, name='cargar_movimientos_por_propiedad'),
    path('buscar_solicitante/', views.buscar_solicitante, name='buscar_solicitante'),
    path('actualizar_estado/', views.actualizar_estado, name='actualizar_estado'),
    path('obtener_estado_propiedad/', views.obtener_estado_propiedad, name='obtener_estado_propiedad'),
    path('subir_pdf/<int:propiedad_id>/', views.subir_pdf, name='subir_pdf'),

 
]
    

