from logging import getLogger

from django.contrib import admin
from django.contrib.admin.models import LogEntry, DELETION
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import escape
from django.utils.safestring import mark_safe

from .models import User

logger = getLogger(__name__)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """Django Admin Log Entries"""
    date_hierarchy = 'action_time'
    list_display = ('action_time', 'user_link', 'content_type', 'object_link',
                    'action_flag', 'change_message')
    list_filter = ('action_flag', 'content_type')
    search_fields = ('user__first_name', 'user__last_name', 'user__email',
                     'object_repr', 'change_message')

    def has_add_permission(self, request):
        """Permission to ADD a LogEntry"""
        return False

    def has_change_permission(self, request, obj=None):
        """Permission to CHANGE a LogEntry"""
        return False

    def has_delete_permission(self, request, obj=None):
        """Permission to DELETE a LogEntry"""
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        """Permission to VIEW a LogEntry"""
        return request.user.is_superuser

    def user_link(self, obj):
        """Show link to the User"""
        try:
            url = reverse('admin:core_user_change', args=[obj.user_id])
            link = f'<a href="{url}">{escape(obj.user)}</a>'
        except Exception as e:
            logger.debug(e)
            link = escape(obj.user)
        return mark_safe(link)

    user_link.admin_order_field = "user"
    user_link.short_description = "user"

    def object_link(self, obj):
        """Show link to the object"""
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            try:
                ct = obj.content_type
                url = reverse(f'admin:{ct.app_label}_{ct.model}_change',
                              args=[obj.object_id])
                link = f'<a href="{url}">{escape(obj.object_repr)}</a>'
            except Exception as e:
                logger.debug(e)
                link = escape(obj.object_repr)
        return mark_safe(link)

    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"


@admin.register(User)
class UserAdmin(UserAdmin):
    """Admin for User model"""
    ordering = ('id', )
    list_display = (
        'id', 'email', 'first_name', 'last_name', 'last_login', 'date_joined',
        'is_staff', 'is_superuser', 'is_active')
    list_display_links = ('id', 'email')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
        ('Roles', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
        ('Dates', {'fields': ('last_login', 'date_joined')}))
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'password1', 'password2')
        }),)
    readonly_fields = ('last_login', 'date_joined')
    search_fields = ('id', 'email', 'first_name', 'last_name')
