document.addEventListener('DOMContentLoaded', function () {
    const searchInput = document.getElementById('competencies_search-input');
    const resultsBox = document.getElementById('competencySearchResults');
    const optionsContainer = document.getElementById('competencyOptions');

    searchInput.addEventListener('input', function () {
        const query = this.value.trim().toLowerCase();
        const options = optionsContainer.querySelectorAll('.competency-option');
        resultsBox.innerHTML = '';

        if (query === '') {
            resultsBox.style.display = 'none';
            return;
        }

        let found = 0;

        options.forEach(option => {
            const text = option.textContent.trim().toLowerCase();
            if (text.includes(query)) {
                const clone = option.cloneNode(true);
                resultsBox.appendChild(clone);
                found++;
            }
        });

        resultsBox.style.display = found > 0 ? 'block' : 'none';
    });
});