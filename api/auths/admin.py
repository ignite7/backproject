"""
Admin Users.
"""

# Django
from django.contrib import admin
from django.contrib.auth.hashers import make_password
from django.contrib.sessions.models import Session
from django.contrib.admin.models import LogEntry

# Models
from models.models import Users, Tokens, Restricts


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    """
    Admin of the model `Users`.
    """

    list_display = (
        'pk',
        'username',
        'email',
        'password',
        'first_name',
        'last_name',
        'phone',
        'picture',
        'is_verified',
        'verified_email',
        'is_used',
        'created_at',
        'modified_at'
    )

    list_editable = (
        'username',
        'email',
        'password',
        'first_name',
        'last_name',
        'phone',
        'picture',
        'is_verified',
        'verified_email',
        'is_used'
    )

    search_fields = (
        'pk',
        'username',
        'email',
        'first_name',
        'last_name',
        'phone',
    )

    list_filter = (
        'is_verified',
        'verified_email',
        'is_used',
        'created_at',
        'modified_at'
    )

    readonly_fields = (
        'created_at',
        'modified_at'
    )

    actions = ['hash_password']

    def hash_password(self, request, queryset):
        """
        Hash the password if is changed.
        """

        for user in queryset:
            user.password = make_password(user.password)
            user.save()

            return self.message_user(
                request=request,
                message='Password hashed successfully.'
            )


@admin.register(Tokens)
class TokensAdmin(admin.ModelAdmin):
    """
    Admin of the model `Token`.
    """

    list_display = (
        'pk',
        'user',
        'mode',
        'key',
        'secret',
        'is_used',
        'created_at',
        'modified_at'
    )

    list_editable = (
        'mode',
        'key',
        'secret',
        'is_used'
    )

    search_fields = (
        'pk',
        'user',
        'mode'
    )

    list_filter = (
        'mode',
        'is_used',
        'created_at',
        'modified_at'
    )

    readonly_fields = (
        'created_at',
        'modified_at'
    )


@admin.register(Restricts)
class RestrictsAdmin(admin.ModelAdmin):
    """
    Admin of the model `Restricts`.
    """

    list_display = (
        'pk',
        'ip_remote_addr',
        'requests',
        'is_used',
        'created_at',
        'modified_at'
    )

    list_editable = (
        'ip_remote_addr',
        'requests',
        'is_used',
    )

    search_fields = (
        'ip_remote_addr',
    )

    list_filter = (
        'requests',
        'is_used'
    )

    readonly_fields = (
        'created_at',
        'modified_at'
    )


@admin.register(Session)
class SessionStore(admin.ModelAdmin):
    """
    Admin of the model `Session`.
    """

    list_display = (
        'pk',
        'session_key',
        'session_data',
        'expire_date'
    )

    list_editable = (
        'session_key',
        'session_data',
        'expire_date'
    )

    search_fields = (
        'pk',
        'session_key',
        'session_data',
    )

    list_filter = ('expire_date',)

    readonly_fields = ('pk',)

    actions = ['clean_admin_sessions']

    def clean_admin_sessions(self, request, view):
        """
        Clean the admin sessions.
        """

        try:
            if request.user.is_staff:
                request.session.flush()
        except AttributeError:
            return self.message_user(
                request=request,
                message='User isn\'t staff.'
            )
        try:
            if request.user.is_superuser:
                request.session.flush()
        except AttributeError:
            return self.message_user(
                request=request,
                message='User isn\'t superuser.'
            )

        return self.message_user(
            request=request,
            message='Session has been deleted.'
        )


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """
    Admin of the model `LogEntry`.
    """

    list_display = (
        'pk',
        'user_id',
        'object_id',
        'content_type_id',
        'object_repr',
        'change_message',
        'action_flag',
        'action_time'
    )

    list_display_links = (
        'user_id',
        'object_id',
        'content_type_id'
    )

    search_fields = (
        'pk',
        'user_id',
        'object_id',
        'content_type_id'
    )

    list_filter = (
        'action_flag',
        'action_time'
    )
