from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_http_methods
from django.views.decorators.csrf import csrf_exempt
from .models import House
from .serializers import HouseSerializer
from users.decorators import auth_required
import cloudinary.uploader

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
@auth_required
def houses_delete(request, house_id):
    try:
        house = House.objects.get(id=house_id)

        if house.image_public_id:
            cloudinary.uploader.destroy(house.image_public_id)

        house.delete()
        return JsonResponse({"message": "House deleted successfully."}, status=200)

    except House.DoesNotExist:
        return JsonResponse({"error": "House not found."}, status=404)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@csrf_exempt
@require_http_methods(["POST"])
@auth_required
def houses_create(request):
    try:
        uploaded_image = request.FILES.get("image")
        image_url = None
        if uploaded_image:
            import cloudinary.uploader
            upload_result = cloudinary.uploader.upload(uploaded_image)
            image_url = upload_result.get("secure_url")
            image_public_id = upload_result.get("public_id")


        price = request.POST.get("price")
        bedrooms = request.POST.get("bedrooms")
        bathrooms = request.POST.get("bathrooms")
        size = request.POST.get("size")
        description = request.POST.get("description")
        street = request.POST.get("streetName")
        house_number = request.POST.get("houseNumber")
        house_number_addition = request.POST.get("numberAddition")
        city = request.POST.get("city")
        zip_code = request.POST.get("zip")
        construction_year = request.POST.get("constructionYear")
        has_garage = request.POST.get("hasGarage")

        required_fields = [price, bedrooms, bathrooms, size, description,
                           street, house_number, city, zip_code, construction_year, has_garage]
        missing = [field for field in required_fields if field in [None, ""]]
        if missing:
            return JsonResponse({"error": "Missing required fields."}, status=400)

        house = House.objects.create(
            user=request.user,
            image=image_url,
            image_public_id=image_public_id,
            price=price,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            size=size,
            description=description,
            street=street,
            house_number=house_number,
            house_number_addition=house_number_addition,
            city=city,
            zip_code=zip_code,
            construction_year=construction_year,
            has_garage=has_garage.lower() == "true",
        )

        serializer = HouseSerializer(house, request=request)
        return serializer.json_response()

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
@auth_required
def house_update(request, house_id):
    try:
        house = House.objects.get(id=house_id)

        if not request.user.is_superuser and house.user != request.user:
            return JsonResponse({"error": "Permission denied."}, status=403)

    except House.DoesNotExist:
        return JsonResponse({"error": "House not found."}, status=404)

    try:
        uploaded_image = request.FILES.get("image")
        if uploaded_image:
            import cloudinary.uploader
            upload_result = cloudinary.uploader.upload(uploaded_image)
            house.image = upload_result.get("secure_url")

        price = request.POST.get("price")
        bedrooms = request.POST.get("bedrooms")
        bathrooms = request.POST.get("bathrooms")
        size = request.POST.get("size")
        description = request.POST.get("description")
        street = request.POST.get("streetName")
        house_number = request.POST.get("houseNumber")
        house_number_addition = request.POST.get("numberAddition")
        city = request.POST.get("city")
        zip_code = request.POST.get("zip")
        construction_year = request.POST.get("constructionYear")
        has_garage = request.POST.get("hasGarage")

        required_fields = [price, bedrooms, bathrooms, size, description,
                           street, house_number, city, zip_code, construction_year, has_garage]
        if any(f in [None, ""] for f in required_fields):
            return JsonResponse({"error": "Missing required fields."}, status=400)

        house.price = price
        house.bedrooms = bedrooms
        house.bathrooms = bathrooms
        house.size = size
        house.description = description
        house.street = street
        house.house_number = house_number
        house.house_number_addition = house_number_addition or house.house_number_addition
        house.city = city
        house.zip_code = zip_code
        house.construction_year = construction_year
        house.has_garage = has_garage.lower() == "true"

        house.save()

        serializer = HouseSerializer(house, request=request)
        return serializer.json_response()

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



