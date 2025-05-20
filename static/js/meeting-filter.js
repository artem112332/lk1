document.addEventListener('DOMContentLoaded', function () {
    const table = document.querySelector('.meeting__list') || document.querySelector('.event__list');
    const headers = table.querySelectorAll('th');
    const rows = Array.from(table.querySelectorAll('tbody tr'));

    function parseDate(str) {
        const [day, month, year] = str.split(".").map(Number);
        return new Date(year, month - 1, day);
    }

    function sortTable(columnIndex, ascending = true) {
        const sortedRows = rows.sort((a, b) => {
            const cellA = a.cells[columnIndex].textContent.trim();
            const cellB = b.cells[columnIndex].textContent.trim();

            let comparison = 0;
            if (columnIndex === 0) {
                const dateA = parseDate(cellA);
                const dateB = parseDate(cellB);
                comparison = dateA - dateB;
            } else if (columnIndex === 2 || columnIndex === 3) {
                const timeA = cellA.split(":").map(Number);
                const timeB = cellB.split(":").map(Number);
                comparison = (timeA[0] * 60 + timeA[1]) - (timeB[0] * 60 + timeB[1]);
            } else {
                comparison = cellA.localeCompare(cellB, 'ru', { numeric: true });
            }

            return ascending ? comparison : -comparison;
        });

        sortedRows.forEach(row => table.querySelector('tbody').appendChild(row));
    }


    function toggleSort(event) {
        if (event.target.classList.contains('sort-data')) {
            const columnIndex = Array.from(headers).indexOf(event.target.closest('th'));
            const currentClass = event.target.classList;

            let ascending = !currentClass.contains('sorted-asc');
            currentClass.remove('sorted-asc', 'sorted-desc');
            if (ascending) {
                currentClass.add('sorted-asc');
            } else {
                currentClass.add('sorted-desc');
            }

            sortTable(columnIndex, ascending);
        }
    }

    headers.forEach(header => {
        header.addEventListener('click', toggleSort);
    });
});