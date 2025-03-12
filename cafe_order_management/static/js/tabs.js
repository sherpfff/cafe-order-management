document.addEventListener('DOMContentLoaded', () => {
    // Инициализация вкладок
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');

    if (tabs.length === 0 || tabContents.length === 0) {
        return; // Если вкладки или контент не найдены, завершаем выполнение
    }

    // Функция для переключения вкладок
    function activateTab(index) {
        // Сброс активности всех вкладок и контента
        tabs.forEach((tab) => tab.classList.remove('active'));
        tabContents.forEach((content) => content.classList.remove('active'));

        // Активация выбранной вкладки и соответствующего контента
        tabs[index].classList.add('active');
        tabContents[index].classList.add('active');
    }

    // Добавление обработчиков событий для вкладок
    tabs.forEach((tab, index) => {
        tab.addEventListener('click', () => {
            activateTab(index);
        });
    });

    // Активация первой вкладки по умолчанию
    activateTab(0);
});