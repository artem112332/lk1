const specializations = [
  "Team lead",
  "Backend-разработчик",
  "Frontend-разработчик",
  "Аналитик",
  "Дизайнер"
];
const selectedSpecializationsContainer = document.getElementById('selectedSpecializations');
const specializationsModal = document.getElementById('specializationsModal');

function openSpecializationsModal() {
    renderSpecializationsOptions();
    specializationsModal.style.display = 'block';
}

function closeSpecializationsModal() {
    specializationsModal.style.display = 'none';
    const searchInput = document.getElementById('competencies_search-input');
    searchInput.value = '';
}

function renderSpecializationsOptions() {
    const optionsContainer = document.getElementById('specializationsOptions');
    optionsContainer.innerHTML = '';

    specializations.forEach(specialization => {
        const div = document.createElement('div');
        div.className = 'competency-option';
        div.textContent = specialization;
        div.onclick = () => {
            addSpecializationsToModal(specialization);
            addSpecialization(specialization);
        };
        optionsContainer.appendChild(div);
    });
}

function addSpecialization(name) {
    const alreadyAdded = Array.from(selectedSpecializationsContainer.children).some(child =>
        child.classList.contains('user__competencies_item-value') &&
        child.textContent.trim().startsWith(name)
    );

    if (!alreadyAdded) {
        const div = document.createElement('div');
        div.className = 'user__competencies_item-value';
        div.style.position = 'relative';
        div.style.paddingRight = '20px';
        div.textContent = name;

        const removeBtn = document.createElement('div');
        removeBtn.textContent = '×';
        removeBtn.style.position = 'absolute';
        removeBtn.style.right = '5px';
        removeBtn.style.top = '0';
        removeBtn.style.cursor = 'pointer';
        removeBtn.style.color = '#888';

        removeBtn.onclick = (e) => {
            e.stopPropagation();
            div.remove();
            saveSpecializations();
        };

        div.appendChild(removeBtn);

        const chooseBtn = document.getElementById('specializationsChooseBtn');
        selectedSpecializationsContainer.insertBefore(div, chooseBtn);

        saveSpecializations();
    }
}

function saveSpecializations() {
    const specializations = Array.from(selectedSpecializationsContainer.children)
        .filter(el => el.classList.contains('user__competencies_item-value') && !el.querySelector('input'))
        .map(el => el.textContent.replace('×', '').trim());
    
    localStorage.setItem('savedSpecializations', JSON.stringify(specializations));
}

window.addEventListener('DOMContentLoaded', function() {
    const savedSpecializations = JSON.parse(localStorage.getItem('savedSpecializations') || []);
    savedSpecializations.forEach(specialization => addSpecialization(specialization));
});