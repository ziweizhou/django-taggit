from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter
from models import TagBase

class TagNameListFilter(SimpleListFilter):
    # Human-readable title which will be displayed in the
    # right admin sidebar just above the filter options.
    title = _('by tag')

    # Parameter for the filter that will be used in the URL query.
    parameter_name = 'tag'

    def lookups(self, request, model_admin):
        """
        Returns a list of tuples. The first element in each
        tuple is the coded value for the option that will
        appear in the URL query. The second element is the
        human-readable name for the option that will appear
        in the right sidebar.
        """
        
        tags = TagBase.objects.all()
        
        options = []
        for tag in tags:
            options.append((tag.slug, tag.name));
        
        return options

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        return queryset.filter(tags__slug=self.value())
