from rest_framework import serializers
from dukan.models import Catagory,Product,Cart,Favourite
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'
class CatagorySerializers(serializers.ModelSerializer):
    class Meta:
        model=Catagory
        fields='__all__'


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields='__all__'

class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model=Favourite
        fields='__all__'