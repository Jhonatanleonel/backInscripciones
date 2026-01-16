from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Iglesia


@api_view(['POST'])
def create_iglesia(request):
    nombre = request.data.get('nombre')

    # 1️⃣ Validar vacío
    if not nombre or nombre.strip() == '':
        return Response(
            {'error': 'El nombre es obligatorio'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 2️⃣ Normalizar (Mayúscula cada palabra)
    nombre_normalizado = nombre.title().strip()

    # 3️⃣ Verificar duplicado (sin importar mayúsculas)
    if Iglesia.objects.filter(nombre__iexact=nombre_normalizado).exists():
        return Response(
            {'error': 'La iglesia ya está registrada'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 4️⃣ Crear
    nueva_iglesia = Iglesia.objects.create(nombre=nombre_normalizado)
    
    # 5️⃣ Devolver datos de la iglesia creada
    return Response({
        'id': nueva_iglesia.id,
        'nombre': nueva_iglesia.nombre
    }, status=status.HTTP_201_CREATED)

    
@api_view(['GET'])
def list_iglesias(request):
    iglesias = Iglesia.objects.all()
    return Response(iglesias.values(), status=status.HTTP_200_OK)

@api_view(['DELETE'])
def delete_iglesia(request, id):
    try:
        iglesia = Iglesia.objects.get(id=id)
        iglesia.delete()
        return Response({'message': 'Iglesia eliminada correctamente'}, status=status.HTTP_200_OK)
    except Iglesia.DoesNotExist:
        return Response({'error': 'Iglesia no encontrada'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_iglesia(request, id):
    try:
        iglesia = Iglesia.objects.get(id=id)
        nombre = request.data.get('nombre')
        if nombre:
            iglesia.nombre = nombre.title().strip()
            iglesia.save()
        return Response({'message': 'Iglesia actualizada correctamente'}, status=status.HTTP_200_OK)
    except Iglesia.DoesNotExist:
        return Response({'error': 'Iglesia no encontrada'}, status=status.HTTP_404_NOT_FOUND)
