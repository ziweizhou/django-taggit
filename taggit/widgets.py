from django import forms
from django.core.urlresolvers import reverse
from django.conf import settings
from django.utils.html import escapejs
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _, ugettext

from utils import edit_string_for_tags

class TagAutocomplete(forms.TextInput):
    input_type = 'text'
    
    def render(self, name, value, attrs=None):
        list_view = reverse('taggit-list')
        if value is not None and not isinstance(value, basestring):
            value = edit_string_for_tags(
              [o.tag for o in value.select_related("tag")]
            )
        html = super(TagAutocomplete, self).render(
            name+"_dummy",
            u'',
            attrs
        )
        js = u'<script type="text/javascript">jQuery = django.jQuery; '
            'jQuery().ready(function() { jQuery("#%s").autoSuggest("%s", '
            '{startText: "%s", preFill: "%s"}); });</script>'
            % (attrs['id'], list_view, _("Enter Tag Here"),
                escapejs(value) if value else u'')
        return mark_safe("\n".join([html, js]))
    
    class Media:
        js_base_url = getattr(
            settings,
            'TAGGIT_AUTOCOMPLETE_JS_BASE_URL',
            '%sjquery-autocomplete' % settings.STATIC_URL)
        css = {
            'all': ('%s/css/autoSuggest.css' % js_base_url,)
        }
        js = (
            '%s/js/jquery.autoSuggest.minified.js' % js_base_url,
        )
