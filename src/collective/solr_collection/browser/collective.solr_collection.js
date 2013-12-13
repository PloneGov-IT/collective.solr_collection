/**
 * Patch createWidget to pass also use_solr=true when needed
 */

;(function($) {
	
	$.querywidget.createWidget = function (type, index) {
        var wrapper = $(document.createElement('div'));
		var useSolr = $('#useSolr').is(':checked');
		
        switch (type) {
            case 'StringWidget':
                wrapper.load(portal_url + '/@@archetypes-querywidget-stringwidget');
                break;
            case 'RelativeDateWidget':
                wrapper.load(portal_url + '/@@archetypes-querywidget-relativedatewidget');
                break;
            case 'DateWidget':
                wrapper.load(portal_url + '/@@archetypes-querywidget-datewidget',
                    function(){
                        $(this).find('input')
                            .dateinput().removeClass('date')
                            .change(function(e){
                                $.querywidget.updateSearch();
                            });
                    });
                break;
            case 'DateRangeWidget':
                wrapper.load(portal_url + '/@@archetypes-querywidget-daterangewidget',
                    function(){
                        $(this).find('input')
                            .dateinput().removeClass('date')
                            .change(function(e){
                                $.querywidget.updateSearch();
                            });
                    });
                break;
            case 'ReferenceWidget':
                wrapper.load(portal_url + '/@@archetypes-querywidget-referencewidget');
                break;
            case 'RelativePathWidget':
                wrapper.load(portal_url + '/@@archetypes-querywidget-relativepathwidget');
                break;
            case 'MultipleSelectionWidget':
                wrapper.load(portal_url + '/@@archetypes-querywidget-multipleselectionwidget',
                            {'index': index, 'useSolr:boolean': useSolr?true:''});
                break;
            default:
                wrapper.load(portal_url + '/@@archetypes-querywidget-emptywidget');
                break;
        }
        return wrapper;
		
	}
	
    $.querywidget.updateSearch = function () {
        var base_url = $("base").attr("href");
        var useSolr = $('#useSolr').is(':checked');
        if(base_url.indexOf("portal_factory") != -1) {
            base_url = base_url.split("/").slice(0, -2).join("/");
        }
        var query = base_url + "/@@querybuilder_html_results?";
        var querylist  = [];
        if (useSolr) {
            querylist.push('use_solr:boolean=true');
        }
        else {
            querylist.push('use_solr:boolean=');
        }
        var items = $('.ArchetypesQueryWidget .queryindex');
        if (!items.length) {
            return;
        }
        items.each(function () {
            var results = $(this).parents('.criteria').children('.queryresults');
            var index = $(this).val();
            var operator = $(this).parents('.criteria').children('.queryoperator').val();
            var widget = $.querywidget.config.indexes[index].operators[operator].widget;
            var querywidget = $(this).parents('.criteria').find('.querywidget');
            querylist.push('query.i:records=' + index);
            querylist.push('query.o:records=' + operator);

            function getDateWidgetValue(obj) {
                // Get values from the date widget instead of the field itself, as the value
                // of the field isn't yet updated at this point in the "change" event.
                value = (obj.data('dateinput') && obj.data('dateinput').getValue('mm/dd/yyyy')) || '';
                return value;
            }

            switch (widget) {
                case 'DateWidget':
                    value = getDateWidgetValue($(this).parents('.criteria').find('.queryvalue'));
                    if (value) {
                        querylist.push('query.v:records=' + value);
                    }
                    break;
                case 'DateRangeWidget':
                    start_date = getDateWidgetValue($(querywidget.children('input')[0]));
                    end_date = getDateWidgetValue($(querywidget.children('input')[1]));

                    querylist.push('query.v:records:list=' + start_date);
                    querylist.push('query.v:records:list=' + end_date);
                    break;
                case 'MultipleSelectionWidget':
                    querywidget.find('input:checked').each(function () {
                        querylist.push('query.v:records:list=' + $(this).val());
                    });
                    break;
                default:
                    value = $(this).parents('.criteria').find('.queryvalue').val();
                    push_string = 'query.v:records=';
                    if (value) {
                        push_string = push_string + value;
                    }
                    querylist.push(push_string);
                    break;
            }
            if (querylist.length){
                $.get(portal_url + '/@@querybuildernumberofresults?' + querylist.join('&'),
                      {},
                      function (data) { results.html(data); });
            }
        });
        query += querylist.join('&');
        query += '&sort_on=' + $('#sort_on').val();
        if ($('#sort_order:checked').length > 0) {
            query += '&sort_order=reverse';
        }
        $.get(query, {}, function (data) { $('.ArchetypesQueryWidget .previewresults').html(data); });
    };
})(jQuery);

$(document).ready(function(){
    $("input#useSolr").change(function(event) {
        $.querywidget.updateSearch();
    });
});
