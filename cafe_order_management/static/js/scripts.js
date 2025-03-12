document.addEventListener('DOMContentLoaded', () => {
    // Обработка формы добавления заказа
    const addOrderForm = document.getElementById('add-order-form');
    if (addOrderForm) {
        addOrderForm.addEventListener('submit', (event) => {
            const tableNumberInput = document.getElementById('table_number');
            const dishesSelect = document.getElementById('dishes');

            // Проверка ввода номера стола
            if (!tableNumberInput.value.trim()) {
                event.preventDefault();
                alert('Пожалуйста, введите номер стола.');
                return;
            }

            // Проверка выбора блюд
            if (dishesSelect && dishesSelect.selectedOptions.length === 0) {
                event.preventDefault();
                alert('Пожалуйста, выберите хотя бы одно блюдо.');
                return;
            }
        });
    }

    // Обработка формы поиска заказов
    const searchOrdersForm = document.getElementById('search-orders-form');
    if (searchOrdersForm) {
        searchOrdersForm.addEventListener('submit', (event) => {
            const searchQueryInput = document.getElementById('search_query');

            // Проверка ввода запроса
            if (!searchQueryInput.value.trim()) {
                event.preventDefault();
                alert('Пожалуйста, введите запрос для поиска.');
                return;
            }
        });
    }

    // Обработка кнопок удаления заказа
    const deleteOrderButtons = document.querySelectorAll('.delete-order-button');
    deleteOrderButtons.forEach((button) => {
        button.addEventListener('click', (event) => {
            const orderId = button.dataset.orderId;
            const confirmDelete = confirm(`Вы уверены, что хотите удалить заказ №${orderId}?`);
            if (!confirmDelete) {
                event.preventDefault();
            }
        });
    });

    // Добавление подсветки строки таблицы при наведении
    const tableRows = document.querySelectorAll('.table tbody tr');
    tableRows.forEach((row) => {
        row.addEventListener('mouseenter', () => {
            row.style.backgroundColor = '#f8f9fa';
        });
        row.addEventListener('mouseleave', () => {
            row.style.backgroundColor = '';
        });
    });
});