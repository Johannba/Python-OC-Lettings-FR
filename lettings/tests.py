from django.test import TestCase, Client
from django.urls import reverse, resolve
from lettings.models import Letting, Address

import pytest
from pytest_django.asserts import assertTemplateUsed


class TestLettingApp(TestCase):
    client = Client()

    @pytest.mark.django_db
    def setUp(self):
        address = Address.objects.create(
            number=7,
            street="street",
            city="issou",
            state="yvelines",
            zip_code=78,
            country_iso_code=249,
        )
        Letting.objects.create(title="issou city", address=address)

    def test_lettings_index_url(self):
        path = reverse("lettings:index")
        assert path == "/lettings/"
        assert resolve(path).view_name == "lettings:index"

    @pytest.mark.django_db
    def test_address_model(self):
        address = Address.objects.get(city="issou")
        expected_value = "7 street"
        assert str(address) == expected_value

    @pytest.mark.django_db
    def test_letting_model(self):
        letting = Letting.objects.get(title="issou city")
        expected_value = "issou city"
        assert str(letting) == expected_value

    @pytest.mark.django_db
    def test_letting_detail_view(self):
        letting = Letting.objects.all().first()
        path = reverse("lettings:letting", kwargs={"letting_id": letting.id})
        response = self.client.get(path)
        content = response.content.decode()
        assert response.status_code == 200
        assert letting.title in content
        assertTemplateUsed(response, "lettings/letting.html")

    @pytest.mark.django_db
    def test_lettings_index_view(self):
        path = reverse("lettings:index")
        response = self.client.get(path)
        content = response.content.decode()
        assert response.status_code == 200
        assert Letting.objects.all().first().title in content
        assertTemplateUsed(response, "lettings/index.html")
