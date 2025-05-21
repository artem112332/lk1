const competencies = [
  "Project Manager",
  "Аналитик",
  "UX/UI",
  "Frontend",
  "Backend",
  "Мобильная разработка",
  "DevOps",
  "ML разработка",
  "Тестировщик",
  "Системный архитектор",
  "Data Engineer",
  "Data Scientist",
  "Product Manager",
  "Scrum Master",
  "Fullstack разработчик",
  "Security Engineer",
  "Cloud Engineer",
  "Game Developer",
  "QA Automation",
  "Бизнес-аналитик",
  "Сетевой инженер",
  "Tech Lead",
  "Solution Architect",
  "AI Engineer",
  "VR/AR разработчик",
  "Game Designer",
  "BI-аналитик",
  "Инженер по данным",
  "iOS разработка",
  "Android разработка",
];
const selectedContainer = document.getElementById('selectedCompetencies');
const modal = document.getElementById('competencyModal');

function openModal() {
    modal.style.display = 'block';
    renderCompetencyOptions();
}

function closeModal() {
    modal.style.display = 'none';
    const searchInput = document.getElementById('competencies_search-input');
    searchInput.value = '';
}

function renderCompetencyOptions() {
    const optionsContainer = document.getElementById('competencyOptions');
    optionsContainer.innerHTML = '';

    competencies.forEach(comp => {
        const div = document.createElement('div');
        div.className = 'competency-option';
        div.textContent = comp;
        div.onclick = () => {
            addCompetencyToModal(comp);
            addCompetency(comp);
        };
        optionsContainer.appendChild(div);
    });
}

function addCompetency(name) {
    const existing = Array.from(selectedContainer.children).some(child =>
        child.classList.contains('user__competencies_item-value') &&
        child.textContent.trim().startsWith(name)
    );

    if (!existing) {
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
            saveCompetencies();
            removeFromModal(name, 'selectedFromModal');
        };

        div.appendChild(removeBtn);

        const chooseButton = selectedContainer.querySelector('[onclick="openModal()"]');
        selectedContainer.insertBefore(div, chooseButton);

        saveCompetencies();
    }
}

function removeFromModal(name, modalContainerId) {
    const container = document.getElementById(modalContainerId);
    const items = Array.from(container.children);
    items.forEach(item => {
        if (item.textContent.trim().startsWith(name)) {
            item.remove();
        }
    });
}

function saveCompetencies() {
    const items = Array.from(selectedContainer.children)
        .filter(child => child.classList.contains('user__competencies_item-value') && !child.querySelector('input'))
        .map(child => child.textContent.replace('×', '').trim());
    
    localStorage.setItem('savedCompetencies', JSON.stringify(items));
}

window.addEventListener('DOMContentLoaded', function() {
    const saved = JSON.parse(localStorage.getItem('savedCompetencies') || []);
    saved.forEach(name => addCompetency(name));
});