import pytest
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
def test_employee_can_list_customers(load_groups):
    employee = baker.make(User, user_type="employee")
    employee.groups.add(Group.objects.get(name='employee'))
    num_of_customers = 10
    customer_ids = []
    for _ in range(num_of_customers):
        customer = baker.make(User, user_type="customer")
        customer.groups.add(Group.objects.get(name='customer'))
        customer_ids.append(customer.id)

    url = reverse("customers-list")
    client.force_authenticate(employee)
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()

    assert set(customer_ids) == set([x['id'] for x in data])


@pytest.mark.django_db
def test_admin_can_list_customers(load_groups):
    admin = baker.make(User, is_superuser=True)
    num_of_customers = 10
    customer_ids = []
    i = 0
    for _ in range(num_of_customers):
        name = 'test'
        customer = baker.make(User, user_type="customer", first_name = f'{name}{i}')
        customer.groups.add(Group.objects.get(name='customer'))
        customer_ids.append(customer.id)
        i += 1

    url = reverse("customers-list")
    client.force_authenticate(admin)
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert set(customer_ids) == set([x['id'] for x in data])


@pytest.mark.django_db
def test_customer_cant_list_customers(load_groups):
    customer = baker.make(User, user_type="customer")
    customer.groups.add(Group.objects.get(name='customer'))

    url = reverse("customers-list")
    client.force_authenticate(customer)
    response = client.get(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_create_customer(load_groups):
    admin = baker.make(User, is_superuser=True)
    data = {
        "first_name": "novi",
        "last_name": "novi",
        "phone_number": "1234",
        "email": "novi@email.com"
    }

    url = reverse("customers-list")
    client.force_authenticate(admin)
    response = client.post(url, data=data)

    assert response.status_code == 201, response.json()
    resp_data = response.json()
    assert data['first_name'] == resp_data['first_name']
    assert data['last_name'] == resp_data['last_name']
    assert data['phone_number'] == resp_data['phone_number']
    assert data['email'] == resp_data['email']


@pytest.mark.django_db
def test_employee_cant_create_customer(load_groups):
    employee = baker.make(User, user_type="employee")
    employee.groups.add(Group.objects.get(name='employee'))
    data = {
        "first_name": "novi",
        "last_name": "novi",
        "phone_number": "1234",
        "email": "novi@email.com"
    }

    url = reverse("customers-list")
    client.force_authenticate(employee)
    response = client.post(url, data=data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_employee_can_retrieve_customer(load_groups):
    customer = baker.make(User, user_type="customer")
    customer.groups.add(Group.objects.get(name='customer'))
    employee = baker.make(User, user_type="employee")
    employee.groups.add(Group.objects.get(name='employee'))

    url = reverse("customers-detail", args=[customer.id])
    client.force_authenticate(employee)
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data['id'] == customer.id


@pytest.mark.django_db
def test_admin_can_retrieve_customer(load_groups):
    customer = baker.make(User, user_type="customer")
    customer.groups.add(Group.objects.get(name='customer'))
    admin = baker.make(User, is_superuser=True)

    url = reverse("customers-detail", args=[customer.id])
    client.force_authenticate(admin)
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data['id'] == customer.id


@pytest.mark.django_db
def test_admin_can_update_customer(load_groups):
    admin = baker.make(User, is_superuser=True)
    data = {
        "first_name": "novi",
        "last_name": "novi",
        "phone_number": "1234",
        "email": "novi@email.com"
    }
    customer = baker.make(User, user_type="customer")
    customer.groups.add(Group.objects.get(name='customer'))

    url = reverse("customers-detail", args=[customer.id])
    client.force_authenticate(admin)
    response = client.patch(url, data=data)
    r_data = response.json()

    assert response.status_code == 200
    assert r_data['id'] == customer.id
    assert r_data['first_name'] == data['first_name']
    assert r_data['last_name'] == data['last_name']
    assert r_data['phone_number'] == data['phone_number']
    assert r_data['email'] == data['email']


@pytest.mark.django_db
def test_employee_cant_update_customer(load_groups):
    employee = baker.make(User, user_type="employee")
    employee.groups.add(Group.objects.get(name='employee'))
    data = {
        "first_name": "novi",
        "last_name": "novi",
        "phone_number": "1234",
        "email": "novi@email.com"
    }
    customer = baker.make(User, user_type="customer")
    customer.groups.add(Group.objects.get(name='customer'))

    url = reverse("customers-detail", args=[customer.id])
    client.force_authenticate(employee)
    response = client.patch(url, data=data)

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_partial_update_customer(load_groups):
    admin = baker.make(User, is_superuser=True)
    data = {
        "phone_number": "5555555",
    }
    customer = baker.make(User, user_type="customer")
    customer.groups.add(Group.objects.get(name='customer'))

    url = reverse("customers-detail", args=[customer.id])
    client.force_authenticate(admin)
    response = client.patch(url, data=data)
    r_data = response.json()

    assert response.status_code == 200
    assert r_data['id'] == customer.id
    assert r_data['phone_number'] == data['phone_number']


@pytest.mark.django_db
def test_employee_can_partial_update_customer(load_groups):
    employee = baker.make(User, user_type="employee")
    employee.groups.add(Group.objects.get(name='employee'))
    data = {
        "phone_number": "5555555",
    }
    customer = baker.make(User, user_type="customer")
    customer.groups.add(Group.objects.get(name='customer'))

    url = reverse("customers-detail", args=[customer.id])
    client.force_authenticate(employee)
    response = client.patch(url, data=data)
    r_data = response.json()

    assert response.status_code == 403


@pytest.mark.django_db
def test_admin_can_delete_customer(load_groups):
    admin = baker.make(User, is_superuser=True)
    customer = baker.make(User, user_type="customer")
    customer.groups.add(Group.objects.get(name='customer'))

    url = reverse("customers-detail", args=[customer.id])
    client.force_authenticate(admin)
    response = client.delete(url)

    assert response.status_code == 204


@pytest.mark.django_db
def test_employee_cant_delete_customer(load_groups):
    employee = baker.make(User, user_type="employee")
    employee.groups.add(Group.objects.get(name='employee'))
    customer = baker.make(User, user_type="customer")
    customer.groups.add(Group.objects.get(name='customer'))

    url = reverse("customers-detail", args=[customer.id])
    client.force_authenticate(employee)
    response = client.delete(url)

    assert response.status_code == 403


@pytest.mark.django_db
def test_employee_and_customer_cant_delete_customer(load_groups):
    employee = baker.make(User, user_type="employee")
    employee.groups.add(Group.objects.get(name='employee'))
    customer = baker.make(User, user_type="customer")
    customer.groups.add(Group.objects.get(name='customer'))
    customer2 = baker.make(User, user_type="customer")
    customer2.groups.add(Group.objects.get(name='customer'))
    users = [employee, customer]

    url = reverse("customers-detail", args=[customer2.id])
    for user in users:
        client.force_authenticate(user)
        response = client.delete(url)

        assert response.status_code == 403
