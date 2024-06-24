document.addEventListener('DOMContentLoaded', function() {
  let lastScrollPosition = window.scrollY;
  let ticking = false; //Used to throttle scroll events

  window.addEventListener('scroll', function() {
    lastScrollPosition = window.scrollY; // Update scroll position

    if (!ticking) {
      // Throttle scroll event using requestAnimationFrame
      window.requestAnimationFrame(function() {
        updateActiveLink(lastScrollPosition);
        ticking = false; //Reset ticking after active link update
      });
    }
    // Set ticking to true to indicate scroll event is being handled
    ticking = true;
  });

  function updateActiveLink(scrollPosition) {
    const headers = document.querySelectorAll('h2');
    const tocLinkItems = document.querySelectorAll('#current > a.toc__link-item'); // Select all TOC links

    let currentHeader;
    let scrollingDown = scrollPosition > lastScrollPosition;

    // Iterate through all headers to find the current active header
    for (let i = 0; i < headers.length; i++) {
      const header = headers[i];

      // If scrolling down, find the next header coming into view
      if (scrollingDown) {
        if (header.offsetTop + header.outerHeight > scrollPosition && header.offsetTop < scrollPosition + window.innerHeight) {
          currentHeader = header;
          break;
        }
      // If scrolling up, find the header going out of view
      } else {
        if (header.offsetTop <= scrollPosition + window.innerHeight) {
          currentHeader = header;
        } else {
          break;
        }
      }
    }

    // Determine if any TOC link should be active
    let anyLinkActive = false; // Used to check if there is an active link

    // Update the active state of TOC links based on currentHeader
    for (let i = 0; i < tocLinkItems.length; i++) {
      const tocLinkItem = tocLinkItems[i];
      tocLinkItem.classList.remove('active');

      if (currentHeader && tocLinkItem.getAttribute('href') === '#' + currentHeader.id) {
        tocLinkItem.classList.add('active');
        anyLinkActive = true; // Mark that there is an active link
      }
    }

    // If no link is active, keep the last link active (handle scrolling to bottom of page)
    if (!anyLinkActive) {
      tocLinkItems[tocLinkItems.length - 1].classList.add('active');
    }

    lastScrollPosition = scrollPosition; // Update last scroll position
  }
});