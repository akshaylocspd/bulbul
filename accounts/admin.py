from django.contrib.auth.admin import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class MyModelAdmin(admin.ModelAdmin):
    def get_model_perms(self, request):
        """
        Return empty perms dict thus hiding the model from admin index.
        """
        return {}


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'number', 'nameUser',  'about_you','bio','forum_posts', 'photos_added', 'favorites')
    search_fields = ('username', 'email', 'number', 'nameUser',)
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'number', 'nameUser',  'profile_image','my_images','my_status_images','about_you','bio', 'forum_posts', 'photos_added', 'favorites')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'number', 'nameUser',  'profile_image','my_images','my_status_images','about_you','bio', 'forum_posts', 'photos_added', 'favorites', 'password1', 'password2'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PhoneNumber)

admin.site.register(MyStatusImages)
# admin.site.register(ProfileImage)
admin.site.register(MyImages)

# admin.site.register(MyStatusImages,MyModelAdmin)
# admin.site.register(ProfileImage,MyModelAdmin)
# admin.site.register(MyImages,MyModelAdmin)

