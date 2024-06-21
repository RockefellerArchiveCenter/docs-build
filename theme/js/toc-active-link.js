document.addEventListener('DOMContentLoaded', function() {
  window.addEventListener('scroll', function() {
    var scrollPosition = window.scrollY;
    var headers = 'h2'; // Define headers as 'h2'

    // Find the next header that comes into view
    var nextHeader = null;
    var headers = document.querySelectorAll(headers);
    for (var i = 0; i < headers.length; i++) {
      var header = headers[i];
      var headerOffset = header.offsetTop;
      var headerHeight = header.offsetHeight;
      if (headerOffset + headerHeight > scrollPosition && headerOffset < scrollPosition + window.innerHeight) {
        nextHeader = header;
        break;
      }
    }

    var tocLinkItems = document.querySelectorAll('#current > a.toc__link-item'); // Get all the TOC header links

    // Check if the user has scrolled to the bottom of the page
    if ((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {
      for (var i = 0; i < tocLinkItems.length; i++) {
        tocLinkItems[i].classList.remove('active');
      }
      tocLinkItems[tocLinkItems.length - 1].classList.add('active'); // Activate the last TOC link item
    } else {
      // If there's a next header
      if (nextHeader) {
        var newActiveLinkId = nextHeader.id;
        for (var i = 0; i < tocLinkItems.length; i++) {
          var tocLinkItem = tocLinkItems[i];
          tocLinkItem.classList.remove('active');
          if (tocLinkItem.getAttribute('href') === '#' + newActiveLinkId) {
            tocLinkItem.classList.add('active');
          }
        }
      }
    }
  });
});
