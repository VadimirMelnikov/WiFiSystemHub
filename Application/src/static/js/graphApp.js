document.addEventListener('DOMContentLoaded', function() {
    let chartInstance = null;
    let updateInterval = null;
    let previousData = null;

    window.fetchData = async function() {
        const groupId = document.getElementById('groupSelect').value;
        if (!groupId) {
            alert('Пожалуйста, выберите ID группы');
            // Очищаем интервал, если группа не выбрана
            if (updateInterval) {
                clearInterval(updateInterval);
                updateInterval = null;
            }
            // Очищаем график, если он существует
            if (chartInstance) {
                chartInstance.destroy();
                chartInstance = null;
            }
            previousData = null;
            return;
        }

        try {
            const response = await fetch(`/history?id=${groupId}`);
            if (!response.ok) {
                throw new Error('Ошибка при получении данных');
            }
            const data = await response.json();

            // Проверяем, изменились ли данные
            if (previousData && JSON.stringify(data) === JSON.stringify(previousData)) {
                return; // Данные не изменились, обновление не требуется
            }
            previousData = data;

            // Собираем все уникальные временные метки
            const allTimestamps = [...new Set(data.map(item => item.time_stamp))].sort((a, b) => {
                // Сортировка по времени в формате DD.MM.YYYY HH:mm:ss
                const dateA = parseTimestamp(a);
                const dateB = parseTimestamp(b);
                return dateA - dateB;
            });

            // Группировка данных по имени датчика
            const sensors = {};
            data.forEach(item => {
                if (!sensors[item.name]) {
                    sensors[item.name] = {};
                }
                sensors[item.name][item.time_stamp] = item.param;
            });

            // Подготовка данных для Chart.js
            const datasets = Object.keys(sensors).map(name => {
                // Для каждого датчика создаем массив params, соответствующий allTimestamps
                const params = allTimestamps.map(timestamp =>
                    sensors[name][timestamp] !== undefined ? sensors[name][timestamp] : null
                );
                return {
                    label: name,
                    data: params,
                    borderColor: stringToColor(name),
                    fill: false,
                    tension: 0.1
                };
            });

            const ctx = document.getElementById('sensorChart').getContext('2d');

            if (chartInstance) {
                // Обновляем существующий график
                chartInstance.data.labels = allTimestamps;
                chartInstance.data.datasets = datasets;
                chartInstance.update();
            } else {
                // Создаем новый график
                chartInstance = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: allTimestamps,
                        datasets: datasets
                    },
                    options: {
                        responsive: true,
                        scales: {
                            x: {
                                title: {
                                    display: true,
                                    text: 'Время'
                                }
                            },
                            y: {
                                title: {
                                    display: true,
                                    text: 'Параметр'
                                },
                                beginAtZero: true
                            }
                        },
                        plugins: {
                            legend: {
                                display: true
                            }
                        },
                        elements: {
                            line: {
                                spanGaps: true // Позволяет линию продолжаться через null
                            }
                        }
                    }
                });
            }

            // Запуск периодического обновления, если еще не запущено
            if (!updateInterval) {
                updateInterval = setInterval(fetchData, 1000); // Обновление каждые 5 секунд
            }
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Не удалось загрузить данные');
            // Очищаем интервал при ошибке
            if (updateInterval) {
                clearInterval(updateInterval);
                updateInterval = null;
            }
        }
    };

    // Функция для генерации цвета на основе последней цифры имени датчика
    function stringToColor(str) {
        // Извлекаем последнюю цифру из имени (например, "Client_3_1" -> "1")
        const uniqueNumber = str.match(/\d+$/)[0];

        // Используем только эту цифру для хэширования
        let hash = 0;
        for (let i = 0; i < uniqueNumber.length; i++) {
            hash = uniqueNumber.charCodeAt(i) + ((hash << 5) - hash);
        }
        let color = '#';
        for (let i = 0; i < 3; i++) {
            const value = (hash >> (i * 8)) & 0xFF;
            color += ('00' + value.toString(16)).slice(-2);
        }
        return color;
    }

    // Функция для парсинга временной метки в формате DD.MM.YYYY HH:mm:ss
    function parseTimestamp(timestamp) {
        const [date, time] = timestamp.split(' ');
        const [day, month, year] = date.split('.').map(Number);
        const [hours, minutes, seconds] = time.split(':').map(Number);
        return new Date(year, month - 1, day, hours, minutes, seconds);
    }
});