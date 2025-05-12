document.addEventListener('DOMContentLoaded', function () {
    const table = document.querySelector('.meeting__list');
    const headers = table.querySelectorAll('th');
    const rows = Array.from(table.querySelectorAll('tbody tr'));

    // Функция для сортировки строк по выбранному столбцу
    function sortTable(columnIndex, ascending = true) {
        // Получаем все строки таблицы
        const sortedRows = rows.sort((a, b) => {
            const cellA = a.cells[columnIndex].textContent.trim();
            const cellB = b.cells[columnIndex].textContent.trim();

            let comparison = 0;
            // Если это дата, нужно сравнивать как дату
            if (columnIndex === 0) {
                const dateA = new Date(cellA);
                const dateB = new Date(cellB);
                comparison = dateA - dateB;
            } else if (columnIndex === 2 || columnIndex === 3) { // Время
                const timeA = cellA.split(":").map(Number);
                const timeB = cellB.split(":").map(Number);
                comparison = (timeA[0] * 60 + timeA[1]) - (timeB[0] * 60 + timeB[1]);
            } else {
                comparison = cellA.localeCompare(cellB);
            }

            return ascending ? comparison : -comparison;
        });

        // Переставляем строки в таблице
        sortedRows.forEach(row => table.querySelector('tbody').appendChild(row));
    }

    // Функция для переключения сортировки по каждому заголовку
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

    // Добавляем обработчики кликов на заголовки таблицы
    headers.forEach(header => {
        header.addEventListener('click', toggleSort);
    });
});