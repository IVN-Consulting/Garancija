from rest_framework import serializers
from garancija.models import Warranty, Employee, Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    shop = ShopSerializer()
    class Meta:
        model = Employee
        fields = '__all__'


class WarrantySerializer(serializers.ModelSerializer):
    salesperson = EmployeeSerializer()
    class Meta:
        model = Warranty
        fields = '__all__'

class ListShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name']


class CreateShopSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=256, required=True)
    address = serializers.CharField(max_length=256, required=True)
    email = serializers.EmailField(required=True)

class RetriveShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'email']
