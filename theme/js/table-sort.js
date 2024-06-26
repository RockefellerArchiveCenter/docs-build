
document.addEventListener('DOMContentLoaded', () => {
  const table = document.querySelector('#docs-list');
  const buttons = table.querySelectorAll('.btn--table-sort');

  buttons.forEach(button => {
      button.addEventListener('click', () => {
          const column = button.closest('th').id;
          const isAscending = table.querySelector(`#${column}`).getAttribute('aria-sort') === 'ascending';
          sortTable(column, !isAscending);
      });
  });

  function sortTable(column, ascending) {
      const tbody = table.querySelector('tbody');
      const rows = Array.from(tbody.rows);
      const columnIndex = [...table.tHead.rows[0].cells].findIndex(th => th.id === column);

      rows.sort((a, b) => {
          let aText = a.cells[columnIndex].textContent;
          let bText = b.cells[columnIndex].textContent;

          // Convert date strings to date objects
          if (column === 'date') {
              aText = new Date(aText);
              bText = new Date(bText);
          }

          return ascending ? aText > bText ? 1 : -1 : aText < bText ? 1 : -1;
      });

      tbody.append(...rows);

      table.querySelectorAll('th').forEach(th => th.setAttribute('aria-sort', ''));
      table.querySelector(`#${column}`).setAttribute('aria-sort', ascending ? 'ascending' : 'descending');
  }

  sortTable('title', true); // Initial sort by title column in ascending order
});
