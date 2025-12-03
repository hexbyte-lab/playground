from django.http import JsonResponse

from core.models import Drink
from core.serializers import DrinkSerializer


def drink_list(request):
    drinks = Drink.objects.all()
    serializer = DrinkSerializer(drinks, many=True)
    # return Response(serializer.data)
    return JsonResponse(serializer.data, safe=False)