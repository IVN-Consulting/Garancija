import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from garancija.models import Warranty
from garancija.models import Employee
from rest_framework.reverse import reverse


client = APIClient()


@pytest.mark.django_db
def test_list_warranties():
    # Given
    num_of_warranty = 10
    warranty_ids = []
    for _ in range(num_of_warranty):
        warranty = baker.make(Warranty)
        warranty_ids.append(warranty.id)

    # When
    url = reverse("warranty-list")
    response = client.get(url)

    # Then
    assert response.status_code == 200
    data = response.json()
    assert set(warranty_ids) == set([x['id'] for x in data])


@pytest.mark.django_db
def test_retrieve_warranty():
    # Given
    warranty = baker.make(Warranty)

    # When
    url = reverse("warranty-detail", args=[warranty.id])
    response = client.get(url)

    # Then
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == warranty.id
    assert data['product_name'] == warranty.product_name
    assert data['start_date'] == str(warranty.start_date)
    assert data['end_date'] == str(warranty.end_date)
    assert data['salesperson']['id'] == warranty.salesperson.id


@pytest.mark.django_db
def test_create_warranty():
    # Given
    salesperson = baker.make(Employee)
    data = {
        "product_name": "test name",
        "start_date": "2022-10-10",
        "end_date": "2033-10-10",
        "salesperson": salesperson.id
    }
    # When
    url = reverse("warranty-list")
    response = client.post(url, data=data)
    # Then
    assert response.status_code == 201, response.json()
    resp_data = response.json()
    assert data['product_name'] == resp_data['product_name']
    assert data['start_date'] == resp_data['start_date']
    assert data['end_date'] == resp_data['end_date']
    assert resp_data['salesperson']['id'] == salesperson.id


@pytest.mark.django_db
def test_delete_warranty():
    # Given
    warranty = baker.make(Warranty)
    # When
    url = reverse("warranty-detail", args=[warranty.id])
    response_delete = client.delete(url)
    response_get_after_del = client.get(url)
    # Then
    assert response_delete.status_code == 204
    assert response_get_after_del.status_code == 404


@pytest.mark.django_db
def test_partial_edit_warranty():
    salesperson = baker.make(Employee)
    test_data = [
        ['product_name', 'test name'],
        ['start_date', '2022-10-10'],
        ['end_date', '2033-10-10'],
        ['salesperson', salesperson.id]
    ]

    warranty = baker.make(Warranty)
    # When
    url = reverse("warranty-detail", args=[warranty.id])

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
def test_edit_warranty():
    # Given
    salesperson = baker.make(Employee)
    data = {
        "product_name": "test name",
        "start_date": "2022-10-10",
        "end_date": "2033-10-10",
        "salesperson": salesperson.id
    }
    warranty = baker.make(Warranty)
    # When
    url = reverse("warranty-detail", args=[warranty.id])
    response = client.put(url, data=data)
    # Then
    assert response.status_code == 200, response.json()
    resp_data = response.json()
    assert data['product_name'] == resp_data['product_name']
    assert data['start_date'] == resp_data['start_date']
    assert data['end_date'] == resp_data['end_date']
    assert salesperson.id == data['salesperson']
