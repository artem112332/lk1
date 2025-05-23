function addSkillToModal(name) {
    const container = document.getElementById('selectedFromSkillsModal');

    const exists = Array.from(container.children).some(child => child.textContent.trim().startsWith(name));
    if (exists) return;

    const item = document.createElement('div');
    item.className = 'competency-option selected';
    item.textContent = name;
    item.style.position = 'relative';
    item.style.cursor = 'auto';
    item.style.backgroundColor = '#dcedc8';

    const removeBtn = document.createElement('div');
    // removeBtn.textContent = '×';
    // removeBtn.style.position = 'absolute';
    // removeBtn.style.right = '5px';
    // removeBtn.style.top = '0';
    // removeBtn.style.cursor = 'pointer';
    // removeBtn.style.color = '#888';

    removeBtn.onclick = (e) => {
        // e.stopPropagation();
        // item.remove();
        removeFromMainPage(name, 'selectedSkills');
    };

    item.appendChild(removeBtn);
    container.appendChild(item);
}