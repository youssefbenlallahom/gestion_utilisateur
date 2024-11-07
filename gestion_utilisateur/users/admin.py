from django.contrib import admin
from django import forms
from .models import CoachNutritionist, Client  # Ensure you import the Client model

# Form for CoachNutritionist with password hashing
class CoachNutriAdminForm(forms.ModelForm):
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(), required=False)

    class Meta:
        model = CoachNutritionist
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
            'fields': ('email', 'username', 'password', 'photo')
        }),
        ('Personal Information', {
            'fields': ('bio', 'certifications')
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

# Register the CoachNutritionist model
admin.site.register(CoachNutritionist, CoachNutriAdmin)


# Form for Client with password hashing
class ClientAdminForm(forms.ModelForm):
    password = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Client
        fields = '__all__'

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])  # Hash the password if provided
        if commit:
            user.save()
        return user

class ClientAdmin(admin.ModelAdmin):
    # Title of the model
    list_display = ('username', 'email', 'is_client', 'is_active')
    
    # Configuration of fields displayed in the form
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'password')
        }),
        ('Personal Information', {
            'fields': ('first_name', 'last_name', 'age')
        }),
        ('Permissions', {
            'fields': ('is_active',)
        }),
    )

    # Allows using the password in plain text in the edit form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password', 'is_active')
        }),
    )

    # For filtering active users
    list_filter = ('is_active',)
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

# Register the Client model
admin.site.register(Client, ClientAdmin)
