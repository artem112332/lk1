const skills = [
  "Jira", "Trello", "Scrum", "Agile", "Kanban",
  "Figma", "Draw.io", "JavaScript", "HTML", "CSS",
  "TypeScript", "React", "Python", "Django", "Flask",
  "Java", "C#", "PHP", "Node.js", "Go",
  "Kotlin", "Cypress", "Sketch", "Adobe XD", "Arc42",
  "Asana", "Monday.com", "Microsoft Project", "Пачка", "Kaiten", "ClickUp", "Notion",
  "Slack", "Microsoft Teams", "Zoom", "Google Meet", "Miro",
  "Confluence", "Google Docs", "Microsoft Word",
  "BPMN", "UML", "Microsoft Visio", "Lucidchart",
  "Balsamiq", "Power BI", "Tableau", "Google Data Studio", "SQL",
  "Angular", "Vue.js", "Webpack", "JQuery",
  "PostgreSQL", "MySQL", "MongoDB", "Redis",
  "Docker", "Kubernetes", "Git", "GitHub", "GitLab",
  "Material UI", "Bootstrap", "TailwindCSS", "ESLint", "Prettier", "Storybook",
  "Jest", "React Testing Library",
  "Spring", ".NET", "Swift", "Elixir",
  "REST", "GraphQL", "gRPC",
  "AWS", "GCP", "Firebase", "Heroku",
  "OAuth", "JWT",
  "TestRail", "Selenium", "JUnit", "TestNG",
  "Jenkins", "GitLab CI", "CircleCI", "GitHub Actions",
  "Appium", "BrowserStack", "JMeter", "Gatling",
  "InVision", "Canva", "Marvel", "UXPressia", "UserTesting", "Hotjar",
  "CJM", "Personae", "Wireframes", "Design Tokens", "Atomic Design",
  "Helm", "Terraform", "Ansible", "Prometheus", "Grafana",
  "ELK Stack", "Loki",
  "C4 Model", "ADR",
  "R", "Pandas", "NumPy", "Scikit-learn", "TensorFlow", "Keras", "PyTorch",
  "Jupyter", "Google Colab", "Matplotlib", "Seaborn", "Plotly"
];
const selectedSkillsContainer = document.getElementById('selectedSkills');
const skillsModal = document.getElementById('skillsModal');

function openSkillsModal() {
    renderSkillsOptions();
    skillsModal.style.display = 'block';
}

function closeSkillsModal() {
    skillsModal.style.display = 'none';
    const searchInput = document.getElementById('competencies_search-input');
    searchInput.value = '';
}

function renderSkillsOptions() {
    const optionsContainer = document.getElementById('skillsOptions');
    optionsContainer.innerHTML = '';

    skills.forEach(skill => {
        const div = document.createElement('div');
        div.className = 'competency-option';
        div.textContent = skill;
        div.onclick = () => {
            addSkillToModal(skill);
            addSkill(skill);
        };
        optionsContainer.appendChild(div);
    });
}

function addSkill(name) {
    const alreadyAdded = Array.from(selectedSkillsContainer.children).some(child =>
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
            saveSkills();
        };

        div.appendChild(removeBtn);

        const chooseBtn = document.getElementById('skillsChooseBtn');
        selectedSkillsContainer.insertBefore(div, chooseBtn);

        saveSkills();
    }
}

function saveSkills() {
    const skills = Array.from(selectedSkillsContainer.children)
        .filter(el => el.classList.contains('user__competencies_item-value') && !el.querySelector('input'))
        .map(el => el.textContent.replace('×', '').trim());
    
    localStorage.setItem('savedSkills', JSON.stringify(skills));
}

window.addEventListener('DOMContentLoaded', function() {
    const savedSkills = JSON.parse(localStorage.getItem('savedSkills') || []);
    savedSkills.forEach(skill => addSkill(skill));
});