document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('search-input');
    const table = document.querySelector('.meeting__list') || document.querySelector('.event__list');
    const rows = Array.from(table.querySelectorAll('tbody tr'));

    function clearHighlights(row) {
        const cells = row.querySelectorAll('td');
        cells.forEach(cell => {
            cell.innerHTML = cell.textContent;
        });
    }

    function highlightText(text, query) {
        const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
        const regex = new RegExp(`(${escapedQuery})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }

    function searchTable(query) {
        const trimmedQuery = query.trim();

        rows.forEach(row => {
            clearHighlights(row);

            const cells = Array.from(row.getElementsByTagName('td'));
            let matchFound = false;

            if (trimmedQuery === '') {
                row.classList.remove('hidden');
                return;
            }

            cells.forEach(cell => {
                const originalText = cell.textContent;
                const lowerText = originalText.toLowerCase();

                if (lowerText.includes(trimmedQuery.toLowerCase())) {
                    matchFound = true;
                    cell.innerHTML = highlightText(originalText, trimmedQuery);
                }
            });

            // row.classList.toggle('hidden', !matchFound);
        });
    }

    searchInput.addEventListener('input', function (event) {
        const query = event.target.value;
        searchTable(query);
    });




    
    const searchFilterToggleBtn = document.getElementById('search-filter-toggle');
    let btnToggled = false;

    searchFilterToggleBtn.addEventListener('click', function () {
        btnToggled = !btnToggled;
        searchFilterToggleBtn.classList.toggle('active', btnToggled);
        const query = searchInput.value.trim();

        rows.forEach(row => {
            clearHighlights(row);

            const cells = Array.from(row.getElementsByTagName('td'));
            let matchFound = false;

            cells.forEach(cell => {
                const originalText = cell.textContent;
                const lowerText = originalText.toLowerCase();

                if (lowerText.includes(query.toLowerCase())) {
                    matchFound = true;
                    cell.innerHTML = highlightText(originalText, query);
                }
            });

            if (btnToggled) {
                row.classList.toggle('hidden', !matchFound);
            } else {
                row.classList.remove('hidden');
            }
        });
    });
});