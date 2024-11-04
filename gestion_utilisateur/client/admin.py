from django.contrib import admin
from client.models import Client

class ClientAdmin(admin.ModelAdmin):
    # Specify the fields to display in the list view
    list_display = ('email', 'username', 'first_name', 'last_name', 'age', 'subscription')
    
    # Enable search functionality
    search_fields = ('email', 'username', 'first_name', 'last_name')
    
    # Add filters for specific fields in the right sidebar
    list_filter = ('subscription',)

    # Customize the form layout
    fieldsets = (
        (None, {
            'fields': ('email', 'username', 'first_name', 'last_name', 'age', 'subscription')
        }),
    )

    # Optionally, you can enable pagination
    list_per_page = 20

# Register the Client model with the custom admin class
admin.site.register(Client, ClientAdmin)
