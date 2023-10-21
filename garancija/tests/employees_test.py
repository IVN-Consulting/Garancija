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


@pytest.mark.django_db
def test_create_employee():
    shop = baker.make(Shop)
    data = {
        "name": "novi",
        "phone_number": "1234",
        "email": "novi@email.com",
    }
    url = reverse("employees-list", args=[shop.id])
    response = client.post(url, data=data)

    assert response.status_code == 201
    resp_data = response.json()

    assert data['name'] == resp_data['name']
    assert data['phone_number'] == resp_data['phone_number']
    assert data['email'] == resp_data['email']


@pytest.mark.django_db
def test_retrieve_employee():
    shop = baker.make(Shop)
    employee = baker.make(Employee, shop=shop)

    url = reverse("employees-detail", args=[shop.id, employee.id])
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()

    assert data['id'] == employee.id
    assert data['shop']['id'] == shop.id

@pytest.mark.django_db
def test_retrieve_non_existing_employee():
    shop = baker.make(Shop)

    url = reverse("employees-detail", args=[shop.id, '14'])
    response = client.get(url)

    assert response.status_code == 404


@pytest.mark.django_db
def test_update_employee():
    data = {
        "name": "new name",
        "phone_number": "1234",
        "email": "changed@email.com"
    }
    shop = baker.make(Shop)
    emp = baker.make(Employee, shop=shop)

    url = reverse("employees-detail", args=[shop.id, emp.id])
    response = client.put(url, data=data)

    assert response.status_code == 200
    r_data = response.json()

    assert r_data['id'] == emp.id
    assert r_data['name'] == data['name']
    assert r_data['phone_number'] == data['phone_number']
    assert r_data['email'] == data['email']


@pytest.mark.django_db
def test_partial_update_employee():
    data = {
        "phone_number": "1234",
        "email": "changed@email.com"
    }
    shop = baker.make(Shop)
    emp = baker.make(Employee, shop=shop)

    url = reverse("employees-detail", args=[shop.id, emp.id])
    response = client.patch(url, data=data)
    r_data = response.json()

    assert response.status_code == 200
    assert r_data['id'] == emp.id
    assert r_data['phone_number'] == data['phone_number']
    assert r_data['email'] == data['email']


@pytest.mark.django_db
def test_delete_employee():
    shop = baker.make(Shop)
    emp = baker.make(Employee, shop=shop)

    url = reverse("employees-detail", args=[shop.id, emp.id])
    response = client.delete(url)

    assert response.status_code == 204
    assert client.get(url).status_code == 404
