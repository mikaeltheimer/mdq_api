from django.contrib import admin
from motsdits.models import Action, Tag, Item, MotDit, Photo, Story, News, Comment


class ActionAdmin(admin.ModelAdmin):
    list_display = ['verb', 'approved', 'created']


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'approved', 'created']


class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'website', 'approved', 'created']


class MotDitAdmin(admin.ModelAdmin):
    list_display = ['action', 'what', 'where']


class PhotoAdmin(admin.ModelAdmin):
    list_display = ['picture', 'motdit', 'created_by']


class StoryAdmin(admin.ModelAdmin):
    list_display = ['teaser', 'motdit', 'created_by']


class NewsAdmin(admin.ModelAdmin):
    list_display = ['action', 'motdit', 'photo', 'story', 'created_by']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['teaser', 'news_item', 'created_by']

admin.site.register(Action, ActionAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(MotDit, MotDitAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Story, StoryAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Comment, CommentAdmin)
