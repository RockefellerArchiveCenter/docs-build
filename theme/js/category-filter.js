document.addEventListener('DOMContentLoaded', function() {
  // Get the filter button and all radio buttons
  const filterButton = document.getElementById('filter-submit');
  const radioButtons = document.querySelectorAll('input[name="category"]');

  // Get all document cards and the container for the list of documents
  const documents = document.querySelectorAll('.card');
  const docsList = document.querySelector('.card-list');

  // Add an event listener to the filter button to handle the click event
  filterButton.addEventListener('click', function(event) {
    event.preventDefault();  // Prevent the default form submission

    let selectedCategory;
    // Find the checked radio button and get its value
    radioButtons.forEach(function(radio) {
      if (radio.checked) {
        selectedCategory = radio.value;
      }
    });

    // Filter the documents based on the selected category
    let filteredDocs = Array.from(documents).filter(function(doc) {
      // Get the categories of the current document
      const categories = Array.from(doc.querySelectorAll('.category')).map(el => el.textContent.toLowerCase());
      // Check if the document belongs to the selected category
      return selectedCategory === 'all categories' || categories.includes(selectedCategory.toLowerCase());
    });

    // Map filtered documents to an array of objects containing title and element
    let docsWithTitles = filteredDocs.map(function(doc) {
      return {
        title: doc.querySelector('.card__title').textContent.trim().toLowerCase(),
        element: doc
      };
    });

    // Sort the documents by title
    docsWithTitles.sort(function(a, b) {
      if (a.title < b.title) {
        return -1;
      }
      if (a.title > b.title) {
        return 1;
      }
      return 0;
    });

    // Clear the current document list
    docsList.innerHTML = '';

    // Append the sorted documents back to the document list
    docsWithTitles.forEach(function(docWithTitle) {
      docsList.appendChild(docWithTitle.element);
    });
  });
});



