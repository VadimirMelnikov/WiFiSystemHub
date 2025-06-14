import React, { useEffect, useState } from 'react';

function ActuatorsTable() {
  const [actuators, setActuators] = useState([]);
  const [inputValue, setInputValue] = useState('');

  useEffect(() => {
    const interval = setInterval(() => {
      fetch('http://127.0.0.1:5000/actuators')
        .then(response => response.json())
        .then(data => setActuators(data));
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleSend = (value) => {
    fetch(`http://127.0.0.1:5000/data?data=${value}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
    })
      .then(response => {
        if (response.ok) {
          setInputValue(''); // Сброс поля ввода после успешной отправки
        } else {
          console.error('Failed to send data');
        }
      })
      .catch(error => console.error('Error sending data:', error));
  };

  return (
    <div className="w-1/2 p-4">
      <h2 className="text-xl mb-2">Исполнительные механизмы</h2>
      <table className="w-full border-collapse border border-gray-300">
        <thead>
          <tr className="bg-gray-100">
            <th className="border border-gray-300 p-2">id</th>
            <th className="border border-gray-300 p-2">sensor_id</th>
          </tr>
        </thead>
        <tbody>
          {actuators.map((actuator, index) => (
            <tr key={index} className="hover:bg-gray-50">
              <td className="border border-gray-300 p-2">{actuator.name}</td>
              <td className="border border-gray-300 p-2">
                {actuator.sensor === 'server' ? (
                  <div>
                    <input
                      type="number"
                      value={inputValue}
                      onChange={(e) => setInputValue(e.target.value)}
                      className="border p-1 mr-2"
                      placeholder="Введите число"
                    />
                    <button
                      onClick={() => handleSend(inputValue)}
                      className="bg-blue-500 text-white p-1 rounded"
                    >
                      Отправить
                    </button>
                  </div>
                ) : (
                  actuator.sensor
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ActuatorsTable;