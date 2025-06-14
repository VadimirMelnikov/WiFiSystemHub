import React, { useEffect, useState } from 'react';
import { filteredSensors } from './filteredSensors';

function SensorsTable() {
  const [sensors, setSensors] = useState([]);

  useEffect(() => {
    const interval = setInterval(() => {
      fetch('http://127.0.0.1:5000/sensors')
        .then(response => response.json())
        .then(data => {
          // Обновляем только те датчики, которые не в списке filteredSensors
          const updatedSensors = data.map(sensor => {
            if (filteredSensors.includes(sensor.name)) {
              // Сохраняем текущее значение для датчиков из filteredSensors
              const existingSensor = sensors.find(s => s.name === sensor.name);
              return { ...sensor, value: existingSensor ? existingSensor.value : sensor.value };
            }
            return sensor;
          });
          setSensors(updatedSensors);
        });
    }, 1000);
    return () => clearInterval(interval);
  }, [sensors]);

  const handleUpdateValue = (sensorName) => {
    fetch('http://127.0.0.1:5000/sensors')
      .then(response => response.json())
      .then(data => {
        const updatedSensor = data.find(s => s.name === sensorName);
        if (updatedSensor) {
          setSensors(prevSensors =>
            prevSensors.map(s =>
              s.name === sensorName ? { ...s, value: updatedSensor.value } : s
            )
          );
        }
      })
      .catch(error => console.error('Error updating sensor value:', error));
  };

  return (
    <div className="w-1/2 p-4">
      <h2 className="text-xl mb-2">Датчики</h2>
      <table className="w-full border-collapse border border-gray-300">
        <thead>
          <tr className="bg-gray-100">
            <th className="border border-gray-300 p-2">id</th>
            <th className="border border-gray-300 p-2">Группа</th>
            <th className="border border-gray-300 p-2">Значение</th>
            <th className="border border-gray-300 p-2">Ед. измерения</th>
            <th className="border border-gray-300 p-2">Состояние</th>
          </tr>
        </thead>
        <tbody>
          {sensors.map((sensor, index) => (
            <tr key={index} className="hover:bg-gray-50">
              <td className="border border-gray-300 p-2">{sensor.name}</td>
              <td className="border border-gray-300 p-2">{sensor.group}</td>
              <td className="border border-gray-300 p-2">
                {filteredSensors.includes(sensor.name) ? (
                  <div>
                    <span>{sensor.value}</span>
                    <button
                      onClick={() => handleUpdateValue(sensor.name)}
                      className="ml-2 bg-blue-500 text-white p-1 rounded"
                    >
                      Обновить
                    </button>
                  </div>
                ) : (
                  sensor.value || 'N/A'
                )}
              </td>
              <td className="border border-gray-300 p-2">{sensor.unit}</td>
              <td className="border border-gray-300 p-2">{sensor.status}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default SensorsTable;