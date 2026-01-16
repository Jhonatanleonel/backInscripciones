from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count, Avg, Min, Max
from ..models import Inscrito, Iglesia


@api_view(['GET'])
def reporte_general(request):
    # 🔹 Totales
    total_inscritos = Inscrito.objects.count()
    total_mujeres = Inscrito.objects.filter(genero='F').count()
    total_hombres = Inscrito.objects.filter(genero='M').count()

    # 🔹 Estadísticas de edad
    edades_stats = Inscrito.objects.aggregate(
        edad_min=Min('edad'),
        edad_max=Max('edad'),
        edad_promedio=Avg('edad')
    )

    # 🔹 Conteo por edades
    edades = (
        Inscrito.objects
        .values('edad')
        .annotate(total=Count('id'))
        .order_by('edad')
    )

    # 🔹 Iglesias con cantidad de inscritos
    iglesias = (
        Iglesia.objects
        .annotate(total=Count('inscrito'))
        .values('nombre', 'total')
        .order_by('-total')
    )

    return Response({
        'totales': {
            'inscritos': total_inscritos,
            'mujeres': total_mujeres,
            'hombres': total_hombres,
        },
        'edades_stats': edades_stats,
        'edades': edades,
        'iglesias': iglesias
    })
