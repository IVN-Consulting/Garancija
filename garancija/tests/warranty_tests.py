import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from garancija.models import Warranty, Shop
from rest_framework.reverse import reverse
from user.models import User
from django.core.management import call_command
from django.contrib.auth.models import Group


client = APIClient()


@pytest.fixture
def load_groups():
    call_command("generate_roles")


@pytest.mark.django_db
def test_list_warranties_employee(load_groups):
    employee = baker.make(User, user_type='employee')
    employee.groups.add(Group.objects.get(name='employee'))
    num_of_warranty = 10
    warranty_ids = []
    for _ in range(num_of_warranty):
        warranty = baker.make(Warranty, salesperson=employee)
        warranty_ids.append(warranty.id)

    url = reverse("warranty-list")
    client.force_authenticate(employee)
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert set(warranty_ids) == set([x['id'] for x in data])


@pytest.mark.django_db
def test_retrieve_warranty_employee(load_groups):
    employee = baker.make(User, user_type='employee')
    employee.groups.add(Group.objects.get(name='employee'))
    customer = baker.make(User, user_type='customer')
    warranty = baker.make(Warranty, salesperson=employee, customer=customer)

    url = reverse("warranty-detail", args=[warranty.id])
    client.force_authenticate(employee)
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data['id'] == warranty.id
    assert data['product_name'] == warranty.product_name
    assert data['start_date'] == str(warranty.start_date)
    assert data['end_date'] == str(warranty.end_date)
    assert data['salesperson']['id'] == warranty.salesperson.id
    assert data['customer']['id'] == warranty.customer.id


@pytest.mark.django_db
def test_create_warranty_employee(load_groups):
    salesperson = baker.make(User, user_type='employee')
    customer = baker.make(User, user_type="customer")
    data = {
        "product_name": "test name",
        "start_date": "2022-10-10",
        "end_date": "2033-10-10",
        "salesperson": salesperson.id,
        "customer": customer.id
    }

    url = reverse("warranty-list")
    client.force_authenticate(salesperson)
    response = client.post(url, data=data)

    assert response.status_code == 201, response.json()
    resp_data = response.json()
    assert data['product_name'] == resp_data['product_name']
    assert data['start_date'] == resp_data['start_date']
    assert data['end_date'] == resp_data['end_date']
    assert resp_data['salesperson']['id'] == salesperson.id
    assert resp_data['customer']['id'] == customer.id


@pytest.mark.django_db
def test_employee_delete_warranty(load_groups):
    salesperson = baker.make(User, user_type='employee')
    salesperson.groups.add(Group.objects.get(name='employee'))
    customer = baker.make(User, user_type='customer')
    warranty = baker.make(Warranty, customer=customer, salesperson=salesperson)

    url = reverse("warranty-detail", args=[warranty.id])
    client.force_authenticate(salesperson)
    response = client.delete(url)

    assert response.status_code == 204
    assert client.get(url).status_code == 404


@pytest.mark.django_db
def test_partial_edit_warranty_employee(load_groups):
    customer = baker.make(User, user_type='customer')
    salesperson = baker.make(User, user_type="employee")
    salesperson.groups.add(Group.objects.get(name='employee'))
    test_data = [
        ['product_name', 'test name'],
        ['start_date', '2022-10-10'],
        ['end_date', '2033-10-10'],
        ['salesperson', salesperson.id],
        ['customer', customer.id]
    ]

    customer2 = baker.make(User, user_type='customer')
    warranty = baker.make(Warranty, customer=customer2)
    # When
    url = reverse("warranty-detail", args=[warranty.id])
    client.force_authenticate(salesperson)

    for field_name, field_value in test_data:
        warranty.refresh_from_db()
        old_data = {
            warranty_field_name: getattr(warranty, warranty_field_name)
            for warranty_field_name, non_used_value in test_data
        }

        response = client.patch(
            url,
            data={field_name: field_value}
        )
        assert response.status_code == 200

        warranty.refresh_from_db()
        new_data = {
            warranty_field_name: getattr(warranty, warranty_field_name)
            for warranty_field_name, non_used_value in test_data
        }

        expected = ((field_name, getattr(warranty, field_name)),)
        assert set(expected) == set(new_data.items()) - set(old_data.items())


@pytest.mark.django_db
def test_edit_warranty_employee(load_groups):
    customer = baker.make(User, user_type='customer')
    salesperson = baker.make(User, user_type="employee")
    salesperson.groups.add(Group.objects.get(name='employee'))
    data = {
        "product_name": "test name",
        "start_date": "2023-10-10",
        "end_date": "2033-10-10",
        "salesperson": salesperson.id,
        "customer": customer.id
    }
    warranty = baker.make(Warranty, customer=customer)

    url = reverse("warranty-detail", args=[warranty.id])
    client.force_authenticate(salesperson)
    response = client.put(url, data=data)

    assert response.status_code == 200, response.json()
    resp_data = response.json()
    assert data['product_name'] == resp_data['product_name']
    assert data['start_date'] == resp_data['start_date']
    assert data['end_date'] == resp_data['end_date']
    assert salesperson.id == resp_data['salesperson']
    assert customer.id == resp_data['customer']


@pytest.mark.django_db
def test_employee_list_warranties_for_shop(load_groups):
    shop = baker.make(Shop)
    employee = baker.make(User, user_type='employee', shop=shop)
    employee2 = baker.make(User, user_type='employee', shop=shop)
    employee.groups.add(Group.objects.get(name='employee'))
    employee2.groups.add(Group.objects.get(name='employee'))
    num_of_warranty = 10
    warranty_ids = []
    for _ in range(num_of_warranty):
        warranty = baker.make(Warranty, salesperson=employee)
        warranty_ids.append(warranty.id)

    url = reverse("warranty-list")
    client.force_authenticate(employee2)
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert set(warranty_ids) == set([x['id'] for x in data])


@pytest.mark.django_db
def test_employee_cant_list_warranties_for_other_shop(load_groups):
    shop = baker.make(Shop)
    employee = baker.make(User, user_type='employee', shop=shop)
    employee2 = baker.make(User, user_type='employee')
    employee.groups.add(Group.objects.get(name='employee'))
    employee2.groups.add(Group.objects.get(name='employee'))
    num_of_warranty = 10
    warranty_ids = []
    for _ in range(num_of_warranty):
        warranty = baker.make(Warranty, salesperson=employee)
        warranty_ids.append(warranty.id)

    url = reverse("warranty-list")
    client.force_authenticate(employee2)
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data == []


@pytest.mark.django_db
def test_employee_retrieve_warranty_for_other_employee(load_groups):
    shop = baker.make(Shop)
    good_salesperson = baker.make(User, user_type='employee')
    good_salesperson.groups.add(Group.objects.get(name='employee'))
    bad_salesperson = baker.make(User, user_type='employee', shop=shop)
    bad_salesperson.groups.add(Group.objects.get(name='employee'))
    bad_warranty = baker.make(Warranty, id=10, customer=bad_salesperson)
    good_warranty = baker.make(Warranty, id=10, customer=good_salesperson)

    url = reverse("warranty-detail", args=["10"])
    client.force_authenticate(good_salesperson)
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data['id'] == good_warranty.id
    assert data['product_name'] == good_warranty.product_name
    assert data['start_date'] == str(good_warranty.start_date)
    assert data['end_date'] == str(good_warranty.end_date)
    assert data['salesperson']['id'] == good_warranty.salesperson.id
    assert data['customer']['id'] == good_warranty.customer.id
    print(bad_warranty)


@pytest.mark.django_db
def test_customer_retrieve_warranty_for_other_customer(load_groups):
    good_customer = baker.make(User, user_type='customer')
    good_customer.groups.add(Group.objects.get(name='customer'))
    bad_customer = baker.make(User, user_type='customer')
    bad_customer.groups.add(Group.objects.get(name='customer'))
    bad_warranty = baker.make(Warranty, id=10, customer=bad_customer)
    good_warranty = baker.make(Warranty, id=10, customer=good_customer)

    url = reverse("warranty-detail", args=["10"])
    client.force_authenticate(good_customer)
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data['id'] == good_warranty.id
    assert data['product_name'] == good_warranty.product_name
    assert data['start_date'] == str(good_warranty.start_date)
    assert data['end_date'] == str(good_warranty.end_date)
    assert data['salesperson']['id'] == good_warranty.salesperson.id
    assert data['customer']['id'] == good_warranty.customer.id
    print(bad_warranty)
