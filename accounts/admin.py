from django.contrib import admin
from .models import User
from .forms import UserUpdationForm

# Register your models here.
class UserAccountAdmin(admin.ModelAdmin):
    form = UserUpdationForm
    search_fields = ('first_name', 'last_name', 'email', 'is_active',) 
    list_display = ('first_name', 'last_name', 'email', 'is_active',)
    list_display_links = ('first_name', 'last_name', 'email',)
    list_filter = ('is_active',)
    ordering = ('first_name', )

admin.site.register(User, UserAccountAdmin)