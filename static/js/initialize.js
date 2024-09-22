
const selectElement = document.getElementById('regionFilter');
const typeSelectElement = document.getElementById('typeFilter');

const choices = new Choices(selectElement, {
    searchEnabled: true,
    itemSelectText: '',
    shouldSort: false,
    placeholder: true,
    placeholderValue: 'Выберите регион'
});

const typeChoices = new Choices(typeSelectElement, {
    searchEnabled: false,
    itemSelectText: '',
    shouldSort: false,
    placeholder: true,
    placeholderValue: 'Выберите тип'
});

function applyFilters() {
    const selectedRegion = selectElement.value;
    const selectedType = typeSelectElement.value; 

    document.querySelectorAll('#table_main tbody tr, .bg-gray-200').forEach(function(element) {
        const region = element.getAttribute('data-region');
        const type = element.getAttribute('data-comptype') === 'ИП' ? 'ip' : 'ooo';
        const matchesRegion = selectedRegion === region || !selectedRegion;
        const matchesType = selectedType === type || !selectedType;
        element.style.display = matchesRegion && matchesType ? '' : 'none';
    });
}

selectElement.addEventListener('change', applyFilters);
typeSelectElement.addEventListener('change', applyFilters);

document.querySelectorAll('.tab-link').forEach(function(tab) {
    tab.addEventListener('click', function() {
        document.querySelectorAll('.tab-link').forEach(t => t.classList.remove('active', 'border-blue-500'));
        document.querySelectorAll('.tab-content').forEach(content => content.classList.add('hidden'));

        tab.classList.add('active', 'border-blue-500');
        const contentId = tab.getAttribute('data-tab');
        document.getElementById(contentId).classList.remove('hidden');
    });
});

// Обработка открытия и закрытия модального окна
document.querySelectorAll('.bg-gray-200').forEach(function(card) {
    card.addEventListener('click', function() {
        const messageId = card.getAttribute('data-id');
        document.getElementById('message_modal_id').value = messageId;
        document.getElementById('messageModal').classList.remove('hidden');
        document.getElementById('messageModal').classList.add('flex');
    });
});

function closeMessageModal(event) {
    if (event.target === document.getElementById('messageModal')) {
        document.getElementById('messageModal').classList.add('hidden');
        document.getElementById('messageModal').classList.remove('flex');
    }
}

function openBalanceModal() {
    document.getElementById('balanceModal').classList.remove('hidden');
    document.getElementById('balanceModal').classList.add('flex');
    document.getElementById('balanceModal').classList.add('items-center');
    document.getElementById('balanceModal').classList.add('justify-center');
}

function openHistoryModal() {
    document.getElementById('historyModal').classList.remove('hidden');
    document.getElementById('historyModal').classList.add('flex');
    document.getElementById('historyModal').classList.add('items-center');
    document.getElementById('historyModal').classList.add('justify-center');
}

function closeModal(event) {
    if (event.target === document.getElementById('balanceModal')) {
        document.getElementById('balanceModal').classList.add('hidden');
        document.getElementById('balanceModal').classList.remove('flex');
    } else if (event.target === document.getElementById('historyModal')) {
        document.getElementById('historyModal').classList.add('hidden');
        document.getElementById('historyModal').classList.remove('flex');
    }
}

$(document).ready(function() {
    $("#table_main").fancyTable({
        pagination: true,
        perPage:15,
        searchable: false,
        paginationElement: '.box_pagination_container',
        paginationClass: 'btn_pagination',
        paginationClassActive: 'btn_pagination_active',
        sortFunction: function(a, b, fancyTableObject, rowA, rowB) {
            // Удаление символов $ и %, обрезка пробелов
            let cleanA = a.replace(/[\$\%]/g, '').trim();
            let cleanB = b.replace(/[\$\%]/g, '').trim();
        
            // Попытка преобразовать очищенные строки в числа
            let numA = parseFloat(cleanA);
            let numB = parseFloat(cleanB);
        
            // Проверка, являются ли оба значения действительными числами и не являются датами
            let isNumA = !isNaN(numA) && cleanA.match(/^\d+(\.\d+)?$/);
            let isNumB = !isNaN(numB) && cleanB.match(/^\d+(\.\d+)?$/);
        
            // Проверка на наличие даты в строке и преобразование в дату
            let datePattern = /^\d{4}-\d{2}-\d{2}$/; // Регулярное выражение для даты в формате ГГГГ-ММ-ДД
            let isDateA = datePattern.test(cleanA);
            let isDateB = datePattern.test(cleanB);
        
            if (isNumA && isNumB) {
                // Сортировка чисел
                return fancyTableObject.sortOrder > 0 ? numA - numB : numB - numA;
            } else if (isDateA && isDateB) {
                // Сортировка дат
                return fancyTableObject.sortOrder > 0 ? Date.parse(cleanA) - Date.parse(cleanB) : Date.parse(cleanB) - Date.parse(cleanA);
            } else {
                // Сортировка строк
                return fancyTableObject.sortOrder > 0 ? cleanA.localeCompare(cleanB) : cleanB.localeCompare(cleanA);
            }
        }
            
    });
});

function hideNoteEditor() {
    document.getElementById('noteEditorModal').classList.add('hidden');
    document.getElementById('noteEditorModal').classList.remove('flex');
}

function closeNoteEditor(event) {
    if (event.target.id === 'noteEditorModal') {
        hideNoteEditor();
    }
}

function toggleFullNoteModal(element) {
    var noteContent = element.getAttribute('data-note');
    var modal = document.getElementById('fullNoteModal');
    var modalContent = document.getElementById('modalNoteContent');

    modalContent.textContent = noteContent; // Устанавливаем текст заметки
    modal.classList.toggle('hidden'); // Переключаем видимость модального окна
}

// Закрытие модального окна при клике вне его
window.onclick = function(event) {
    var modal = document.getElementById('fullNoteModal');

    // Проверяем, что клик произошел на модальном окне
    if (event.target === modal) {
        modal.classList.add('hidden');
    }
}





function openNoteEditor(messageId) {
    var hiddenMessageId = document.getElementById('hiddenMessageId');
    hiddenMessageId.value = messageId;
    var noteEditorModal = document.getElementById('noteEditorModal');
    noteEditorModal.classList.remove('hidden');
    noteEditorModal.classList.add('flex');
}

function openTariffModal() {
    document.getElementById('tariffModal').style.display = 'block';
}

function closeTariffModal(event) {
    if (event) event.stopPropagation();
    document.getElementById('tariffModal').style.display = 'none';
}

function openRequisitesModal() {
    document.getElementById('requisitesModal').style.display = 'block';
}

function closeRequisitesModal() {
    document.getElementById('requisitesModal').style.display = 'none';
}