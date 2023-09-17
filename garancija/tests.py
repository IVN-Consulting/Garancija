import pytest
from garancija.models import Shop, Employee, Warranty
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework.reverse import reverse


client = APIClient()


@pytest.mark.django_db
def test_get_existing_shop():
    # Given
    shop = baker.make(Shop)

    # When
    url = reverse("shop-retrieve", args=[shop.id])
    response = client.get(url)

    # Then
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == shop.id
    assert data['name'] == shop.name
    assert data['email'] == shop.email
@pytest.mark.django_db
def test_get_employees_by_shop():
    shop = baker.make(Shop)
    employee = baker.make(Employee, shop=shop)
    employee2 = baker.make(Employee)

    url = reverse("shop-employees", args=[shop.id])
    response = client.get(url)
    assert response.status_code == 200

    data = response.json()
    assert employee.id in [x['id'] for x in data]
    assert not employee2.id in [x['id'] for x in data]

    url = reverse("shop-employees", args=['14'])
    response = client.get(url)

    data=response.json()
    assert response.status_code == 404
    assert data['detail'] == 'Not found.'

@pytest.mark.django_db
def test_warranty_view():
    shop = baker.make(Shop)
    salesperson = baker.make(Employee, shop=shop)
    bad_salesperson = baker.make(Employee)
    warranty = baker.make(Warranty, salesperson=salesperson)

    url = reverse('generics-warranty')
    response = client.get(url)
    assert response.status_code == 200

    data= response.json()
    assert salesperson.id in [x['salesperson']['id'] for x in data]
    assert shop.id in [x['salesperson']['shop']['id'] for x in data]
    assert not bad_salesperson.id in [x['salesperson']['id'] for x in data]