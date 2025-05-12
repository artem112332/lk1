document.addEventListener('DOMContentLoaded', function () {
    const filterIcon = document.querySelector('.column-filter'); // Картинка фильтра
    const modal = document.getElementById('column-modal'); // Модальное окно
    const closeModalButton = document.getElementById('close-modal'); // Кнопка закрытия окна
    const form = document.getElementById('column-filter-form'); // Форма с чекбоксами
    const table = document.querySelector('.meeting__list'); // Таблица
    const headers = table.querySelectorAll('th');
    const rows = Array.from(table.querySelectorAll('tbody tr'));

    // Открытие модального окна при клике на фильтр
    filterIcon.addEventListener('click', function() {
        modal.style.display = 'block';
    });

    // Закрытие модального окна
    closeModalButton.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Применение выбранных колонок
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Скрытие или отображение колонок в таблице в зависимости от чекбоксов
        const checkedColumns = Array.from(form.querySelectorAll('input[name="column"]:checked')).map(input => input.value);

        // Для каждого столбца проверяем, выбран ли он
        headers.forEach((header, index) => {
            if (!checkedColumns.includes(index.toString())) {
                // Если колонка не выбрана, скрыть ее
                header.classList.add('hidden');
                Array.from(table.querySelectorAll('tbody tr')).forEach(row => {
                    row.cells[index].classList.add('hidden');
                });
            } else {
                // Если колонка выбрана, показать ее
                header.classList.remove('hidden');
                Array.from(table.querySelectorAll('tbody tr')).forEach(row => {
                    row.cells[index].classList.remove('hidden');
                });
            }
        });

        modal.style.display = 'none';
    });
});