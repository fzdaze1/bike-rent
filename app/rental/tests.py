import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rental.models import Bike, Rental
from rest_framework import status
from unittest.mock import patch

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpass')


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def auth_client(api_client, user):
    response = api_client.post(reverse('token_obtain_pair'), {
                               'username': 'testuser', 'password': 'testpass'})
    token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


@pytest.fixture
def bike():
    return Bike.objects.create(name='Test Bike', status='available')


@pytest.mark.django_db
def test_register(api_client):
    url = reverse('register')
    data = {
        'username': 'newuser',
        'password': 'newpass',
        'email': 'newuser@example.com'
    }

    response = api_client.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username='newuser').exists()

    user = User.objects.get(username='newuser')
    assert user.email == 'newuser@example.com'


@pytest.mark.django_db
def test_token_obtain(api_client, user):
    response = api_client.post(reverse('token_obtain_pair'), {
                               'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data


@pytest.mark.django_db
def test_bike_list(auth_client, bike):
    response = auth_client.get(reverse('bike-list'))
    assert response.status_code == 200
    assert len(response.data) != 0
    assert response.data[0]['name'] == 'Bike 1'


@pytest.mark.django_db
def test_bike_rent(auth_client, user, bike):
    response = auth_client.post(reverse('bike-rent', args=[bike.id]))
    assert response.status_code == 200
    assert Rental.objects.filter(user=user, bike=bike).exists()
    bike.refresh_from_db()
    assert bike.status == 'rented'


@pytest.mark.django_db
@patch('rental.views.calculate_rental_cost.delay')
def test_bike_return(mock_calculate_rental_cost, auth_client, user, bike):
    rental = Rental.objects.create(user=user, bike=bike)
    bike.status = 'rented'
    bike.save()
    response = auth_client.post(reverse('bike-return', args=[bike.id]))
    assert response.status_code == status.HTTP_200_OK
    rental.refresh_from_db()
    bike.refresh_from_db()
    assert bike.status == 'available'
    mock_calculate_rental_cost.assert_called_once_with(rental.id)
    assert response.data['message'] == 'Bike returned successfully.'


@pytest.mark.django_db
def test_rental_history(auth_client, user, bike):
    Rental.objects.create(user=user, bike=bike)
    response = auth_client.get(reverse('rental-history'))
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['bike']['name'] == 'Test Bike'
