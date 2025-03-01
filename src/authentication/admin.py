from django.contrib import admin


from .models import UserToken


@admin.register(UserToken)
class TokenAdmin(admin.ModelAdmin):

    list_display = ('key', 'user', 'created')
    def has_delete_permission(self, request, obj=None):
        return True
    
    def has_change_permission(self, request, obj=None):
        return False
    
    def has_add_permission(self, request, obj=None):
        return True
