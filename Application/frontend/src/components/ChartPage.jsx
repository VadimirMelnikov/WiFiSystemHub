import React, { useEffect, useState, useRef, useCallback } from 'react';
import Selector from './Selector';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

function ChartPage() {
  const [group, setGroup] = useState('temperature');
  const chartRef = useRef(null);
  const colorMap = useRef({});

  // Начальное состояние данных графика
  const [chartData, setChartData] = useState({
    datasets: [],
    labels: [],
  });

  // Функция обновления данных с добавлением новых значений и обрезкой до 100
  const updateChartData = useCallback((newData) => {
    let updatedDatasets = [...chartData.datasets];
    if (!updatedDatasets.length) {
      updatedDatasets = newData.reduce((acc, item) => {
        if (!colorMap.current[item.name]) {
          colorMap.current[item.name] = `hsl(${Object.keys(colorMap.current).length * 60}, 70%, 50%)`;
        }
        if (!acc.find(d => d.label === item.name)) {
          acc.push({ label: item.name, data: [], borderColor: colorMap.current[item.name], backgroundColor: colorMap.current[item.name] });
        }
        return acc;
      }, []);
    }

    // Добавление новых точек и обрезка до 100 значений
    newData.forEach(item => {
      const dataset = updatedDatasets.find(d => d.label === item.name);
      if (dataset) {
        dataset.data.push({ x: item.time_stamp, y: item.value });
        if (dataset.data.length > 100) {
          dataset.data = dataset.data.slice(-100);
        }
      }
    });

    // Обновление меток (labels) на основе последней серии данных
    const lastDataset = updatedDatasets[updatedDatasets.length - 1];
    const updatedLabels = lastDataset ? lastDataset.data.map(d => d.x).slice(-100) : [];

    setChartData({
      datasets: updatedDatasets,
      labels: updatedLabels,
    });

    // Обновление графика через ref, если доступен
    if (chartRef.current) {
      chartRef.current.update();
    }
  }, [chartData.datasets]);

  useEffect(() => {
    const interval = setInterval(() => {
      fetch(`http://127.0.0.1:5000/history?group=${group}`)
        .then(response => response.json())
        .then(updateChartData)
        .catch(error => console.error('Error fetching data:', error));
    }, 2000);
    return () => clearInterval(interval);
  }, [group, updateChartData]);

  return (
    <div className="p-4">
      <h2 className="text-xl mb-2">График значений датчиков</h2>
      <Selector onChange={setGroup} />
      <div className="mt-4">
        <Line
          ref={chartRef}
          data={chartData}
          options={{
            responsive: true,
            animation: false,
            plugins: { legend: { position: 'top' }, title: { display: true, text: `Group: ${group}` } },
          }}
        />
      </div>
    </div>
  );
}

export default ChartPage;