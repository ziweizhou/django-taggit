import os
from django import forms
from django.utils.translation import ugettext as _

from taggit.utils import parse_tags, edit_string_for_tags

class TagWidget(forms.TextInput):
	
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
		if attrs is None:
			attrs = {}
		attrs.update({'class': 'taggit-tags'})
		return super(TagWidget, self).render(name, value, attrs)

	def _has_changed(self, initial, data):
		try:
			if len(initial) == 0 and len(data) == 0:
				return False
		except TypeError, ValueError:
			pass
		return super(TagWidget, self)._has_changed(initial, data)

class TagField(forms.CharField):
	widget = TagWidget

	def clean(self, value):
		value = super(TagField, self).clean(value)
		try:
			return parse_tags(value)
		except ValueError:
			raise forms.ValidationError(_("Please provide a comma-separated list of tags."))
