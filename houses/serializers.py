from shared.serializers import BaseSerializer

class HouseSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.pk,
            'image': instance.image.url if instance.image else None,
            'price': float(instance.price),
            'rooms': {
                'bedrooms': instance.bedrooms,
                'bathrooms': instance.bathrooms
            },
            'size': instance.size,
            'description': instance.description,
            'location': {
                'street': instance.street,
                'houseNumber': instance.house_number,
                'houseNumberAddition': instance.house_number_addition,
                'city': instance.city,
                'zip': instance.zip_code,
            },
            'createdAt': instance.created_at.isoformat(),
            'constructionYear': instance.construction_year,
            'hasGarage': instance.has_garage,
        }
