from rest_framework import serializers
from NurseryApp.models import Pet


class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        exclude = ['shelter', 'is_active']
