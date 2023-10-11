import pytest
from garancija.models import Shop, Employee
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework.reverse import reverse


client = APIClient()


@pytest.mark.django_db
def test_list_employees():
    shop = baker.make(Shop)
    employee = baker.make(Employee, shop=shop)
    employee2 = baker.make(Employee)

    url = reverse("employees-list", args=[shop.id])
    response = client.get(url)
    assert response.status_code == 200

    data = response.json()
    data_emp_id = [int(x['id']) for x in data]
    assert employee.id in data_emp_id
    assert employee2.id not in data_emp_id


@pytest.mark.django_db
def test_list_employees_for_non_existing_shop():
    url = reverse("employees-list", args=['14'])
    response = client.get(url)

    data = response.json()
    assert response.status_code == 404
    assert data['detail'] == 'Not found.'


@pytest.mark.django_db
def test_create_employee():
    payload = {
        'name': 'New name',
        'phone_number': '12345',
        'email': 'new@email.com',
    }
    shop = baker.make(Shop)

    url = reverse('employees-list', args=[shop.id])
    response = client.post(url, data=payload)

    assert response.status_code == 201, response.json()
    data = response.json()

    assert data['name'] == payload['name']
    assert data['phone_number'] == payload['phone_number']
    assert data['email'] == payload['email']


@pytest.mark.django_db
def test_retrieve_employee():
    shop = baker.make(Shop)
    employee = baker.make(Employee, shop=shop)

    url = reverse("employees-detail", args=[shop.id, employee.id])
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data['id'] == employee.id
    url2 = reverse("employees-detail", args=[shop.id, '15'])
    response2 = client.get(url2)
    assert response2.status_code == 404
    data2 = response2.json()
    assert data2['detail'] == 'Not found.'


@pytest.mark.django_db
def test_update_employee():
    payload = {
        'name': 'Changed name',
        'phone_number': '12345',
        'email': 'changed@email.com'
    }
    shop = baker.make(Shop)
    employee = baker.make(Employee, shop=shop)

    url = reverse('employees-detail', args=[shop.id, employee.id])
    response = client.put(url, data=payload)

    assert response.status_code == 200
    data = response.json()

    assert data['id'] == employee.id
    assert data['name'] == payload['name']
    assert data['phone_number'] == payload['phone_number']
    assert data['email'] == payload['email']


@pytest.mark.django_db
def test_partial_update_employee():
    payload = {
        'email': 'changed@email.com'
    }
    shop = baker.make(Shop)
    employee = baker.make(Employee, shop=shop)

    url = reverse('employees-detail', args=[shop.id, employee.id])
    response = client.patch(url, data=payload)

    assert response.status_code == 200
    data = response.json()

    assert data['id'] == employee.id
    assert data['name'] == employee.name
    assert data['phone_number'] == employee.phone_number
    assert data['email'] == payload['email']


@pytest.mark.django_db
def test_delete_employee():
    shop = baker.make(Shop)
    employee = baker.make(Employee, shop=shop)

    url = reverse("employees-detail", args=[shop.id, employee.id])
    response = client.delete(url)

    assert response.status_code == 204
    assert client.get(url).status_code == 404
