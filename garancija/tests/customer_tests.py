import pytest
from garancija.models import Shop
from model_bakery import baker
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from user.models import User


client = APIClient()


@pytest.mark.django_db
def test_list_customers():
    pass


@pytest.mark.django_db
def test_retrieve_customer():
    pass


@pytest.mark.django_db
def test_retrieve_404():
    pass


@pytest.mark.django_db
def test_create_customer():
    pass


@pytest.mark.django_db
def test_edit_customer():
    pass


@pytest.mark.django_db
def test_delete_customer():
    pass
