(function ($) {
  const mobileSmall = window.matchMedia('(max-width: 580px)')
  // Side navigation toggle
  $(function () {
    $('#toc-nav-toggle').on('click', function (e) {
      if ($(this).siblings('#toc__link-group').is(':visible')) {
        $(this).html('Open Page Menu')
        $(this).attr('aria-expanded', 'false')
      } else {
        $(this).html('Close Page Menu')
        $(this).attr('aria-expanded', 'true')
      }
      $(this).siblings('#toc__link-group').toggle()
      e.stopPropagation()
    })
    $('html').click(function () {
      if (mobileSmall.matches) {
        $('#toc__link-group').hide()
        $('#toc__link-group').siblings('#toc-nav-toggle').html('Open Page Menu')
      } else {
        // allow keyboard focus
        $('#toc__link-group button').attr('tabindex', '0')
      }
    })
  })
})(jQuery)
