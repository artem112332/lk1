let uploadedFiles = [];

window.onload = function () {
    const saved = JSON.parse(localStorage.getItem('savedFileNames') || '[]');
    uploadedFiles = saved;

    const fileListContainer = document.getElementById('fileList');
    saved.forEach(name => {
        const fileSpan = createFileSpan(name);
        fileListContainer.appendChild(fileSpan);
    });
};

function handleFileUpload() {
    const fileInput = document.getElementById('fileInput');
    const fileListContainer = document.getElementById('fileList');

    const newFiles = Array.from(fileInput.files);

    newFiles.forEach(file => {
        if (!uploadedFiles.includes(file.name)) {
            uploadedFiles.push(file.name);
            const fileSpan = createFileSpan(file.name);
            fileListContainer.appendChild(fileSpan);
        }
    });

    localStorage.setItem('savedFileNames', JSON.stringify(uploadedFiles));

    // fileInput.value = '';
}

function createFileSpan(fileName) {
    const fileSpan = document.createElement('span');
    fileSpan.className = 'file-item';
    fileSpan.textContent = fileName;

    const removeBtn = document.createElement('span');
    removeBtn.className = 'remove-btn';
    removeBtn.textContent = '×';

    removeBtn.onclick = function (e) {
        e.stopPropagation();
        fileSpan.remove();
        uploadedFiles = uploadedFiles.filter(name => name !== fileName);
        localStorage.setItem('savedFileNames', JSON.stringify(uploadedFiles));
    };

    fileSpan.appendChild(removeBtn);
    return fileSpan;
}