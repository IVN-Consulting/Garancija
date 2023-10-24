from rest_framework import serializers, exceptions
from garancija.models import Warranty, Employee, Shop


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class EmployeeWithoutShopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employee
        exclude = ['shop']

    def create(self, validated_data):
        shop_id = (self.context['view'].kwargs['shop_id'])
        try:
            shop = Shop.objects.get(id=shop_id)
        except Shop.DoesNotExist:
            raise exceptions.NotFound

        employee = Employee.objects.create(shop=shop, **validated_data)
        return employee

    def update(self, employee, validated_data):
        employee.name = validated_data.get('name', employee.name)
        employee.phone_number = validated_data.get('phone_number', employee.phone_number)
        employee.email = validated_data.get('email', employee.email)

        employee.save()
        return employee

    def delete(self, employee):
        employee.delete()


class EmployeeSerializer(serializers.ModelSerializer):
    shop = ShopSerializer()

    class Meta:
        model = Employee
        fields = '__all__'


class CreateUpdateWarrantySerializer(serializers.ModelSerializer):

    class Meta:
        model = Warranty
        fields = '__all__'


class ListWarrantySerializer(serializers.ModelSerializer):
    class Meta:
        model = Warranty
        fields = '__all__'
        depth = 1


class PartialUpdateWarrantySerializer(serializers.ModelSerializer):
    class Meta:
        model = Warranty
        fields = ['start_date', 'end_date']
