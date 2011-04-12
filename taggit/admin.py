from django.contrib import admin

from taggit.models import Tag, TaggedItem


class TaggedItemInline(admin.StackedInline):
    model = TaggedItem
    extra = 0

class TagAdmin(admin.ModelAdmin):
    inlines = [
        TaggedItemInline
    ]
    ordering = ['name']
    search_fields = ['name']

admin.site.register(Tag, TagAdmin)