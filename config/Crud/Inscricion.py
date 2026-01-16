from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from ..models import Inscrito

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
def create_inscrito(request):
    data = request.data

    nombre = data.get('nombre', '').strip().title()
    paterno = data.get('paterno', '').strip().title()
    materno = data.get('materno', '').strip().title()
    edad = data.get('edad')
    genero = data.get('genero', '').strip().title()
    iglesia = data.get('iglesia')

    pagoTelefono = data.get('telefono')
    pagoFecha = data.get('pagoFecha')
    pagoHora = data.get('pagoHora')
    pagoComprobante = data.get('pagoComprobante')  # Restored missing variable

    if not nombre or not paterno or not materno or not edad or not genero or not iglesia:
        return Response({'error': 'Todos los campos son obligatorios'}, status=400)

    if pagoComprobante and not pagoTelefono:
        return Response({'error': 'Teléfono obligatorio si hay pago'}, status=400)

    existe = Inscrito.objects.filter(
        nombre=nombre,
        paterno=paterno,
        materno=materno,
        edad=edad
    ).exists()

    if existe:
        return Response({'error': 'Inscrito duplicado'}, status=400)

    try:
        inscrito = Inscrito.objects.create(
            nombre=nombre,
            paterno=paterno,
            materno=materno,
            edad=edad,
            genero=genero,
            iglesia_id=iglesia,
            pagoTelefono=pagoTelefono,
            pagoFecha=pagoFecha,
            pagoHora=pagoHora,
            pagoComprobante=pagoComprobante
        )

        return Response({
            'id': inscrito.id,
            'nombre': inscrito.nombre,
            'paterno': inscrito.paterno,
            'materno': inscrito.materno,
            'edad': inscrito.edad,
            'genero': inscrito.genero,
            'pagoTelefono': inscrito.pagoTelefono,
            'pagoFecha': inscrito.pagoFecha,
            'pagoHora': inscrito.pagoHora,
            'pagoComprobante': inscrito.pagoComprobante,
            'verificado': inscrito.verificado,
            'iglesia': inscrito.iglesia.nombre
        }, status=201)
    except Exception as e:
        return Response({'error': str(e)}, status=500)

@api_view(['GET'])
def list_inscritos(request):
    inscritos = Inscrito.objects.select_related('iglesia').values(
        'id',
        'nombre',
        'paterno',
        'materno',
        'edad',
        'genero',
        'pagoTelefono',
        'pagoFecha',
        'pagoHora',
        'pagoComprobante',
        'verificado',
        'iglesia__id',
        'iglesia__nombre'
    )
    return Response(inscritos, status=status.HTTP_200_OK)

@api_view(['GET'])
def cupo_inscritos(request):
    cupo = Inscrito.objects.count()
    return Response(cupo, status=status.HTTP_200_OK)

@api_view(['POST'])
def confirmar_inscrito(request):
    Inscrito.objects.filter(id=request.data.get('id')).update(verificado=True)
    return Response(status=status.HTTP_200_OK)
