(function($){
  $.fn.toc = function(options) {
    var defaults = {
      noBackToTopLinks: false,
      title: '',
      minimumHeaders: 1,
      headers: 'h2',
      listType: 'ul', // values: [ol|ul]
      showEffect: 'slideDown', // values: [show|slideDown|fadeIn|none]
      showSpeed: '200', // set to 0 to deactivate effect
    },
    settings = $.extend(defaults, options);

    function fixedEncodeURIComponent (str) {
      return encodeURIComponent(str).replace(/[!'()*]/g, function(c) {
        return '%' + c.charCodeAt(0).toString(16);
      });
    }

    function createLink (header) {
      var innerText = (header.textContent === undefined) ? header.innerText : header.textContent;
      return "<a class='toc__link-item' id='toc-link' href='#" + fixedEncodeURIComponent(header.id) + "' >" + innerText + "</a>";
    }

    var headers = $(settings.headers).filter(function() {
      // get all headers with an ID
      var previousSiblingName = $(this).prev().attr( "name" );
      if (!this.id && previousSiblingName) {
        this.id = $(this).attr( "id", previousSiblingName.replace(/\./g, "-") );
      }
      return this.id;
    }), output = $(this);
    if (!headers.length || headers.length < settings.minimumHeaders || !output.length) {
      $(this).hide();
      return;
    }

    if (0 === settings.showSpeed) {
      settings.showEffect = 'none';
    }

    var render = {
      show: function() { output.hide().html(html).show(settings.showSpeed); },
      slideDown: function() { output.hide().html(html).slideDown(settings.showSpeed); },
      fadeIn: function() { output.hide().html(html).fadeIn(settings.showSpeed); },
      none: function() { output.html(html); }
    };

    var get_level = function(ele) { return parseInt(ele.nodeName.replace("H", ""), 10); };
    var highest_level = headers.map(function(_, ele) { return get_level(ele); }).get().sort()[0];
    var return_to_top = '<i class="icon-arrow-up back-to-top"> </i>';

    var level = get_level(headers[0]),
      this_level,
      html = "";
    headers.on('click', function() {
      if (!settings.noBackToTopLinks) {
        window.location.hash = this.id;
      }
    })
    .each(function(_, header) {
      this_level = get_level(header);
      if (!settings.noBackToTopLinks && this_level === highest_level) {
        $(header).addClass('top-level-header').after(return_to_top);
      }
      html += createLink(header);
      level = this_level; // update for the next one
    });
    if (!settings.noBackToTopLinks) {
      $(document).on('click', '.back-to-top', function() {
        $(window).scrollTop(0);
        window.location.hash = '';
      });
    }

    render[settings.showEffect]();

    var tocLinkItems = $('#current > a.toc__link-item'); // Get all the TOC header links
    var activeLink = null; // Store the currently active TOC link

    $(window).on('scroll', function() {
      var scrollPosition = $(window).scrollTop();

      // Find the next header that comes into view
      var nextHeader = null;
      headers.each(function(_, header) {
        var headerOffset = $(header).offset().top;
        var headerHeight = $(header).outerHeight();
        if (headerOffset + headerHeight > scrollPosition && headerOffset < scrollPosition + $(window).height()) {
          nextHeader = header;
          return false; // Exit the loop once next header is found
        }
      });

      // If there's a next header
      if (nextHeader) {
        var newActiveLinkId = $(nextHeader).attr('id');
        if (newActiveLinkId !== activeLink) {
          // Remove active class from previously active TOC link
          tocLinkItems.removeClass('active');
          // Add active class to the corresponding TOC link
          tocLinkItems.filter('[href="#' + newActiveLinkId + '"]').addClass('active');
          activeLink = newActiveLinkId; // Update active link ID
        }
      }
    });
  };
})(jQuery);
