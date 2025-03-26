function toggleForm(formId) {
    var form = document.getElementById(formId);
    
    if (form.classList.contains('open')) {
        form.style.maxHeight = null; // Сброс максимальной высоты
        form.classList.remove('open');
    } else {
        form.style.maxHeight = form.scrollHeight + "px"; // Установите максимальную высоту на основе содержимого
        form.classList.add('open');
    }
}