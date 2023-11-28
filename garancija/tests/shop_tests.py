import pytest
from garancija.models import Shop
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from django.core.management import call_command
from django.contrib.auth.models import Group
from user.models import User


client = APIClient()


@pytest.fixture
def load_groups():
    call_command("generate_roles")


@pytest.mark.django_db
def test_retrieve_shop_admin(load_groups):
    # Given
    shop = baker.make(Shop)
    admin = baker.make(User, is_superuser=True)
    # When
    url = reverse("shops-detail", args=[shop.id])
    client.force_authenticate(admin)
    response = client.get(url)

    # Then
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == shop.id
    assert data['name'] == shop.name
    assert data['email'] == shop.email
    assert data['address'] == shop.address


@pytest.mark.django_db
def test_retrieve_404_admin(load_groups):
    # Given
    shop_id = 111
    admin = baker.make(User, is_superuser=True)
    try:
        Shop.objects.get(id=shop_id)
        assert False, "object exists"
    except Shop.DoesNotExist:
        pass

    # When
    url = reverse("shops-detail", args=[shop_id])
    client.force_authenticate(admin)
    response = client.get(url)

    # Then
    assert response.status_code == 404


@pytest.mark.django_db
def test_list_shop_admin(load_groups):
    # Given
    admin = baker.make(User, is_superuser=True)
    num_of_shops = 50
    shop_ids = []
    for _ in range(num_of_shops):
        shop = baker.make(Shop)
        shop_ids.append(shop.id)

    # When
    url = reverse("shops-list")
    client.force_authenticate(admin)
    response = client.get(url)

    # Then
    assert response.status_code == 200
    data = response.json()
    assert set(shop_ids) == set([x['id'] for x in data])


@pytest.mark.django_db
def test_create_shop_admin(load_groups):
    admin = baker.make(User, is_superuser=True)
    data = {
        "name": "shop1",
        "address": "jagodinska 1234",
        "email": "novi@email.com"
    }
    url = reverse("shops-list")
    client.force_authenticate(admin)
    response = client.post(url, data=data)

    # Then
    assert response.status_code == 201, response.json()
    resp_data = response.json()

    assert data['name'] == resp_data['name']
    assert data['address'] == resp_data['address']
    assert data['email'] == resp_data['email']

    shop_id = resp_data['id']

    shop = Shop.objects.get(id=shop_id)
    assert data['name'] == shop.name
    assert data['address'] == shop.address
    assert data['email'] == shop.email


@pytest.mark.django_db
def test_edit_shop_admin(load_groups):
    # Given
    admin = baker.make(User, is_superuser=True)
    data = {
        "address": "changed adr",
        "email": "changed@email.com"
    }
    shop = baker.make(Shop)
    # When
    url = reverse("shops-detail", args=[shop.id])
    client.force_authenticate(admin)
    response = client.patch(url, data=data)
    r_data = response.json()
    # Then
    assert r_data['id'] == shop.id
    assert r_data['address'] == data['address']
    assert r_data['email'] == data['email']


@pytest.mark.django_db
def test_delete_shop_admin(load_groups):
    # Given
    admin = baker.make(User, is_superuser=True)
    shop = baker.make(Shop)
    # When
    url = reverse("shops-detail", args=[shop.id])
    client.force_authenticate(admin)
    response_delete = client.delete(url)
    response_get_after_del = client.get(url)
    # Then
    assert response_delete.status_code == 204
    assert response_get_after_del.status_code == 404


@pytest.mark.django_db
def test_retrieve_shop_employee(load_groups):
    # Given
    shop = baker.make(Shop)
    emp = baker.make(User, user_type="employee")
    emp.groups.add(Group.objects.get(name='employee'))

    # When
    url = reverse("shops-detail", args=[shop.id])
    client.force_authenticate(emp)
    response = client.get(url)

    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_retrieve_404_employee(load_groups):
    # Given
    shop_id = 111
    emp = baker.make(User, user_type="employee")
    emp.groups.add(Group.objects.get(name='employee'))
    try:
        Shop.objects.get(id=shop_id)
        assert False, "object exists"
    except Shop.DoesNotExist:
        pass

    # When
    url = reverse("shops-detail", args=[shop_id])
    client.force_authenticate(emp)
    response = client.get(url)

    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_list_shop_employee(load_groups):
    # Given
    emp = baker.make(User, user_type="employee")
    emp.groups.add(Group.objects.get(name='employee'))
    num_of_shops = 50
    shop_ids = []
    for _ in range(num_of_shops):
        shop = baker.make(Shop)
        shop_ids.append(shop.id)

    # When
    url = reverse("shops-list")
    client.force_authenticate(emp)
    response = client.get(url)

    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_shop_employee(load_groups):
    emp = baker.make(User, user_type="employee")
    emp.groups.add(Group.objects.get(name='employee'))
    data = {
        "name": "shop1",
        "address": "jagodinska 1234",
        "email": "novi@email.com"
    }
    url = reverse("shops-list")
    client.force_authenticate(emp)
    response = client.post(url, data=data)

    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_shop_employee(load_groups):
    # Given
    emp = baker.make(User, user_type="employee")
    emp.groups.add(Group.objects.get(name='employee'))
    data = {
        "address": "changed adr",
        "email": "changed@email.com"
    }
    shop = baker.make(Shop)
    # When
    url = reverse("shops-detail", args=[shop.id])
    client.force_authenticate(emp)
    response = client.patch(url, data=data)
    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_shop_employee(load_groups):
    # Given
    emp = baker.make(User, user_type="employee")
    emp.groups.add(Group.objects.get(name='employee'))
    shop = baker.make(Shop)
    # When
    url = reverse("shops-detail", args=[shop.id])
    client.force_authenticate(emp)
    response_delete = client.delete(url)
    # Then
    assert response_delete.status_code == 403


@pytest.mark.django_db
def test_retrieve_shop_customer(load_groups):
    # Given
    shop = baker.make(Shop)
    cus = baker.make(User, user_type="customer")
    cus.groups.add(Group.objects.get(name='customer'))

    # When
    url = reverse("shops-detail", args=[shop.id])
    client.force_authenticate(cus)
    response = client.get(url)

    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_retrieve_404_customer(load_groups):
    # Given
    shop_id = 111
    cus = baker.make(User, user_type="customer")
    cus.groups.add(Group.objects.get(name='customer'))
    try:
        Shop.objects.get(id=shop_id)
        assert False, "object exists"
    except Shop.DoesNotExist:
        pass

    # When
    url = reverse("shops-detail", args=[shop_id])
    client.force_authenticate(cus)
    response = client.get(url)

    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_list_shop_customer(load_groups):
    # Given
    cus = baker.make(User, user_type="customer")
    cus.groups.add(Group.objects.get(name='customer'))
    num_of_shops = 50
    shop_ids = []
    for _ in range(num_of_shops):
        shop = baker.make(Shop)
        shop_ids.append(shop.id)

    # When
    url = reverse("shops-list")
    client.force_authenticate(cus)
    response = client.get(url)

    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_shop_customer(load_groups):
    cus = baker.make(User, user_type="customer")
    cus.groups.add(Group.objects.get(name='customer'))
    data = {
        "name": "shop1",
        "address": "jagodinska 1234",
        "email": "novi@email.com"
    }
    url = reverse("shops-list")
    client.force_authenticate(cus)
    response = client.post(url, data=data)

    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_edit_shop_customer(load_groups):
    # Given
    cus = baker.make(User, user_type="customer")
    cus.groups.add(Group.objects.get(name='customer'))
    data = {
        "address": "changed adr",
        "email": "changed@email.com"
    }
    shop = baker.make(Shop)
    # When
    url = reverse("shops-detail", args=[shop.id])
    client.force_authenticate(cus)
    response = client.patch(url, data=data)
    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_shop_customer(load_groups):
    # Given
    cus = baker.make(User, user_type="customer")
    cus.groups.add(Group.objects.get(name='customer'))
    shop = baker.make(Shop)
    # When
    url = reverse("shops-detail", args=[shop.id])
    client.force_authenticate(cus)
    response_delete = client.delete(url)
    # Then
    assert response_delete.status_code == 403