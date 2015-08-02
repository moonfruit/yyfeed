$(function() {

	'use strict';

	var imgs = [];
	$.templates("#itemTemplate").link(".row", {imgs: imgs});

	var $row = $('.row').masonry({
		itemSelector: '.item'
	});

	var offset = 0;
	getImages = function() {
		console.log("get offset[" + offset + "]")

		url = "/data/images?offset=" + offset
		$.getJSON(url, function(data) {
			$.each(data.imgs, function(i, item) {
				$.observable(imgs).insert({src: item});
			});

			$row.masonry('reloadItems');

			$row.imagesLoaded().progress(function() {
				$row.masonry('layout');
			});

			offset += 30;
		});
	}

	getImages();
	$(window).scroll(function() {
		var scrollHeight = $(document).height();
		var scrollPosition = $(window).height() + $(window).scrollTop();
		if ((scrollHeight - scrollPosition) / scrollHeight === 0) {
			getImages();
		}
	});
});
