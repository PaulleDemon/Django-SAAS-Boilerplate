from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth.models import Group

from unfold.admin import ModelAdmin
from unfold.forms import UserCreationForm, UserChangeForm

from .models import User
from .admingroupform import GroupAdminForm

# Unregister the original Group admin.
admin.site.unregister(Group)

# Create a new Group admin.
@admin.register(Group)
class GroupAdmin(ModelAdmin):
    # Use our custom form.
    form = GroupAdminForm
    # Filter permissions horizontal as well.
    filter_horizontal = ['permissions']

# Register the new Group ModelAdmin.


class CustomUserCreationForm(UserCreationForm, ModelAdmin):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ()


class CustomUserChangeForm(UserChangeForm, ModelAdmin):

    class Meta(UserChangeForm.Meta):
        model = User
        # fields = ('name', )



@admin.register(User)
class CustomUserAdmin(UserAdmin, ModelAdmin):

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ['email', 'name', 'id', 'is_active', 'is_staff', 'is_admin']
    list_filter = ['date_joined', 'last_login', 'is_active', 'is_staff', 'is_admin']

    ordering = ['-date_joined']
    readonly_fields = ['id', 'date_joined', 'last_login']

    fieldsets = (
        ('User details', {'fields': ('id', 'email', 'name',  "dp", 
                                     'date_joined', 
                                     'password')}), # displays hashed password
        ('Status', {'fields': ('is_active', 'is_staff', 'is_admin', 'is_superuser')}),
        ('Authorization groups', {'fields': ('groups', 'user_permissions')}),
        ('Login', {'fields': ('last_login', )}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    list_editable = ['is_active',]
    search_fields = ['name', 'email']

    readonly_fields = ['id', 'date_joined']
    
    def get_readonly_fields(self, request, obj=None):
        
        if 'last_login' not in self.readonly_fields:
            self.readonly_fields.append('last_login')
        
        return self.readonly_fields
    
    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj=obj, change=change, **kwargs)
        # print("change: ", change, obj)
        if change and "is_active" in form.base_fields:
            form.base_fields["is_active"].help_text = "If the user is inactive, they cannot login to any login forms. Even if active, they still won't be able to access admin panel."
            form.base_fields["is_staff"].help_text = "Indicates that the user is staff and can login to admin dashboards, but needs to have explicit permissions to access other areas."
            form.base_fields["is_admin"].help_text = "Indicates that the user is staff and admin and can login to admin dashboards, has special permissions for such as blogs, but needs to have explicit permissions to access other areas."
        return form