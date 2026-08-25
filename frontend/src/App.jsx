import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Accounts from './pages/Accounts';
import Posts from './pages/Posts';
import Analytics from './pages/Analytics';
import Navigation from './components/Navigation';
import './App.css';

function App() {
  return (
    <Router>
      <div className="flex h-screen bg-gray-100">
        <Navigation />
        <div className="flex-1 overflow-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/accounts" element={<Accounts />} />
            <Route path="/posts" element={<Posts />} />
            <Route path="/analytics" element={<Analytics />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
