from django.contrib import admin

from core.models import TwitterAccount


class TwitterAccountAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'username', 'orientation')


admin.site.register(TwitterAccount, TwitterAccountAdmin)
