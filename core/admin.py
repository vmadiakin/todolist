from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import User


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    exclude = ('password',)
    readonly_fields = ('last_login', 'date_joined')

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.change_password_form = self.change_password_form or self.get_change_password_form()
        return super().change_view(request, object_id, form_url, extra_context)


admin.site.register(User, CustomUserAdmin)
