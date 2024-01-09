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
def test_list_employees_admin(load_groups):
    admin = baker.make(User, is_superuser=True)
    shop = baker.make(Shop)
    shop2 = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee2 = baker.make(User, user_type="employee", shop=shop2)

    url = reverse("employees-list", args=[shop.id])
    client.force_authenticate(admin)
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    data_emp_id = [int(x['id']) for x in data]
    assert employee.id in data_emp_id
    assert employee2.id not in data_emp_id

    url = reverse("employees-list", args=[shop2.id])
    client.force_authenticate(admin)
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    data_emp_id = [int(x['id']) for x in data]
    assert employee2.id in data_emp_id
    assert employee.id not in data_emp_id


@pytest.mark.django_db
def test_list_employees_for_non_existing_shop_admin(load_groups):
    admin = baker.make(User, is_superuser=True)
    url = reverse("employees-list", args=['14'])
    client.force_authenticate(admin)
    response = client.get(url)

    data = response.json()
    assert response.status_code == 404
    assert data['detail'] == 'Not found.'


@pytest.mark.django_db
def test_create_employee_admin(load_groups):
    admin = baker.make(User, is_superuser=True)
    shop = baker.make(Shop)
    data = {
        "first_name": "novi",
        "last_name": "god",
        "phone_number": "1234",
        "email": "novi@email.com"
    }
    url = reverse("employees-list", args=[shop.id])
    client.force_authenticate(admin)
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
def test_retrieve_employee_admin(load_groups):
    admin = baker.make(User, is_superuser=True)
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)

    url = reverse("employees-detail", args=[shop.id, employee.id])
    client.force_authenticate(admin)
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
def test_update_employee_admin(load_groups):
    # Given
    admin = baker.make(User, is_superuser=True)
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
    client.force_authenticate(admin)
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
def test_partial_update_employee_admin(load_groups):
    # Given
    admin = baker.make(User, is_superuser=True)
    data = {
        "phone_number": "1234",
        "email": "changed@email.com"
    }
    shop = baker.make(Shop)
    emp = baker.make(User, user_type="employee", shop=shop)
    # When
    url = reverse("employees-detail", args=[shop.id, emp.id])
    client.force_authenticate(admin)
    response = client.patch(url, data=data)
    r_data = response.json()
    # Then
    assert response.status_code == 200
    assert r_data['id'] == emp.id
    assert r_data['phone_number'] == data['phone_number']
    assert r_data['email'] == data['email']


@pytest.mark.django_db
def test_delete_employee_admin(load_groups):
    # Given
    admin = baker.make(User, is_superuser=True)
    shop = baker.make(Shop)
    emp = baker.make(User, user_type="employee", shop=shop)
    # When
    url = reverse("employees-detail", args=[shop.id, emp.id])
    client.force_authenticate(admin)
    response_delete = client.delete(url)
    response_get_after_del = client.get(url)
    # Then
    assert response_delete.status_code == 204
    assert response_get_after_del.status_code == 404


@pytest.mark.django_db
def test_list_employees_employee(load_groups):
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee.groups.add(Group.objects.get(name='employee'))
    employee2 = baker.make(User, user_type="employee")

    url = reverse("employees-list", args=[shop.id])
    client.force_authenticate(employee)
    response = client.get(url)
    assert response.status_code == 200

    data = response.json()
    data_emp_id = [int(x['id']) for x in data]
    assert employee.id in data_emp_id
    assert employee2.id not in data_emp_id


@pytest.mark.django_db
def test_list_employees_for_non_existing_shop_employee(load_groups):
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee.groups.add(Group.objects.get(name='employee'))
    url = reverse("employees-list", args=['14'])
    client.force_authenticate(employee)
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_create_employee_employee(load_groups):
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee.groups.add(Group.objects.get(name='employee'))
    data = {
        "first_name": "novi",
        "last_name": "god",
        "phone_number": "1234",
        "email": "novi@email.com"
    }
    url = reverse("employees-list", args=[shop.id])
    client.force_authenticate(employee)
    response = client.post(url, data=data)

    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_retrieve_employee_employee(load_groups):
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee.groups.add(Group.objects.get(name='employee'))
    url = reverse("employees-detail", args=[shop.id, employee.id])
    client.force_authenticate(employee)
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
def test_update_employee_employee(load_groups):
    # Given
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee.groups.add(Group.objects.get(name='employee'))
    data = {
        "first_name": "new name",
        "last_name": "stagod",
        "phone_number": "1234",
        "email": "changed@email.com"
    }
    # When
    url = reverse("employees-detail", args=[shop.id, employee.id])
    client.force_authenticate(employee)
    response = client.patch(url, data=data)
    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_partial_update_employee_employee(load_groups):
    # Given
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee.groups.add(Group.objects.get(name='employee'))
    data = {
        "phone_number": "1234",
        "email": "changed@email.com"
    }
    # When
    url = reverse("employees-detail", args=[shop.id, employee.id])
    client.force_authenticate(employee)
    response = client.patch(url, data=data)
    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_employee_employee(load_groups):
    # Given
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee.groups.add(Group.objects.get(name='employee'))
    # When
    url = reverse("employees-detail", args=[shop.id, employee.id])
    client.force_authenticate(employee)
    response_delete = client.delete(url)
    # Then
    assert response_delete.status_code == 403


@pytest.mark.django_db
def test_list_employees_customer(load_groups):
    cus = baker.make(User, user_type='customer')
    cus.groups.add(Group.objects.get(name='customer'))
    shop = baker.make(Shop)

    url = reverse("employees-list", args=[shop.id])
    client.force_authenticate(cus)
    response = client.get(url)
    assert response.status_code == 403


@pytest.mark.django_db
def test_list_employees_for_non_existing_shop_customer(load_groups):
    cus = baker.make(User, user_type='customer')
    cus.groups.add(Group.objects.get(name='customer'))
    url = reverse("employees-list", args=['14'])
    client.force_authenticate(cus)
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_create_employee_customer(load_groups):
    shop = baker.make(Shop)
    cus = baker.make(User, user_type='customer')
    cus.groups.add(Group.objects.get(name='customer'))
    data = {
        "first_name": "novi",
        "last_name": "god",
        "phone_number": "1234",
        "email": "novi@email.com"
    }
    url = reverse("employees-list", args=[shop.id])
    client.force_authenticate(cus)
    response = client.post(url, data=data)

    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_retrieve_employee_customer(load_groups):
    cus = baker.make(User, user_type='customer')
    cus.groups.add(Group.objects.get(name='customer'))
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    url = reverse("employees-detail", args=[shop.id, employee.id])
    client.force_authenticate(cus)
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_update_employee_customer(load_groups):
    # Given
    cus = baker.make(User, user_type='customer')
    cus.groups.add(Group.objects.get(name='customer'))
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    data = {
        "first_name": "new name",
        "last_name": "stagod",
        "phone_number": "1234",
        "email": "changed@email.com"
    }
    # When
    url = reverse("employees-detail", args=[shop.id, employee.id])
    client.force_authenticate(cus)
    response = client.patch(url, data=data)
    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_partial_update_employee_customer(load_groups):
    # Given
    cus = baker.make(User, user_type='customer')
    cus.groups.add(Group.objects.get(name='customer'))
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    data = {
        "phone_number": "1234",
        "email": "changed@email.com"
    }
    # When
    url = reverse("employees-detail", args=[shop.id, employee.id])
    client.force_authenticate(cus)
    response = client.patch(url, data=data)
    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_employee_customer(load_groups):
    # Given
    cus = baker.make(User, user_type='customer')
    cus.groups.add(Group.objects.get(name='customer'))
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    # When
    url = reverse("employees-detail", args=[shop.id, employee.id])
    client.force_authenticate(cus)
    response_delete = client.delete(url)
    # Then
    assert response_delete.status_code == 403
