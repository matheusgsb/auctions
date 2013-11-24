from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
from .forms import *

# Register your models here.

class CustomUserAdmin(UserAdmin):
	add_form = CustomUserCreationForm
	form = CustomUserChangeForm

	list_display = ('username', 'email', 'name', 'is_staff', 'signup_date')
	list_filter = ('is_staff', 'is_superuser',
		'is_active', 'groups')
	search_fields = ('username', 'email',)	
	ordering = ('-signup_date', 'username')
	filter_horizontal = ('groups', 'user_permissions',)

	fieldsets = (
			(None, {'fields': (('username', 'email'), 'password',)}),
			('Personal info', {'fields': ('name',)}),
			('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
			('Important dates', {'fields': ('last_login', 'signup_date',)}),
		)

	add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')}
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
# admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Product)