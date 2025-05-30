let allSensors = [];

async function fetchSensorData() {
    try {
        const response = await fetch('/view');
        if (!response.ok) throw new Error("Ошибка загрузки данных");

        allSensors = await response.json();
        applyFilter();     // Применяем текущий фильтр
    } catch (error) {
        console.error('Ошибка:', error);
    }
}


function applyFilter() {
    const selectedGroup = document.getElementById('group-filter').value;
    const tbody = document.querySelector('#sensors-table tbody');
    tbody.innerHTML = '';

    const filtered = selectedGroup
    ? allSensors.filter(s => s.group === selectedGroup)
    : allSensors;

    filtered.forEach(sensor => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${sensor.id}</td>
            <td>${sensor.group}</td>
            <td>${sensor.value.toFixed(2)}</td>
            <td>${sensor.unit}</td>
            <td>
                <span class="status-icon ${getStatusClass(sensor.status)}">
                    ${getStatusIcon(sensor.status)}
                </span>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function getStatusClass(status) {
    switch (status) {
        case 'active': return 'green';
        case 'inactive': return 'red';
    }
}

function getStatusIcon(status) {
    switch (status) {
        case 'active': return '🟢';
        case 'inactive': return '🔴';
    }
}

// Первый вызов и обновление каждые 5 секунд
fetchSensorData();
setInterval(fetchSensorData, 5000);