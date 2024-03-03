from django.contrib import admin
from .models import Interest, JobTitle, UserProfile, EmploymentHistory
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class EmploymentHistoryInline(admin.StackedInline):
    model = EmploymentHistory
    extra = 1
    can_delete = False
    verbose_name_plural = 'employment history'


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'user profile'


class UserAdmin(BaseUserAdmin):
    model = User
    inlines = [UserProfileInline, EmploymentHistoryInline]

# Unregister initial User so we can update the modified User for admin
admin.site.unregister(User)
admin.site.unregister(Group)
# Reregister User and profile
admin.site.register(User, UserAdmin)

# register the UserProfileAdmin that will display the employment history included

admin.site.register(Interest)
admin.site.register(JobTitle)
admin.site.register(EmploymentHistory)