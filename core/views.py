from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Propiedades,Solicitante,Registro,Movimientos

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages  # Para enviar mensajes a las plantillas
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from django.core.files.base import ContentFile
import io
import datetime

def index(request):
    template_name="dashboard.html"
    return render(request,template_name)

@login_required
def registrar_propiedad(request):
    nombre = request.GET.get('nombre', '')
    apellido = request.GET.get('apellido', '')
    soli = Solicitante.objects.filter(nombre=nombre, apellido=apellido).first()  # Tomamos el primero si 
    registro = Registro.objects.filter(solicitante=soli).first() if soli else None
    propiedades = Propiedades.objects.filter(solicitante=soli) if soli else []
    if registro:
        titulo = registro.titulo
        numero_inscripcion = registro.Numero_Inscripcion
        oficina = registro.oficina_guarda_original
        canton = registro.nombre_canton
        fecha_resolucion = registro.fecha_resolucion
        fecha_inscripcion = registro.fecha_inscripcion
        observaciones = registro.observaciones
    else:
        titulo = numero_inscripcion = oficina = canton = fecha_resolucion = fecha_inscripcion = observaciones = ''
    if request.method == 'POST':
        try:
            
            nombres = request.POST.get('nombres', '').strip()  # Aseguramos que no haya espacios vacíos
            apellidos = request.POST.get('apellidos', '').strip()
            soli = Solicitante.objects.filter(nombre=nombres, apellido=apellidos).first()
            # Crear la propiedad a partir del formulario
            Registro.objects.create(
                administrador=request.user,  # Usuario autenticado como administrador
                titulo=request.POST['titulo'],
                observaciones=request.POST['descripcion'],
                Numero_Inscripcion =  request.POST['numeroregistro'],
                oficina_guarda_original =  request.POST['oficina'],
                nombre_canton =  request.POST['canton'],
                fecha_resolucion =  request.POST['fecharesolucion'],
                fecha_inscripcion =  request.POST['fechainscripcion'],
                solicitante=soli
                
            )
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
    return render(request, 'registrar_propiedad.html', {
        'nombre': nombre,
        'apellido': apellido,
        'registro': registro,
        'titulo': titulo,
        'numero_inscripcion': numero_inscripcion,
        'oficina': oficina,
        'canton': canton,
        'fecha_resolucion': fecha_resolucion,
        'fecha_inscripcion': fecha_inscripcion,
        'observaciones': observaciones,
        'propiedades': propiedades,
    })
    
@login_required
def listar_propiedades(request):
    if not request.user.is_authenticated:
        return render(request, 'listar_propiedades_sol.html', {'propiedades': []})

    try:
        solicitante = Solicitante.objects.get(usuario=request.user)
        propiedades = Propiedades.objects.filter(solicitante=solicitante)
    except Solicitante.DoesNotExist:
        propiedades = []  # Si el usuario no tiene solicitante, no se muestran propiedades.

    return render(request, 'listar_propiedades_sol.html', {'propiedades': propiedades})


# def editar_propiedad(request, id):
#     propiedad = get_object_or_404(Propiedad, id=id)
#     if request.method == 'POST':
#         propiedad.numero_registro=request.POST['numeroregistro']
#         propiedad.titulo = request.POST['titulo']
#         propiedad.descripcion = request.POST['descripcion']
#         propiedad.ubicacion = request.POST['ubicacion']
#         propiedad.area = request.POST['area']
#         propiedad.precio = request.POST['precio']
#         propiedad.disponible = request.POST['disponible'] == 'True'
#         propiedad.save()
#         return redirect('listar_propiedades')
#     return render(request, 'editar_propiedad.html', {'propiedad': propiedad})

# def eliminar_propiedad(request, id):
#     propiedad = get_object_or_404(Propiedad, id=id)
    
#     if request.method == "POST":
#         propiedad.delete()
#         return JsonResponse({"status": "success", "message": "Propiedad eliminada exitosamente"})
    
#     return JsonResponse({"status": "error", "message": "No se pudo eliminar la propiedad"}, status=400)

# Vista de login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                #messages.success(request, f"Bienvenido, {user.username}")
                return redirect('index')  # Redirige a la página principal
            else:
                messages.error(request, "Usuario o contraseña incorrectos.")
        else:
            messages.error(request, "Usuario o contraseña incorrectos.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Vista de registro
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirigir al login después de registrar
        else:
            # Extraer errores y pasarlos al template
            errores = form.errors.get_json_data()
    else:
        form = UserCreationForm()
        errores = None

    return render(request, 'register.html', {'form': form, 'errores': errores})


@login_required
def registrar_solicitante(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': False, 'error': 'Usuario no autenticado'}, status=403)

    # Buscar si el usuario ya tiene un solicitante registrado
    solicitante = Solicitante.objects.filter(usuario=request.user).first()

    if request.method == 'POST' and not solicitante:
        try:
            solicitante = Solicitante.objects.create(
                nombre=request.POST['nombre'],
                apellido=request.POST['apellido'],
                cedula=request.POST['cedula'],
                tipo_solicitud=request.POST['tipo'],
                usuario=request.user
            )
            return JsonResponse({
                'success': True,
                'nombre': solicitante.nombre,
                'apellido': solicitante.apellido,
                'cedula': solicitante.cedula,
                'tipo_solicitud': solicitante.tipo_solicitud,
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    # Si el solicitante ya existe, simplemente se cargan sus datos en el formulario
    return render(request, 'registrar_solicitante.html', {'solicitante': solicitante})



def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('login')  # Redirige a la página de inicio de sesión u otra página

@login_required
def listar_solicitantes(request):
    solicitantes = Solicitante.objects.all()
    return render(request, 'listar_solicitantes.html', {'solicitantes': solicitantes})


@csrf_exempt
def registrar_movimiento(request):
    if request.method == "POST":
        propiedad_id = request.POST.get('propiedad_id')
        print(f"propieda id {propiedad_id}")
        libro = request.POST.get('libro')
        acto = request.POST.get('acto')
        numero_Inscripcion = request.POST.get('numero_Inscripcion')
        fecha_inscripcion = request.POST.get('fecha_inscripcion')
        folio_inicial = request.POST.get('folio_inicial')

        # Verificar si el valor de propiedad_id es válido
        if not propiedad_id:
            return JsonResponse({
                'success': False,
                'message': 'El ID de la propiedad no ha sido proporcionado.'
            }, status=400)

        # Obtener la propiedad seleccionada
        propiedad = get_object_or_404(Propiedades, id=propiedad_id)

    
        # Crear el movimiento
        movimiento = Movimientos(
            libro=libro,
            acto=acto,
            numero_Inscripcion=numero_Inscripcion,
            fecha_inscripcion=fecha_inscripcion,
            folio_inicial=folio_inicial,
            Propiedad=propiedad  # Asocia la propiedad seleccionada
        )
        movimiento.save()

        return JsonResponse({
            'success': True,
            'message': 'Movimiento registrado correctamente.'
        })

    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

def cargar_movimientos_por_propiedad(request, propiedad_id):
    propiedad = Propiedades.objects.get(id=propiedad_id)
    movimientos = Movimientos.objects.filter(Propiedad=propiedad)

    # Verificar si hay un archivo PDF
    archivo_pdf_url = None
    if propiedad.archivo_pdf:
        archivo_pdf_url = propiedad.archivo_pdf.url

    movimientos_data = [
        {
            "libro": mov.libro,
            "acto": mov.acto,
            "numero_Inscripcion": mov.numero_Inscripcion,
            "fecha_inscripcion": mov.fecha_inscripcion,
            "folio_inicial": mov.folio_inicial,
        }
        for mov in movimientos
    ]

    # Responder con los movimientos en formato JSON
    return JsonResponse({'movimientos': movimientos_data ,'archivo_pdf_url': archivo_pdf_url})

def buscar_solicitante(request):
    """ Busca un solicitante por cédula y devuelve sus datos en JSON """
    cedula = request.GET.get('cedula')
    try:
        solicitante = Solicitante.objects.get(cedula=cedula)
        return JsonResponse({
            'success': True,
            'nombre': solicitante.nombre,
            'apellido': solicitante.apellido,
            'tipo_solicitud': solicitante.tipo_solicitud
        })
    except Solicitante.DoesNotExist:
        return JsonResponse({'success': False})
    
def actualizar_estado(request):
    if request.method == "POST":
        propiedad_id = request.POST.get('propiedad_id')
        estado = request.POST.get('valestado')

        if not propiedad_id or not estado:
            return JsonResponse({'success': False, 'message': 'Faltan datos requeridos: propiedad o estado.'}, status=400)

        propiedad = get_object_or_404(Propiedades, id=propiedad_id)
        propiedad.estado = estado

        # Si el estado es "atendido", generar el PDF con diseño tipo recibo
        if estado == "atendido":
            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=letter)

            # Cargar imagen de marca de agua
            watermark_url = "https://res.cloudinary.com/dream-music/image/upload/v1739489089/logo_sjexi3.jpg"
            watermark = ImageReader(watermark_url)

            # Dibujar la marca de agua en el fondo
            pdf.drawImage(watermark, 150, 200, width=300, height=300, mask='auto')

            # Encabezado del recibo
            pdf.setFont("Helvetica-Bold", 16)
            pdf.drawString(200, 750, "RECIBO DE ATENCIÓN")

            pdf.setFont("Helvetica", 10)
            pdf.drawString(400, 750, f"Fecha: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")

            # Línea separadora
            pdf.line(50, 740, 550, 740)

            # Información de la propiedad
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(50, 710, "Información de la Propiedad:")

            pdf.setFont("Helvetica", 10)
            pdf.drawString(50, 690, f"📌 Código Interno: {propiedad.codigo_interno or 'N/A'}")
            pdf.drawString(50, 670, f"🏠 Bien Inmueble: {propiedad.bien_inmueble}")
            pdf.drawString(50, 650, f"📍 Ubicación: {propiedad.ubicacion or 'N/A'}")
            pdf.drawString(50, 630, f"📏 Área: {propiedad.area or 'N/A'}")
            pdf.drawString(50, 610, f"🙍‍♂️ Solicitante: {propiedad.solicitante}")

            # Estado
            pdf.setFont("Helvetica-Bold", 12)
            pdf.drawString(50, 580, "✅ Estado de Atención: ATENDIDO")

            # Línea final
            pdf.line(50, 560, 550, 560)

            pdf.showPage()
            pdf.save()

            buffer.seek(0)
            propiedad.documento_pdf.save(f"recibo_atencion_{propiedad_id}.pdf", ContentFile(buffer.read()), save=False)

        propiedad.save()

        return JsonResponse({'success': True, 'message': 'Estado actualizado correctamente y PDF generado.'})

    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

def obtener_estado_propiedad(request):
    if request.method == "POST":
        propiedad_id = request.POST.get('propiedad_id')

        if not propiedad_id:
            return JsonResponse({'success': False, 'message': 'ID de propiedad no válido.'}, status=400)

        # Obtén la propiedad y su estado
        propiedad = get_object_or_404(Propiedades, id=propiedad_id)

        return JsonResponse({
            'success': True,
            'estado': propiedad.estado  # Devuelve el estado de la propiedad seleccionada
        })

    return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

@csrf_exempt
def subir_pdf(request, propiedad_id):
    try:
        propiedad = get_object_or_404(Propiedades, id=propiedad_id)

        if propiedad.estado != 'atendiendo':
            return JsonResponse({'error': '❌ Solo puedes subir un archivo cuando la propiedad está "Atendiendo".'}, status=400)

        if request.method == 'POST' and request.FILES.get('pdf_file'):
            pdf_file = request.FILES['pdf_file']

            if not pdf_file.name.endswith('.pdf'):
                return JsonResponse({'error': '⚠️ Solo se permiten archivos PDF.'}, status=400)

            propiedad.archivo_pdf = pdf_file
            propiedad.save()

            return JsonResponse({'success': True, 'pdf_url': propiedad.archivo_pdf.url})

        return JsonResponse({'error': '⚠️ No se detectó ningún archivo adjunto.'}, status=400)

    except Exception as e:
        
        return JsonResponse({'error': f'🚨 Error interno del servidor: {str(e)}'}, status=500)
