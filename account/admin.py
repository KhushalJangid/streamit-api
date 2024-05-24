from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.sessions.models import Session
from import_export.admin import ExportActionMixin,ExportActionModelAdmin,ImportExportMixin
from .models import *
from import_export import resources
from import_export.widgets import ForeignKeyWidget,DateTimeWidget
from import_export import fields
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"
    
class AccountResource(resources.ModelResource):
    first_name = fields.Field(
        column_name='First Name',
        attribute='first_name',)
    last_name = fields.Field(
        column_name='Last Name',
        attribute='last_name',)
    email = fields.Field(
        column_name='Email',
        attribute='email',)
    phone = fields.Field(
        column_name='Phone No',
        attribute='phone',)
    dob = fields.Field(
        column_name='Date of Birth',
        attribute='dob',)
    address = fields.Field(
        column_name='Address',
        attribute='address',)
    published = fields.Field(
        column_name='Registered On',
        attribute='date_joined', 
        widget=DateTimeWidget(format='%d %b, %Y, %-I:%M %p'))   
    class Meta:
        model = User
        fields = ['first_name','last_name','email','rollno','phone','dob','address','published'] 

class AccountAdmin(ExportActionMixin,UserAdmin):
    # add_form = UserCreateForm
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': (
    #               'email',
    #               'password1',
    #               'password2' 
    #               ),
    #     }),
    # )
    
    list_display=('id','first_name','last_name','email','last_login')
    search_fields = ["email","id","first_name"]
    readonly_fields = ['id',"date_joined","last_login"]
    # autocomplete_fields = ["email"]
    filter_horizontal = ()
    list_filter = UserAdmin.list_filter
    fieldsets = ()
    ordering =()
    resource_class = AccountResource


# class SessionAdmin(admin.ModelAdmin):
#     def _session_data(self, obj):
#         return obj.get_decoded()
#     list_display = ['session_key', '_session_data', 'expire_date']


# admin.site.register(Session, SessionAdmin)
admin.site.register(User,AccountAdmin)
