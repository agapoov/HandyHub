document.getElementById('saveSkills').addEventListener('click', function () {
    // Получаем все выбранные навыки
    const selectedSkills = [];
    document.querySelectorAll('input[name="skills"]:checked').forEach(function (checkbox) {
        selectedSkills.push(checkbox.value);
    });

    // Проверяем, выбраны ли навыки
    if (selectedSkills.length === 0) {
        alert('Пожалуйста, выберите хотя бы один навык.');
        return; // Не закрываем модальное окно
    }

    // Здесь можно выполнить нужные действия с выбранными навыками, например, отобразить их в форме
    console.log('Выбранные навыки:', selectedSkills);

    // Закрыть модальное окно
    const skillsModal = new bootstrap.Modal(document.getElementById('skillsModal'));
    skillsModal.hide();
});