import pytest
from garancija.models import Shop
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from user.models import User
from django.core.management import call_command
from django.contrib.auth.models import Group


client = APIClient()


@pytest.fixture
def load_groups():
    call_command("generate_roles")


@pytest.mark.django_db
def test_retrieve_shop(load_groups):
    admin = baker.make(User, is_superuser=True)
    shop = baker.make(Shop)

    url = reverse("shops-detail", args=[shop.id])
    client.force_authenticate(admin)
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data['id'] == shop.id
    assert data['name'] == shop.name
    assert data['email'] == shop.email
    assert data['address'] == shop.address


@pytest.mark.django_db
def test_retrieve_404(load_groups):
    admin = baker.make(User, is_superuser=True)
    shop_id = 111

    try:
        Shop.objects.get(id=shop_id)
        assert False, "object exists"
    except Shop.DoesNotExist:
        pass

    url = reverse("shops-detail", args=[shop_id])
    client.force_authenticate(admin)
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_list_shop(load_groups):
    admin = baker.make(User, is_superuser=True)
    num_of_shops = 50
    shop_ids = []
    for _ in range(num_of_shops):
        shop = baker.make(Shop)
        shop_ids.append(shop.id)

    url = reverse("shops-list")
    client.force_authenticate(admin)
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert set(shop_ids) == set([x['id'] for x in data])


@pytest.mark.django_db
def test_create_shop(load_groups):
    admin = baker.make(User, is_superuser=True)
    data = {
        "name": "shop1",
        "address": "jagodinska 1234",
        "email": "novi@email.com"
    }
    url = reverse("shops-list")
    client.force_authenticate(admin)
    response = client.post(url, data=data)

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
def test_edit_shop(load_groups):
    admin = baker.make(User, is_superuser=True)
    data = {
        "address": "changed adr",
        "email": "changed@email.com"
    }
    shop = baker.make(Shop)

    url = reverse("shops-detail", args=[shop.id])
    client.force_authenticate(admin)
    response = client.patch(url, data=data)
    r_data = response.json()

    assert r_data['id'] == shop.id
    assert r_data['address'] == data['address']
    assert r_data['email'] == data['email']


@pytest.mark.django_db
def test_delete_shop(load_groups):
    admin = baker.make(User, is_superuser=True)
    shop = baker.make(Shop)

    url = reverse("shops-detail", args=[shop.id])
    client.force_authenticate(admin)
    response = client.delete(url)

    assert response.status_code == 204
    assert client.get(url).status_code == 404


@pytest.mark.django_db
def test_employee_cant_list_shop(load_groups):
    for _ in range(10):
        baker.make(Shop)
    employee = baker.make(User, user_type='employee')
    employee.groups.add(Group.objects.get(name='employee'))

    url = reverse('shops-list')
    client.force_authenticate(employee)
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_employee_cant_retrieve_shop(load_groups):
    shop = baker.make(Shop)
    employee = baker.make(User, user_type='employee')
    employee.groups.add(Group.objects.get(name='employee'))

    url = reverse('shops-detail', args=[shop.id])
    client.force_authenticate(employee)
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_employee_cant_create_shop(load_groups):
    data = {
        "name": "shop1",
        "address": "jagodinska 1234",
        "email": "novi@email.com"
    }
    employee = baker.make(User, user_type='employee')
    employee.groups.add(Group.objects.get(name='employee'))

    url = reverse('shops-list')
    client.force_authenticate(employee)
    response = client.post(url, data=data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_employee_cant_edit_shop(load_groups):
    shop = baker.make(Shop)
    data = {
        "name": "shop1",
        "address": "jagodinska 1234",
        "email": "novi@email.com"
    }
    employee = baker.make(User, user_type='employee')
    employee.groups.add(Group.objects.get(name='employee'))

    url = reverse('shops-detail', args=[shop.id])
    client.force_authenticate(employee)
    response = client.put(url, data=data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_employee_cant_partial_edit_shop(load_groups):
    shop = baker.make(Shop)
    data = {
        "email": "novi@email.com"
    }
    employee = baker.make(User, user_type='employee')
    employee.groups.add(Group.objects.get(name='employee'))

    url = reverse('shops-detail', args=[shop.id])
    client.force_authenticate(employee)
    response = client.patch(url, data=data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_employee_cant_delete_shop(load_groups):
    shop = baker.make(Shop)
    employee = baker.make(User, user_type='employee')
    employee.groups.add(Group.objects.get(name='employee'))

    url = reverse('shops-detail', args=[shop.id])
    client.force_authenticate(employee)
    response = client.delete(url)

    assert response.status_code == 403
