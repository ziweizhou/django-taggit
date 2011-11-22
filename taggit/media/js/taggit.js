(function($) {
	
	var taggitPrefix = '/';
	
	var scripts = document.getElementsByTagName('SCRIPT');
	for (var i = 0; i < scripts.length; i++) {
		var src = scripts[i].getAttribute('src');
		if (typeof src == 'string' && src.length) {
			var matches = src.match(/^(.+\/)static\/js\/taggit\.js/);
			if (matches) {
				taggitPrefix = matches[1];
			}
		}
	}
	
	function split(val) {
		return val.split(/,\s*/);
	}
	
	function extractLast(term) {
		return split(term).pop();
	}
	
	$(document).ready(function() {
		$.getJSON(taggitPrefix + 'ajax', {}, function(data) {
			var availableTags = [];
			for(var i=0; i < data.length; i++){
				availableTags.push(data[i].fields.name);
			}
			if ($.ui && $.ui.autocomplete && $.ui.autocomplete.filter) {
				$('input.taggit-tags')
				// don't navigate away from the field on tab when selecting an item
				.bind("keydown", function(event) {
					if (event.keyCode === $.ui.keyCode.TAB &&
							$(this).data("autocomplete").menu.active) {
						event.preventDefault();
					}
				})
				.autocomplete({
					minLength: 0,
					source: function(request, response) {
						// delegate back to autocomplete, but extract the last term
						response($.ui.autocomplete.filter(
							availableTags, extractLast(request.term)));
					},
					focus: function() {
						// prevent value inserted on focus
						return false;
					},
					select: function(event, ui) {
						var terms = split(this.value);
						// remove the current input
						terms.pop();
						// add the selected item
						terms.push(ui.item.value);
						// add placeholder to get the comma-and-space at the end
						terms.push("");
						this.value = terms.join(", ");
						return false;
					}
				});				
			} else {
				$('input.taggit-tags').autocomplete({
					source: availableTags
				});
			}

		});
	});
})((typeof window.django != 'undefined') ? django.jQuery : jQuery);