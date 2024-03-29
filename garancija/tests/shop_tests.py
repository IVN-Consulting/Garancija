import pytest
from garancija.models import Shop
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework.reverse import reverse


client = APIClient()


@pytest.mark.django_db
def test_retrieve_shop():
    # Given
    shop = baker.make(Shop)

    # When
    url = reverse("shops-detail", args=[shop.id])
    response = client.get(url)

    # Then
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == shop.id
    assert data['name'] == shop.name
    assert data['email'] == shop.email
    assert data['address'] == shop.address


@pytest.mark.django_db
def test_retrieve_404():
    # Given
    shop_id = 111

    try:
        Shop.objects.get(id=shop_id)
        assert False, "object exists"
    except Shop.DoesNotExist:
        pass

    # When
    url = reverse("shops-detail", args=[shop_id])
    response = client.get(url)

    # Then
    assert response.status_code == 404


@pytest.mark.django_db
def test_list_shop():
    # Given
    num_of_shops = 50
    shop_ids = []
    for _ in range(num_of_shops):
        shop = baker.make(Shop)
        shop_ids.append(shop.id)

    # When
    url = reverse("shops-list")
    response = client.get(url)

    # Then
    assert response.status_code == 200
    data = response.json()
    assert set(shop_ids) == set([x['id'] for x in data])


@pytest.mark.django_db
def test_create_shop():
    data = {
        "name": "shop1",
        "address": "jagodinska 1234",
        "email": "novi@email.com"
    }
    url = reverse("shops-list")
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
def test_edit_shop():
    # Given
    data = {
        "address": "changed adr",
        "email": "changed@email.com"
    }
    shop = baker.make(Shop)
    # When
    url = reverse("shops-detail", args=[shop.id])
    response = client.patch(url, data=data)
    r_data = response.json()
    # Then
    assert r_data['id'] == shop.id
    assert r_data['address'] == data['address']
    assert r_data['email'] == data['email']


@pytest.mark.django_db
def test_delete_shop():
    # Given
    shop = baker.make(Shop)
    # When
    url = reverse("shops-detail", args=[shop.id])
    response_delete = client.delete(url)
    response_get_after_del = client.get(url)
    # Then
    assert response_delete.status_code == 204
    assert response_get_after_del.status_code == 404
