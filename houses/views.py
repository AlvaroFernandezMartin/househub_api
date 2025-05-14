from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt

from .models import House
from serializers import HouseSerializer
@csrf_exempt
@require_GET
def houses_list(request):
    houses = House.objects.all()
    serializer = HouseSerializer(houses)
    
    return serializer.json_response()