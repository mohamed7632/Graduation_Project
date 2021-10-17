from django.contrib import admin
from .models import Topic,CustomUser
from .forms import CustomUserForm
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model=CustomUser
    add_form=CustomUserForm

    fieldsets=(
        *UserAdmin.fieldsets,
        (
            'User data',
            {
              'fields':(
                  'job_title',
                  'phone_number',
                  'age',
                  'gender',
                  'topics'
              )
            }
        )
    )
admin.site.register(Topic)
admin.site.register(CustomUser,CustomUserAdmin)
