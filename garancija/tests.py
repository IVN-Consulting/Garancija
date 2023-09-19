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
    data_emp_id = [x['id'] for x in data]
    assert employee.id in data_emp_id
    assert not employee2.id in data_emp_id

    url = reverse("shop-employees", args=['14'])
    response = client.get(url)

    data=response.json()
    assert response.status_code == 404
    assert data['detail'] == 'Not found.'

@pytest.mark.django_db
def test_warranty_api_health():
    baker.make(Warranty)

    url = reverse('generics-warranty')
    response = client.get(url)

    assert response.status_code == 200

@pytest.mark.django_db
def test_warranty_exist():
    warranty = baker.make(Warranty)
    warranty2 = baker.make(Warranty)

    url = reverse('generics-warranty')
    response = client.get(url)
    data = response.json()
    data_id = [x['id'] for x in data]

    assert warranty.id in data_id
    assert warranty2.id in data_id

@pytest.mark.django_db
def test_warranty_salesperson():
    good_shop = baker.make(Shop)
    good_salesperson = baker.make(Employee, shop=good_shop)
    bad_salesperson = baker.make(Employee)
    warranty = baker.make(Warranty, salesperson=good_salesperson)

    url = reverse('generics-warranty')
    response = client.get(url)
    data= response.json()
    data_sp_id = [x['salesperson']['id'] for x in data]

    assert good_salesperson.id in data_sp_id
    assert warranty.salesperson.id in data_sp_id
    assert not bad_salesperson.id in data_sp_id

@pytest.mark.django_db
def test_warranty_shop():
    good_shop = baker.make(Shop)
    bad_shop = baker.make(Shop)

    good_salesperson = baker.make(Employee, shop=good_shop)
    warranty = baker.make(Warranty, salesperson=good_salesperson)
    warranty2 = baker.make(Warranty, salesperson=good_salesperson)

    url = reverse('generics-warranty')
    response = client.get(url)
    data= response.json()
    data_shop_id = [x['salesperson']['shop']['id'] for x in data]

    assert warranty.salesperson.shop.id in data_shop_id
    assert warranty2.salesperson.shop.id in data_shop_id
    assert good_shop.id in data_shop_id
    assert not bad_shop.id in data_shop_id