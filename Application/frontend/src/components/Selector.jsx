import React from 'react';

function Selector({ onChange }) {
  const groups = ['temperature', 'level', 'humidity', 'pressure'];

  return (
    <select
      className="p-2 border border-gray-300 rounded"
      onChange={(e) => onChange(e.target.value)}
      defaultValue="temperature"
    >
      {groups.map((group) => (
        <option key={group} value={group}>{group}</option>
      ))}
    </select>
  );
}

export default Selector;