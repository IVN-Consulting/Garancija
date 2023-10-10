import pytest
from garancija.models import Shop, Employee, Warranty
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework.reverse import reverse


client = APIClient()


@pytest.mark.django_db
def test_list_warranties():
    pass

@pytest.mark.django_db
def test_retrieve_warranty():
    pass


@pytest.mark.django_db
def test_create_warranty():
    pass


@pytest.mark.django_db
def test_delete_warranty():
    pass


@pytest.mark.django_db
def test_edit_warranty():
    pass
