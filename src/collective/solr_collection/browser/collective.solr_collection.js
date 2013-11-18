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
	
})(jQuery);


