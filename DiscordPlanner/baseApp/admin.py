from django.contrib import admin
from .models import User, Guild


class GuildAdmin(admin.ModelAdmin):
    pass


class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(Guild, GuildAdmin)
admin.site.register(User, UserAdmin)
