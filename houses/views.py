from django.views.decorators.http import require_GET, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponseNotFound
from django.core.exceptions import ValidationError
from .models import House
from .serializers import HouseSerializer
import json


@csrf_exempt
@require_GET
def houses_list(request):
    try:
        houses = House.objects.all()
        serializer = HouseSerializer(houses, request=request)

        return serializer.json_response()
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_GET
def houses_detail(request, house_id):
    try:
        house = House.objects.get(id=house_id)
        serializer = HouseSerializer(house, request=request)

        return serializer.json_response()
    except House.DoesNotExist:
        return JsonResponse({"error": "House not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def houses_delete(request, house_id):
    try:
        house = House.objects.get(id=house_id)
        house.delete()
        return JsonResponse({"message": "House deleted successfully."}, status=200)
    except House.DoesNotExist:
        return JsonResponse({"error": "House not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def houses_create(request):
    try:
        data = json.loads(request.body)

        required_fields = [
            "price", "bedrooms", "bathrooms", "size", "description", "streetName",
            "houseNumber", "city", "zip", "constructionYear", "hasGarage"
        ]
        missing = [f for f in required_fields if f not in data or data[f] in [None, ""]]
        if missing:
            return JsonResponse({"error": "Missing required fields.", "missing": missing}, status=400)

        house = House.objects.create(
            price=data["price"],
            bedrooms=data["bedrooms"],
            bathrooms=data["bathrooms"],
            size=data["size"],
            description=data["description"],
            street=data["streetName"],
            house_number=data["houseNumber"],
            house_number_addition=data.get("numberAddition"),
            city=data["city"],
            zip_code=data["zip"],
            construction_year=data["constructionYear"],
            has_garage=data["hasGarage"],
            image=None  # Se sube por separado
        )

        serializer = HouseSerializer(house)
        return serializer.json_response()

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def house_update(request, house_id):
    try:
        house = House.objects.get(id=house_id)
    except House.DoesNotExist:
        return JsonResponse({"error": "House not found."}, status=404)

    try:
        data = json.loads(request.body)

        required_fields = [
            "price", "bedrooms", "bathrooms", "size", "description", "streetName",
            "houseNumber", "city", "zip", "constructionYear", "hasGarage"
        ]
        missing = [f for f in required_fields if f not in data or data[f] in [None, ""]]
        if missing:
            return JsonResponse({"error": "Missing required fields.", "missing": missing}, status=400)

        house.price = data["price"]
        house.bedrooms = data["bedrooms"]
        house.bathrooms = data["bathrooms"]
        house.size = data["size"]
        house.description = data["description"]
        house.street = data["streetName"]
        house.house_number = data["houseNumber"]
        house.house_number_addition = data.get("numberAddition")
        house.city = data["city"]
        house.zip_code = data["zip"]
        house.construction_year = data["constructionYear"]
        house.has_garage = data["hasGarage"]

        house.save()

        serializer = HouseSerializer(house)
        return serializer.json_response()

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def upload_image(request, house_id):
    try:
        house = House.objects.get(id=house_id)
    except House.DoesNotExist:
        return JsonResponse({"error": "House not found."}, status=404)

    image = request.FILES.get("image")
    if not image:
        return JsonResponse({"error": "No image file provided."}, status=400)

    house.image = image
    house.save()

    return JsonResponse({"message": "Image uploaded successfully."})
