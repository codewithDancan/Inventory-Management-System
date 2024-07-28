from app.models import Vehicle
from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedModelSerializer,
    )

from app.models import Vehicle, VehicleModel, Engine, Seller


class EngineSerializer(ModelSerializer):
    class Meta:
        model = Engine
        fields = "__all__"

class VehicleSerializer(ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"

class VehicleModelSeerializer(ModelSerializer):
    class Meta:
        model = VehicleModel
        fields = "__all__"

class SellerSerializer(ModelSerializer):
    class Meta:
        model = Seller
        #fields = "__all__"
        exclude = ["groups", "user_permissions"]




