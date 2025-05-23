function addSpecializationsToModal(name) {
    const container = document.getElementById('selectedFromSpecializationsModal');

    const exists = Array.from(container.children).some(child => child.textContent.trim().startsWith(name));
    if (exists) return;

    const item = document.createElement('div');
    item.className = 'competency-option selected';
    item.textContent = name;
    item.style.position = 'relative';
    item.style.cursor = 'auto';
    item.style.backgroundColor = '#dcedc8';

    const removeBtn = document.createElement('div');
    removeBtn.onclick = (e) => {
        removeFromMainPage(name, 'selectedSpecializations');
    };
    item.appendChild(removeBtn);
    container.appendChild(item);
}