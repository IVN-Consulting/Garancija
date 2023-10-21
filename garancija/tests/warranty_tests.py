import pytest
from garancija.models import Warranty, Employee
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from model_bakery import baker


client = APIClient()


@pytest.mark.django_db
def test_list_warranties():
    num_of_warranties = 10
    warranty_ids = []
    for _ in range(num_of_warranties):
        warranty = baker.make(Warranty)
        warranty_ids.append(warranty.id)

    url = reverse('warranty-list')
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()

    assert set(warranty_ids) == set([x['id'] for x in data])


@pytest.mark.django_db
def test_retrieve_warranty():
    warranty = baker.make(Warranty)

    url = reverse('warranty-detail', args=[warranty.id])
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()

    assert data['id'] == warranty.id
    assert data['product_name'] == warranty.product_name


@pytest.mark.django_db
def test_retrieve_warranty_404():
    url = reverse('warranty-detail', args=['14'])
    response = client.get(url)
    data = response.json()

    assert response.status_code == 404
    assert data['detail'] == 'Not found.'


@pytest.mark.django_db
def test_create_warranty():
    salesperson = baker.make(Employee)
    data = {
        'salesperson': salesperson.id,
        'product_name': 'Test Product',
        'start_date': '2023-10-11',
        'end_date': '2024-02-15'
    }
    url = reverse("warranty-list")
    response = client.post(url, data=data)

    assert response.status_code == 201
    resp_data = response.json()

    assert data['salesperson'] == salesperson.id
    assert data['product_name'] == resp_data['product_name']
    assert data['start_date'] == resp_data['start_date']
    assert data['end_date'] == resp_data['end_date']


@pytest.mark.django_db
def test_delete_warranty():
    warranty = baker.make(Warranty)

    url = reverse('warranty-detail', args=[warranty.id])
    response = client.delete(url)

    assert response.status_code == 204
    assert client.get(url).status_code == 404


@pytest.mark.django_db
def test_update_warranty():
    warranty = baker.make(Warranty)
    data = {
        'product_name': 'Test product',
        'start_date': '2023-10-11',
        'end_date': '2026-02-15'
    }

    url = reverse('warranty-detail', args=[warranty.id])
    response = client.put(url, data=data)

    assert response.status_code == 200
    resp_data = response.json()

    assert resp_data['id'] == warranty.id
    assert resp_data['product_name'] == data['product_name']
    assert resp_data['start_date'] == data['start_date']
    assert resp_data['end_date'] == data['end_date']


@pytest.mark.django_db
def test_partial_update_warranty():
    warranty = baker.make(Warranty)
    data = {
        'product_name': 'Changed prod name',
        'end_date': '2028-11-11'
    }

    url = reverse('warranty-detail', args=[warranty.id])
    response = client.patch(url, data=data)

    assert response.status_code == 200
    resp_data = response.json()

    assert resp_data['id'] == warranty.id
    assert resp_data['product_name'] == data['product_name']
    assert resp_data['start_date'] == str(warranty.start_date)
    assert resp_data['end_date'] == data['end_date']
