from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Bike, Rental
from django.contrib.auth import authenticate

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ['id', 'name', 'status']


class RentalSerializer(serializers.ModelSerializer):
    bike = BikeSerializer(read_only=True)

    class Meta:
        model = Rental
        fields = '__all__'
        read_only_fields = ('start_time', 'end_time', 'total_cost')
