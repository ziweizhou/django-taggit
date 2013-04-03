# coding: utf-8
import os

from django import forms
from django.utils.translation import ugettext as _

from taggit.utils import parse_tags, edit_string_for_tags


class TagWidget(forms.TextInput):

    def __init__(self, attrs=None):
        if attrs is not None:
            self.attrs = attrs.copy()
        else:
            self.attrs = {'class': 'taggit-tags'}

    def get_media(self):
        """
        A method used to dynamically generate the media property,
        since we may not have the urls ready at the time of import,
        and then the reverse() call would fail.
        """
        from django.forms.widgets import Media as _Media
        from django.core.urlresolvers import NoReverseMatch, reverse
        try:
            media_url = reverse('taggit-static', kwargs={'path': ''})
        except NoReverseMatch:
            media_url = None
        if media_url is None:
            class_props = {}
        else:
            class_props = {
                'css': {
                    'all': (
                        os.path.join(media_url, 'css', 'autocomplete.css'),
                    )
                },
                'js': (
                    os.path.join(media_url, 'js', 'taggit.js'),
                )
            }
        media_cls = type('Media', (_Media,), class_props)
        return _Media(media_cls)

    media = property(get_media)

    def render(self, name, value, attrs=None):
        if value is not None and not isinstance(value, basestring):
            value = edit_string_for_tags([o.tag for o in value.select_related("tag")])
        return super(TagWidget, self).render(name, value, attrs)

    def _has_changed(self, initial, data):
        """
        Called by BaseForm._get_changed_data, which sends this the form's initial value
        for the field and the raw value that was submitted to the form, *before it has
        been through any clean() methods.*

        This means that the initial data will (usually) be a related Tag manager, while
        the raw data will (usually) be a string. So, they're both converted to strings
        before sending them to the regular change comparison.
        """

        if initial is not None and not isinstance(initial, basestring):
            initial = edit_string_for_tags([o.tag for o in initial.select_related("tag")])

        if data is not None and not isinstance(data, basestring):
            data = edit_string_for_tags([o.tag for o in data.select_related("tag")])

        return super(TagWidget, self)._has_changed(initial, data)


class TagField(forms.CharField):

    widget = TagWidget

    def clean(self, value):
        value = super(TagField, self).clean(value)
        try:
            return parse_tags(value)
        except ValueError:
            raise forms.ValidationError(_("Please provide a comma-separated list of tags."))
