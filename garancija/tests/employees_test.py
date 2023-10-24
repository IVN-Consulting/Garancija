import pytest
from garancija.models import Shop
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from user.models import User


client = APIClient()


@pytest.mark.django_db
def test_list_employees():
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee2 = baker.make(User, user_type="employee")

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
    shop = baker.make(Shop)
    data = {
        "first_name": "novi",
        "last_name": "god",
        "phone_number": "1234",
        "email": "novi@email.com",
    }
    url = reverse("employees-list", args=[shop.id])
    response = client.post(url, data=data)

    # Then
    assert response.status_code == 201, response.json()
    resp_data = response.json()

    assert data['first_name'] == resp_data['first_name']
    assert data['last_name'] == resp_data['last_name']
    assert data['phone_number'] == resp_data['phone_number']
    assert data['email'] == resp_data['email']
    employee = User.objects.get(id=resp_data['id'])
    assert employee.shop == shop


@pytest.mark.django_db
def test_retrieve_employee():
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)

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
    # Given
    data = {
        "first_name": "new name",
        "last_name": "stagod",
        "phone_number": "1234",
        "email": "changed@email.com"
    }
    shop = baker.make(Shop)
    emp = baker.make(User, user_type="employee", shop=shop)
    # When
    url = reverse("employees-detail", args=[shop.id, emp.id])
    response = client.patch(url, data=data)
    r_data = response.json()
    # Then
    assert response.status_code == 200
    assert r_data['id'] == emp.id
    assert r_data['first_name'] == data['first_name']
    assert r_data['last_name'] == data['last_name']
    assert r_data['phone_number'] == data['phone_number']
    assert r_data['email'] == data['email']


@pytest.mark.django_db
def test_partial_update_employee():
    # Given
    data = {
        "phone_number": "1234",
        "email": "changed@email.com"
    }
    shop = baker.make(Shop)
    emp = baker.make(User, user_type="employee", shop=shop)
    # When
    url = reverse("employees-detail", args=[shop.id, emp.id])
    response = client.patch(url, data=data)
    r_data = response.json()
    # Then
    assert response.status_code == 200
    assert r_data['id'] == emp.id
    assert r_data['phone_number'] == data['phone_number']
    assert r_data['email'] == data['email']


@pytest.mark.django_db
def test_delete_employee():
    # Given
    shop = baker.make(Shop)
    emp = baker.make(User, user_type="employee", shop=shop)
    # When
    url = reverse("employees-detail", args=[shop.id, emp.id])
    response_delete = client.delete(url)
    response_get_after_del = client.get(url)
    # Then
    assert response_delete.status_code == 204
    assert response_get_after_del.status_code == 404
