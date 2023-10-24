from rest_framework import serializers, exceptions
from garancija.models import Warranty, Shop
from user.models import User


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'


class EmployeeWithoutShopSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        attrs['username'] = attrs['email']
        attrs['user_type'] = 'employee'
        attrs['password'] = 'dummypassword'
        return super().validate(attrs)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'id']

    def create(self, validated_data):
        shop_id = (self.context['view'].kwargs['shop_id'])
        try:
            shop = Shop.objects.get(id=shop_id)
        except Shop.DoesNotExist:
            raise exceptions.NotFound
        validated_data['shop_id'] = shop.id
        return super().create(validated_data)

    def update(self, employee, validated_data):
        employee.first_name = validated_data.get('first_name', employee.first_name)
        employee.last_name = validated_data.get('last_name', employee.last_name)
        employee.phone_number = validated_data.get('phone_number', employee.phone_number)
        employee.email = validated_data.get('email', employee.email)

        employee.save()
        return employee

    def delete(self, employee):
        employee.delete()


class EmployeeSerializer(serializers.ModelSerializer):
    shop = ShopSerializer()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'shop', 'phone_number', 'id']


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
