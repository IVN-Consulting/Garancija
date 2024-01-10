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
def test_admin_can_list_employees(load_groups):
    admin = baker.make(User, is_superuser=True)
    shop = baker.make(Shop)
    num_of_employees = 10
    employee_ids = []
    for _ in range(num_of_employees):
        employee2 = baker.make(User, user_type="employee", shop=shop)
        employee2.groups.add(Group.objects.get(name='employee'))
        employee_ids.append(employee2.id)

    url = reverse("employees-list", args=[shop.id])
    client.force_authenticate(admin)
    response = client.get(url)
    assert response.status_code == 200

    data = response.json()
    assert set(employee_ids) == set([x['id'] for x in data])


@pytest.mark.django_db
def test_employee_can_list_own_shop_employees(load_groups):
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee.groups.add(Group.objects.get(name='employee'))
    employee2 = baker.make(User, user_type="employee", shop=shop)
    employee2.groups.add(Group.objects.get(name='employee'))

    url = reverse("employees-list", args=[shop.id])
    client.force_authenticate(employee)
    response = client.get(url)
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert employee.id in [x['id'] for x in data]
    assert employee2.id in [x['id'] for x in data]


@pytest.mark.django_db
def test_employee_cant_list_other_shop_employees(load_groups):
    shop = baker.make(Shop)
    shop2 = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee.groups.add(Group.objects.get(name='employee'))
    num_of_employees = 5
    for _ in range(num_of_employees):
        employee2 = baker.make(User, user_type="employee", shop=shop)
        employee2.groups.add(Group.objects.get(name='employee'))

    url = reverse("employees-list", args=[shop2.id])
    client.force_authenticate(employee)
    response = client.get(url)
    assert response.status_code == 403


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
def test_admin_can_create_employee(load_groups):
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

    assert response.status_code == 201, response.json()
    resp_data = response.json()

    assert data['first_name'] == resp_data['first_name']
    assert data['last_name'] == resp_data['last_name']
    assert data['phone_number'] == resp_data['phone_number']
    assert data['email'] == resp_data['email']
    employee = User.objects.get(id=resp_data['id'])
    assert employee.shop == shop


@pytest.mark.django_db
def test_employee_cant_create_employee(load_groups):
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee.groups.add(Group.objects.get(name='employee'))
    shop = baker.make(Shop)
    data = {
        "first_name": "novi",
        "last_name": "god",
        "phone_number": "1234",
        "email": "novi@email.com"
    }

    url = reverse("employees-list", args=[shop.id])
    client.force_authenticate(employee)
    response = client.post(url, data=data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_retrieve_employee(load_groups):
    admin = baker.make(User, is_superuser=True)
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee.groups.add(Group.objects.get(name='employee'))

    url = reverse("employees-detail", args=[shop.id, employee.id])
    client.force_authenticate(admin)
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data['id'] == employee.id


@pytest.mark.django_db
def test_employee_can_retrieve_own_shop_employee(load_groups):
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee.groups.add(Group.objects.get(name='employee'))
    employee2 = baker.make(User, user_type="employee", shop=shop)
    employee2.groups.add(Group.objects.get(name='employee'))

    url = reverse("employees-detail", args=[shop.id, employee2.id])
    client.force_authenticate(employee)
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data['id'] == employee2.id


@pytest.mark.django_db
def test_employee_cant_retrieve_other_shop_employee(load_groups):
    shop = baker.make(Shop)
    shop2 = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee.groups.add(Group.objects.get(name='employee'))
    employee2 = baker.make(User, user_type="employee", shop=shop2)
    employee2.groups.add(Group.objects.get(name='employee'))

    url = reverse("employees-detail", args=[shop2.id, employee2.id])
    client.force_authenticate(employee)
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_update_employee(load_groups):
    admin = baker.make(User, is_superuser=True)
    data = {
        "first_name": "new name",
        "last_name": "stagod",
        "phone_number": "1234",
        "email": "changed@email.com"
    }
    shop = baker.make(Shop)
    emp = baker.make(User, user_type="employee", shop=shop)
    emp.groups.add(Group.objects.get(name='employee'))
    emp.groups.add(Group.objects.get(name='employee'))

    url = reverse("employees-detail", args=[shop.id, emp.id])
    client.force_authenticate(admin)
    response = client.patch(url, data=data)
    r_data = response.json()

    assert response.status_code == 200
    assert r_data['id'] == emp.id
    assert r_data['first_name'] == data['first_name']
    assert r_data['last_name'] == data['last_name']
    assert r_data['phone_number'] == data['phone_number']
    assert r_data['email'] == data['email']


@pytest.mark.django_db
def test_employee_cant_update_employee(load_groups):
    data = {
        "first_name": "new name",
        "last_name": "stagod",
        "phone_number": "1234",
        "email": "changed@email.com"
    }
    shop = baker.make(Shop)
    emp = baker.make(User, user_type="employee", shop=shop)
    emp.groups.add(Group.objects.get(name='employee'))
    emp2 = baker.make(User, user_type="employee", shop=shop)
    emp2.groups.add(Group.objects.get(name='employee'))

    url = reverse("employees-detail", args=[shop.id, emp2.id])
    client.force_authenticate(emp)
    response = client.patch(url, data=data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_partial_update_employee(load_groups):
    admin = baker.make(User, is_superuser=True)
    data = {
        "phone_number": "1234",
        "email": "changed@email.com"
    }
    shop = baker.make(Shop)
    emp = baker.make(User, user_type="employee", shop=shop)
    emp.groups.add(Group.objects.get(name='employee'))

    url = reverse("employees-detail", args=[shop.id, emp.id])
    client.force_authenticate(admin)
    response = client.patch(url, data=data)
    r_data = response.json()

    assert response.status_code == 200
    assert r_data['id'] == emp.id
    assert r_data['phone_number'] == data['phone_number']
    assert r_data['email'] == data['email']


@pytest.mark.django_db
def test_employee_cant_partial_update_employee(load_groups):
    data = {
        "phone_number": "1234",
        "email": "changed@email.com"
    }
    shop = baker.make(Shop)
    emp = baker.make(User, user_type="employee", shop=shop)
    emp.groups.add(Group.objects.get(name='employee'))
    emp2 = baker.make(User, user_type="employee", shop=shop)
    emp2.groups.add(Group.objects.get(name='employee'))

    url = reverse("employees-detail", args=[shop.id, emp2.id])
    client.force_authenticate(emp)
    response = client.patch(url, data=data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_delete_employee(load_groups):
    admin = baker.make(User, is_superuser=True)
    shop = baker.make(Shop)
    emp = baker.make(User, user_type="employee", shop=shop)

    url = reverse("employees-detail", args=[shop.id, emp.id])
    client.force_authenticate(admin)
    response_delete = client.delete(url)

    assert response_delete.status_code == 204


@pytest.mark.django_db
def test_employee_cant_delete_employee(load_groups):
    shop = baker.make(Shop)
    emp = baker.make(User, user_type="employee", shop=shop)
    emp.groups.add(Group.objects.get(name='employee'))
    emp2 = baker.make(User, user_type="employee", shop=shop)
    emp2.groups.add(Group.objects.get(name='employee'))

    url = reverse("employees-detail", args=[shop.id, emp2.id])
    client.force_authenticate(emp)
    response_delete = client.delete(url)

    assert response_delete.status_code == 403
