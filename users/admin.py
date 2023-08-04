from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (
    Student,
    StudentProfile,
    AcademicManager,
    DepartmentHead,
    DataClerk,
    Instructor,
)


# Inline StudentProfile with Student
class StudentProfileInline(admin.StackedInline):
    model = StudentProfile


class AcademicManagerAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


class DepartmentHeadAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


class DataClerkAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


class InstructorAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )


class StudentAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "username",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    inlines = [StudentProfileInline]


# Register the proxy models with the admin interface
admin.site.register(AcademicManager, AcademicManagerAdmin)
admin.site.register(DepartmentHead, DepartmentHeadAdmin)
admin.site.register(DataClerk, DataClerkAdmin)
admin.site.register(Instructor, InstructorAdmin)
admin.site.register(Student, StudentAdmin)
