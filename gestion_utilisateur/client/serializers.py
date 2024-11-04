
from rest_framework import serializers
from .models import *

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'
    def create(self, validated_data):
        # Supprime le mot de passe des données validées pour ne pas l'enregistrer en texte clair
        password = validated_data.pop('password')
        user = Client(**validated_data)
        user.set_password(password)  # Utilise la méthode pour hasher le mot de passe
        user.save()
        return user
    
