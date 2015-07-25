$(function() {
	var imgs = [];
	$.templates("#itemTemplate").link(".row", {imgs: imgs});

	var $row = $('.row').masonry({
		itemSelector: '.item'
	});

	var offset = 0;

	getImages = function(offset) {
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
		});
	}

	getImages(offset);
	offset += 30;

	$(window).scroll(function() {
		var scrollHeight = $(document).height();
		var scrollPosition = $(window).height() + $(window).scrollTop();
		if ((scrollHeight - scrollPosition) / scrollHeight === 0) {
			getImages(offset);
			offset += 30;
		}
	});
});
