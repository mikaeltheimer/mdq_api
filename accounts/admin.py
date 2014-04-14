from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from models import MDQUser
from django.utils.translation import ugettext_lazy as _


class MDQUserAdmin(UserAdmin):
    '''Custom user admin for the MDQUser object'''

    filter_horizontal = []

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_admin', )}),
        #(_('Important dates'), {'fields': ('last_login', 'date_joined')})
    )
    list_filter = ('is_admin', 'is_active', )

# Register your models here.
admin.site.register(MDQUser, MDQUserAdmin)
