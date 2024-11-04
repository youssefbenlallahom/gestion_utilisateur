from django.db import models
from django.contrib.auth.models import AbstractBaseUser , BaseUserManager, PermissionsMixin, Group, Permission

# Manager personnalisé pour CustomUser
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

# Modèle principal pour l'authentification
class CoachNutri(AbstractBaseUser , PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_coach = models.BooleanField(default=False)
    is_nutritionist = models.BooleanField(default=False)
    photo = models.TextField(blank=True, null=True,default="https://www.shareicon.net/data/256x256/2016/07/21/799323_user_512x512.png")     
    certifications = models.TextField()
    bio = models.TextField()
    specialization = models.CharField(max_length=50, choices=[
        ('fitness', 'Fitness'),
        ('yoga', 'Yoga'),
    ])

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    groups = models.ManyToManyField(Group, related_name='coachnutri_set', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='coachnutri_permissions', blank=True)

    def __str__(self):
        return self.username