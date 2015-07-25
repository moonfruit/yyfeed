$(function() {
	var imgs = [];
	$.templates("#itemTemplate").link(".row", {imgs: imgs});

	var $row = $('.row').masonry({
		itemSelector: '.item'
	});

	$.getJSON("/data", function(data) {
		$.each(data.imgs, function(i, item) {
            $.observable(imgs).insert({src: item});
        });

        $row.masonry('reloadItems');

	    $row.imagesLoaded().progress(function() {
		    $row.masonry('layout');
	    });
	});
});
