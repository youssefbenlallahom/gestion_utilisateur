
from rest_framework import serializers
from .models import *

class CoachNutriSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachNutri
        fields = [
            'email',
            'username',
            'password',  # Le mot de passe doit être traité séparément
            'is_coach',
            'is_nutritionist',
            'certifications',
            'bio',
            'specialization',
        ]
        extra_kwargs = {
            'password': {'write_only': True},  # Assure que le mot de passe est en mode écriture uniquement
        }

    def create(self, validated_data):
        # Supprime le mot de passe des données validées pour ne pas l'enregistrer en texte clair
        password = validated_data.pop('password')
        user = CoachNutri(**validated_data)
        user.set_password(password)  # Utilise la méthode pour hasher le mot de passe
        user.save()
        return user
    
    
    def update(self, instance, validated_data):
        # Si le mot de passe est présent dans les données validées, le hacher
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)  # Hachage du nouveau mot de passe
        instance.save()
        return instance
