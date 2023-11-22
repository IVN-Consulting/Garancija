import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from garancija.models import Warranty
from rest_framework.reverse import reverse
from user.models import User
from django.core.management import call_command
from django.contrib.auth.models import Group


client = APIClient()


@pytest.fixture
def load_groups():
    call_command("generate_roles")


@pytest.mark.django_db
def test_list_warranties_customer(load_groups):
    # Given
    customer = baker.make(User, user_type='customer')
    customer.groups.add(Group.objects.get(name='customer'))
    num_of_warranty = 10
    warranty_ids = []
    for _ in range(num_of_warranty):
        warranty = baker.make(Warranty, customer=customer)
        warranty_ids.append(warranty.id)

    # When
    url = reverse("warranty-list")
    client.force_authenticate(customer)
    response = client.get(url)

    # Then
    assert response.status_code == 200
    data = response.json()
    assert set(warranty_ids) == set([x['id'] for x in data])


@pytest.mark.django_db
def test_retrieve_warranty_customer(load_groups):
    # Given
    customer = baker.make(User, user_type='customer')
    customer.groups.add(Group.objects.get(name='customer'))
    warranty = baker.make(Warranty, customer=customer)

    # When
    url = reverse("warranty-detail", args=[warranty.id])
    client.force_authenticate(customer)
    response = client.get(url)

    # Then
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == warranty.id
    assert data['product_name'] == warranty.product_name
    assert data['start_date'] == str(warranty.start_date)
    assert data['end_date'] == str(warranty.end_date)
    assert data['salesperson']['id'] == warranty.salesperson.id
    assert data['customer']['id'] == warranty.customer.id


@pytest.mark.django_db
def test_create_warranty_customer(load_groups):
    # Given
    customer = baker.make(User, user_type='customer')
    customer.groups.add(Group.objects.get(name='customer'))
    salesperson = baker.make(User, user_type="employee")
    data = {
        "product_name": "test name",
        "start_date": "2022-10-10",
        "end_date": "2033-10-10",
        "salesperson": salesperson.id,
        "customer": customer.id
    }
    # When
    url = reverse("warranty-list")
    client.force_authenticate(customer)
    response = client.post(url, data=data)
    # Then
    assert response.status_code == 403, response.json()
    resp_data = response.json()
    assert resp_data == {'detail': 'You do not have permission to perform this action.'}


@pytest.mark.django_db
def test_delete_warranty_customer(load_groups):
    # Given
    customer = baker.make(User, user_type='customer')
    customer.groups.add(Group.objects.get(name='customer'))
    warranty = baker.make(Warranty, customer=customer)
    # When
    url = reverse("warranty-detail", args=[warranty.id])
    client.force_authenticate(customer)
    response = client.delete(url)
    # Then
    assert response.status_code == 403
    resp_data = response.json()
    assert resp_data == {'detail': 'You do not have permission to perform this action.'}


@pytest.mark.django_db
def test_partial_edit_warranty_customer(load_groups):
    customer = baker.make(User, user_type='customer')
    salesperson = baker.make(User, user_type="employee")
    warranty = baker.make(Warranty, customer=customer, salesperson=salesperson)
    # When
    url = reverse("warranty-detail", args=[warranty.id])
    client.force_authenticate(customer)
    response = client.put(url)
    assert response.status_code == 403
    resp_data = response.json()
    assert resp_data == {'detail': 'You do not have permission to perform this action.'}


@pytest.mark.django_db
def test_edit_warranty_customer(load_groups):
    # Given
    customer = baker.make(User, user_type='customer')
    salesperson = baker.make(User, user_type="employee")
    warranty = baker.make(Warranty, customer=customer, salesperson=salesperson)
    # When
    url = reverse("warranty-detail", args=[warranty.id])
    response = client.put(url)
    # Then
    assert response.status_code == 403
    resp_data = response.json()
    assert resp_data == {'detail': 'You do not have permission to perform this action.'}

@pytest.mark.django_db
def test_retrieve_warranty_other_customer(load_groups):
    # Given
    customer = baker.make(User, user_type='customer')
    customer2 = baker.make(User, user_type='customer')
    customer.groups.add(Group.objects.get(name='customer'))
    customer2.groups.add(Group.objects.get(name='customer'))
    warranty = baker.make(Warranty, customer=customer2)

    # When
    url = reverse("warranty-detail", args=[warranty.id])
    client.force_authenticate(customer)
    response = client.get(url)

    # Then
    assert response.status_code == 404



