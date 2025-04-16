from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from .models import CustomUser

class CustomUserAdmin(DefaultUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Roles', {'fields': ('is_student', 'is_teacher', 'is_admin')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_author'),
        }),
    )

    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_author',
        'is_student', 'is_teacher', 'is_admin', 'is_staff', 'is_superuser'
    )

    list_filter = ('is_student', 'is_teacher', 'is_admin', 'is_author')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if not request.user.is_superuser:
            # Restrict non-superusers from seeing superusers
            queryset = queryset.filter(is_superuser=False)
        return queryset

# Register the CustomUser with the CustomUserAdmin
admin.site.register(CustomUser, CustomUserAdmin)