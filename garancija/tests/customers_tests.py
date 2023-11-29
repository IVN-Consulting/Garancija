import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from user.models import User
from django.core.management import call_command
from django.contrib.auth.models import Group
from garancija.models import Shop


client = APIClient()


@pytest.fixture
def load_groups():
    call_command("generate_roles")


@pytest.mark.django_db
def test_list_customers_admin(load_groups):
    # Given
    admin = baker.make(User, is_superuser=True)
    num_of_customers = 10
    customer_ids = []

    for i in range(1, num_of_customers + 1):
        customer = baker.make(User, user_type="customer")
        if customer.id != admin.id:
            customer_ids.append(customer.id)
    # When
    url = reverse("customers-list")
    client.force_authenticate(admin)
    response = client.get(url)
    # Then
    assert response.status_code == 200
    data = response.json()
    assert set(customer_ids) == set([x['id'] for x in data])


@pytest.mark.django_db
def test_create_customer_admin(load_groups):
    admin = baker.make(User, is_superuser=True)
    # Given
    data = {
        "first_name": "novi",
        "last_name": "novi",
        "phone_number": "1234",
        "email": "novi@email.com"
    }
    # When
    url = reverse("customers-list")
    client.force_authenticate(admin)
    response = client.post(url, data=data)
    # Then
    assert response.status_code == 201, response.json()
    resp_data = response.json()
    assert data['first_name'] == resp_data['first_name']
    assert data['last_name'] == resp_data['last_name']
    assert data['phone_number'] == resp_data['phone_number']
    assert data['email'] == resp_data['email']


@pytest.mark.django_db
def test_retrieve_customer_admin(load_groups):
    # Given
    admin = baker.make(User, is_superuser=True)
    customer = baker.make(User, user_type="customer")
    # When
    url = reverse("customers-detail", args=[customer.id])
    client.force_authenticate(admin)
    response = client.get(url)
    # Then
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == customer.id
    url2 = reverse("customers-detail", args=['150'])
    response2 = client.get(url2)
    assert response2.status_code == 404
    data2 = response2.json()
    assert data2['detail'] == 'Not found.'


@pytest.mark.django_db
def test_update_customer_admin(load_groups):
    # Given
    admin = baker.make(User, is_superuser=True)
    data = {
        "first_name": "novi",
        "last_name": "novi",
        "phone_number": "1234",
        "email": "novi@email.com"
    }
    customer = baker.make(User, user_type="customer")
    # When
    url = reverse("customers-detail", args=[customer.id])
    client.force_authenticate(admin)
    response = client.patch(url, data=data)
    r_data = response.json()
    # Then
    assert response.status_code == 200
    assert r_data['id'] == customer.id
    assert r_data['first_name'] == data['first_name']
    assert r_data['last_name'] == data['last_name']
    assert r_data['phone_number'] == data['phone_number']
    assert r_data['email'] == data['email']


@pytest.mark.django_db
def test_partial_update_customer_admin(load_groups):
    # Given
    admin = baker.make(User, is_superuser=True)
    data = {
        "phone_number": "5555555",
    }
    customer = baker.make(User, user_type="customer")
    # When
    url = reverse("customers-detail", args=[customer.id])
    client.force_authenticate(admin)
    response = client.patch(url, data=data)
    r_data = response.json()
    # Then
    assert response.status_code == 200
    assert r_data['id'] == customer.id
    assert r_data['phone_number'] == data['phone_number']


@pytest.mark.django_db
def test_delete_customer_admin(load_groups):
    # Given
    admin = baker.make(User, is_superuser=True)
    customer = baker.make(User, user_type="customer")
    # When
    url = reverse("customers-detail", args=[customer.id])
    client.force_authenticate(admin)
    response_delete = client.delete(url)
    response_get_after_del = client.get(url)
    # Then
    assert response_delete.status_code == 204
    assert response_get_after_del.status_code == 404


@pytest.mark.django_db
def test_list_customers_employee(load_groups):
    # Given
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee.groups.add(Group.objects.get(name='employee'))
    num_of_customers = 10
    customer_ids = []
    for _ in range(num_of_customers):
        customer = baker.make(User, user_type="customer")
        customer_ids.append(customer.id)
    # When
    url = reverse("customers-list")
    client.force_authenticate(employee)
    response = client.get(url)
    # Then
    assert response.status_code == 200
    data = response.json()
    assert set(customer_ids) == set([x['id'] for x in data])


@pytest.mark.django_db
def test_create_customer_employee(load_groups):
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee.groups.add(Group.objects.get(name='employee'))
    # Given
    data = {
        "first_name": "novi",
        "last_name": "novi",
        "phone_number": "1234",
        "email": "novi@email.com"
    }
    # When
    url = reverse("customers-list")
    client.force_authenticate(employee)
    response = client.post(url, data=data)
    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_retrieve_customer_employee(load_groups):
    # Given
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee.groups.add(Group.objects.get(name='employee'))
    customer = baker.make(User, user_type="customer")
    # When
    url = reverse("customers-detail", args=[customer.id])
    client.force_authenticate(employee)
    response = client.get(url)
    # Then
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == customer.id
    url2 = reverse("customers-detail", args=['150'])
    response2 = client.get(url2)
    assert response2.status_code == 404
    data2 = response2.json()
    assert data2['detail'] == 'Not found.'


@pytest.mark.django_db
def test_update_customer_employee(load_groups):
    # Given
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee.groups.add(Group.objects.get(name='employee'))
    data = {
        "first_name": "novi",
        "last_name": "novi",
        "phone_number": "1234",
        "email": "novi@email.com"
    }
    customer = baker.make(User, user_type="customer")
    # When
    url = reverse("customers-detail", args=[customer.id])
    client.force_authenticate(employee)
    response = client.patch(url, data=data)
    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_partial_update_customer_employee(load_groups):
    # Given
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee.groups.add(Group.objects.get(name='employee'))
    data = {
        "phone_number": "5555555",
    }
    customer = baker.make(User, user_type="customer")
    # When
    url = reverse("customers-detail", args=[customer.id])
    client.force_authenticate(employee)
    response = client.patch(url, data=data)
    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_customer_employee(load_groups):
    # Given
    shop = baker.make(Shop)
    employee = baker.make(User, user_type="employee", shop=shop)
    employee.groups.add(Group.objects.get(name='employee'))
    customer = baker.make(User, user_type="customer")
    # When
    url = reverse("customers-detail", args=[customer.id])
    client.force_authenticate(employee)
    response_delete = client.delete(url)
    # Then
    assert response_delete.status_code == 403


@pytest.mark.django_db
def test_list_customers_customer(load_groups):
    # Given
    customer_test = baker.make(User, user_type="customer")
    customer_test.groups.add(Group.objects.get(name='customer'))
    num_of_customers = 10
    customer_ids = []
    for _ in range(num_of_customers):
        customer = baker.make(User, user_type="customer")
        customer_ids.append(customer.id)
    # When
    url = reverse("customers-list")
    client.force_authenticate(customer_test)
    response = client.get(url)
    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_create_customer_customer(load_groups):
    customer_test = baker.make(User, user_type="customer")
    customer_test.groups.add(Group.objects.get(name='customer'))
    # Given
    data = {
        "first_name": "novi",
        "last_name": "novi",
        "phone_number": "1234",
        "email": "novi@email.com"
    }
    # When
    url = reverse("customers-list")
    client.force_authenticate(customer_test)
    response = client.post(url, data=data)
    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_retrieve_customer_customer(load_groups):
    # Given
    customer_test = baker.make(User, user_type="customer")
    customer_test.groups.add(Group.objects.get(name='customer'))
    customer = baker.make(User, user_type="customer")
    # When
    url = reverse("customers-detail", args=[customer.id])
    client.force_authenticate(customer_test)
    response = client.get(url)
    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_retrieve_customer_customer_self(load_groups):
    # Given
    customer_test = baker.make(User, user_type="customer")
    customer_test.groups.add(Group.objects.get(name='customer'))
    # When
    url = reverse("customers-detail", args=[customer_test.id])
    client.force_authenticate(customer_test)
    response = client.get(url)
    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_update_customer_customer(load_groups):
    # Given
    customer_test = baker.make(User, user_type="customer")
    customer_test.groups.add(Group.objects.get(name='customer'))
    data = {
        "first_name": "novi",
        "last_name": "novi",
        "phone_number": "1234",
        "email": "novi@email.com"
    }
    customer = baker.make(User, user_type="customer")
    # When
    url = reverse("customers-detail", args=[customer.id])
    client.force_authenticate(customer_test)
    response = client.patch(url, data=data)
    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_update_customer_customer_self(load_groups):
    # Given
    customer_test = baker.make(User, user_type="customer")
    customer_test.groups.add(Group.objects.get(name='customer'))
    data = {
        "first_name": "novi",
        "last_name": "novi",
        "phone_number": "1234",
        "email": "novi@email.com"
    }
    # When
    url = reverse("customers-detail", args=[customer_test.id])
    client.force_authenticate(customer_test)
    response = client.patch(url, data=data)
    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_partial_update_customer_customer(load_groups):
    # Given
    customer_test = baker.make(User, user_type="customer")
    customer_test.groups.add(Group.objects.get(name='customer'))
    data = {
        "phone_number": "5555555",
    }
    customer = baker.make(User, user_type="customer")
    # When
    url = reverse("customers-detail", args=[customer.id])
    client.force_authenticate(customer_test)
    response = client.patch(url, data=data)
    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_partial_update_customer_customer_self(load_groups):
    # Given
    customer_test = baker.make(User, user_type="customer")
    customer_test.groups.add(Group.objects.get(name='customer'))
    data = {
        "phone_number": "5555555",
    }
    # When
    url = reverse("customers-detail", args=[customer_test.id])
    client.force_authenticate(customer_test)
    response = client.patch(url, data=data)
    # Then
    assert response.status_code == 403


@pytest.mark.django_db
def test_delete_customer_customer(load_groups):
    # Given
    customer_test = baker.make(User, user_type="customer")
    customer_test.groups.add(Group.objects.get(name='customer'))
    customer = baker.make(User, user_type="customer")
    # When
    url = reverse("customers-detail", args=[customer.id])
    client.force_authenticate(customer_test)
    response_delete = client.delete(url)
    # Then
    assert response_delete.status_code == 403


@pytest.mark.django_db
def test_delete_customer_customer_self(load_groups):
    # Given
    customer_test = baker.make(User, user_type="customer")
    customer_test.groups.add(Group.objects.get(name='customer'))
    # When
    url = reverse("customers-detail", args=[customer_test.id])
    client.force_authenticate(customer_test)
    response_delete = client.delete(url)
    # Then
    assert response_delete.status_code == 403
