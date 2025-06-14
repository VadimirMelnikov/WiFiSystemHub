import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import SensorsTable from './components/SensorsTable';
import ActuatorsTable from './components/ActuatorsTable';
import ChartPage from './components/ChartPage';
import './index.css';

function App() {
  return (
    <Router>
      <div className="container mx-auto p-4">
        <nav className="mb-4">
          <Link to="/" className="mr-4 text-blue-500">Home</Link>
          <Link to="/charts" className="text-blue-500">Charts</Link>
        </nav>
        <Routes>
          <Route path="/" element={<div className="flex"><SensorsTable /><ActuatorsTable /></div>} />
          <Route path="/charts" element={<ChartPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;