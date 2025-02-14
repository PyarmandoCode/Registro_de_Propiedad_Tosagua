from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now



class Solicitante(models.Model):
     nombre = models.CharField(max_length=255)
     apellido = models.CharField(max_length=255)
     cedula = models.CharField(max_length=10)
     tipo_solicitud= models.CharField(max_length=10)
     usuario = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    
     def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Propiedades(models.Model):
    codigo_interno= models.CharField(max_length=255,blank=True,null=True)
    bien_inmueble= models.CharField(max_length=255)
    ubicacion =  models.CharField(max_length=255,blank=True,null=True)
    area =  models.CharField(max_length=255,blank=True,null=True)
    solicitante = models.ForeignKey(Solicitante, on_delete=models.CASCADE)
    estado=models.CharField(max_length=69,blank=True,null=True)
    archivo_pdf = models.FileField(upload_to='pdfs/', blank=True, null=True)
    documento_pdf = models.FileField(upload_to='documento/', blank=True, null=True)
    


    def __str__(self):
        return self.bien_inmueble

class Registro(models.Model):
    titulo = models.CharField(max_length=255)
    fecha_inscripcion=models.DateField()
    Numero_Inscripcion=models.IntegerField()
    oficina_guarda_original=models.CharField(max_length=255)
    nombre_canton= models.CharField(max_length=255,blank=True,null=True)
    observaciones=models.TextField(blank=True,null=True)
    fecha_resolucion=models.DateField()
    solicitante = models.ForeignKey(Solicitante, on_delete=models.CASCADE,blank=True,null=True)
    administrador = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="propiedades", limit_choices_to={'is_staff': True}
    )
    def __str__(self):
        return self.titulo
    
class Movimientos(models.Model):
    libro=models.CharField(max_length=255)
    acto=models.CharField(max_length=255)
    numero_Inscripcion=models.IntegerField()
    fecha_inscripcion=models.DateField()
    folio_inicial=models.CharField(max_length=255)
    Propiedad = models.ForeignKey(Propiedades, on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return self.libro
    
    
