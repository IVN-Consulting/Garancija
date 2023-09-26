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

    def create(self, validated_data):
        shop_data = validated_data.pop('shop')
        shop = Shop.objects.get(**shop_data)
        employee = Employee.objects.create(shop=shop, **validated_data)
        return employee

    def update(self, employee, validated_data):
        shop_data = validated_data.pop('shop')
        shop = Shop.objects.get(**shop_data)

        employee.name = validated_data.get('name', employee.name)
        employee.phone_number = validated_data.get('phone_number', employee.phone_number)
        employee.email = validated_data.get('email', employee.email)
        employee.shop = shop

        employee.save()
        return employee

    def delete(self, employee):
        employee.delete()

class WarrantySerializer(serializers.ModelSerializer):
    salesperson = EmployeeSerializer()
    class Meta:
        model = Warranty
        fields = '__all__'


