document.addEventListener('DOMContentLoaded', function () {
    const filterIcon = document.querySelector('.column-filter');
    const modal = document.getElementById('column-modal');
    const closeModalButton = document.getElementById('close-modal');
    const form = document.getElementById('column-filter-form');
    const table = document.querySelector('.meeting__list');
    const headers = table.querySelectorAll('th');
    const rows = Array.from(table.querySelectorAll('tbody tr'));

    filterIcon.addEventListener('click', function() {
        modal.style.display = 'block';
    });

    closeModalButton.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        const checkedColumns = Array.from(form.querySelectorAll('input[name="column"]:checked')).map(input => input.value);

        headers.forEach((header, index) => {
            if (!checkedColumns.includes(index.toString())) {
                header.classList.add('hidden');
                Array.from(table.querySelectorAll('tbody tr')).forEach(row => {
                    row.cells[index].classList.add('hidden');
                });
            } else {
                header.classList.remove('hidden');
                Array.from(table.querySelectorAll('tbody tr')).forEach(row => {
                    row.cells[index].classList.remove('hidden');
                });
            }
        });

        modal.style.display = 'none';
    });
});