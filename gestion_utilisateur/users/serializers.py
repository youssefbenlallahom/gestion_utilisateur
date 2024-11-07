from rest_framework import serializers
from .models import User, Client, CoachNutritionist

class CoachNutriSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachNutritionist
        fields = ['email', 'username', 'is_coach', 'is_nutritionist', 'certifications', 'bio', 'photo']
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
        }

    def create(self, validated_data):
        password = validated_data.pop('password')  # Remove password from validated data
        user = CoachNutritionist(**validated_data)  # Create user instance
        user.set_password(password)  # Hash the password
        user.save()  # Save the user instance
        return user
    
    def update(self, instance, validated_data):
        # Handle the password in the update method
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:  # If a new password is provided, hash it
            instance.set_password(password)
        instance.save()
        return instance
    
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},  # Ensure password is write-only
        }

    def create(self, validated_data):
        password = validated_data.pop('password')  # Remove password from validated data
        user = Client(**validated_data)  # Create user instance
        user.set_password(password)  # Hash the password
        user.save()  # Save the user instance
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)  # Handle password in update
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:  # If a new password is provided, hash it
            instance.set_password(password)
        instance.save()
        return instance
