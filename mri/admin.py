from django.contrib import admin

# Register your models here.
from .models import MRIImage
from django.contrib.auth.admin import UserAdmin
from .models import Hospital

admin.site.register(MRIImage)


# class HospitalAdmin(UserAdmin):
#     list_display = ("name", "email", "phone_number", "is_active", "is_staff")
#     search_fields = ("name", "email")
#     ordering = ("name",)
#     fieldsets = (
#         (None, {"fields": ("name", "email", "password")}),
#         ("Hospital Info", {"fields": ("address", "phone_number")}),
#         ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
#     )
#     add_fieldsets = (
#         (None, {
#             "classes": ("wide",),
#             "fields": ("name", "email", "password1", "password2"),
#         }),
#     )

admin.site.register(Hospital)