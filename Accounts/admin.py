from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline, )

    list_display = ('email', 'get_phone', 'get_full_name')
    list_select_related = ('profile', )

    def get_phone(self, instance):
        return instance.profile.phone
    get_phone.short_description = 'Phone'
        
    def get_full_name(self, instance):
        return instance.profile.full_name
    get_full_name.short_description = 'Full Name'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)