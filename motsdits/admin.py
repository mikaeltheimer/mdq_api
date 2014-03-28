from django.contrib import admin
from motsdits.models import Action, Tag, Item, MotDit


class ActionAdmin(admin.ModelAdmin):
    list_display = ['verb', 'approved', 'created']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'approved', 'created']


class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'website', 'approved', 'created']


class MotDitAdmin(admin.ModelAdmin):
    list_display = ['action', 'what', 'where']


admin.site.register(Action, ActionAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(MotDit, MotDitAdmin)
