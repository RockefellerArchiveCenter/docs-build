(function ($) {
  const mobileSmall = window.matchMedia('(max-width: 580px)')
  // Side navigation toggle
  $(function () {
    $('#toc-nav-toggle').on('click', function (e) {
      if ($(this).siblings('#toc-link-group').is(':visible')) {
        $(this).html('Open Page Menu')
        $(this).attr('aria-expanded', 'false')
      } else {
        $(this).html('Close Page Menu')
        $(this).attr('aria-expanded', 'true')
      }
      $(this).siblings('#toc-link-group').toggle()
      e.stopPropagation()
    })
    $('html').click(function () {
      if (mobileSmall.matches) {
        $('#toc-link-group').hide()
        $('#toc-link-group').siblings('#toc-nav-toggle').html('Open Page Menu')
      } else {
        // allow keyboard focus
        $('#toc-link-group button').attr('tabindex', '0')
      }
    })
  })
})(jQuery)
