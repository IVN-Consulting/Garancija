import pytest
from rest_framework.test import APIClient


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
