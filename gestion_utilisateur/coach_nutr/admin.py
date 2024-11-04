from django.contrib import admin
from django import forms
from .models import CoachNutri

class CoachNutriAdminForm(forms.ModelForm):
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(), required=False)

    class Meta:
        model = CoachNutri
        fields = '__all__'

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])  # Hash the password if provided
        if commit:
            user.save()
        return user

class CoachNutriAdmin(admin.ModelAdmin):
    # Title of the model
    list_display = ('username', 'email', 'is_coach', 'is_nutritionist', 'is_staff', 'is_active')
    
    # Configuration of fields displayed in the form
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password','photo')
        }),
        ('Personal Information', {
            'fields': ('bio', 'certifications', 'specialization')
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_coach', 'is_nutritionist')
        }),
    )

    # Allows using the password in plain text in the edit form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'is_staff', 'is_active', 'is_coach', 'is_nutritionist')
        }),
    )

    # For filtering active users
    list_filter = ('is_staff', 'is_active', 'is_coach', 'is_nutritionist')
    search_fields = ('username', 'email')

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['password'].widget.attrs['autocomplete'] = 'new-password'
        return form

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)  # Save the user first
        if form.cleaned_data['password']:  # If a password is provided
            obj.set_password(form.cleaned_data['password'])  # Hash the password
            obj.save()  # Save the user again

# Register the model and the admin
admin.site.register(CoachNutri, CoachNutriAdmin)
