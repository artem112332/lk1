function addCompetencyToModal(name) {
    const container = document.getElementById('selectedFromModal');

    const exists = Array.from(container.children).some(child => child.textContent.trim().startsWith(name));
    if (exists) return;

    const item = document.createElement('div');
    item.className = 'competency-option selected';
    item.textContent = name;
    item.style.position = 'relative';
    item.style.paddingRight = '20px';
    item.style.backgroundColor = '#dcedc8';

    const removeBtn = document.createElement('div');
    removeBtn.textContent = '×';
    removeBtn.style.position = 'absolute';
    removeBtn.style.right = '5px';
    removeBtn.style.top = '0';
    removeBtn.style.cursor = 'pointer';
    removeBtn.style.color = '#888';

    removeBtn.onclick = (e) => {
        e.stopPropagation();
        item.remove();
        removeFromMainPage(name, 'selectedCompetencies');
    };

    item.appendChild(removeBtn);
    container.appendChild(item);

    function removeFromMainPage(name, containerId) {
        const container = document.getElementById(containerId);
        const items = Array.from(container.children);
        items.forEach(item => {
            if (item.classList.contains('user__competencies_item-value') && 
                item.textContent.trim().startsWith(name)) {
                item.remove();
                if (containerId === 'selectedCompetencies') {
                    saveSkills();
                } else {
                    saveCompetencies();
                }
            }
        });
    };
}