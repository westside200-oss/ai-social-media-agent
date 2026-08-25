import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FiHome, FiUsers, FiFileText, FiBarChart2 } from 'react-icons/fi';

const Navigation = () => {
  const location = useLocation();
  
  const isActive = (path) => location.pathname === path;
  
  const navItems = [
    { label: 'Dashboard', path: '/', icon: FiHome },
    { label: 'Accounts', path: '/accounts', icon: FiUsers },
    { label: 'Posts', path: '/posts', icon: FiFileText },
    { label: 'Analytics', path: '/analytics', icon: FiBarChart2 },
  ];
  
  return (
    <nav className="w-64 bg-gradient-to-b from-purple-700 to-purple-900 text-white p-6">
      <div className="mb-8">
        <h1 className="text-2xl font-bold">📱 AI Social Agent</h1>
        <p className="text-purple-200 text-sm mt-1">Content Automation</p>
      </div>
      
      <ul className="space-y-2">
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <li key={item.path}>
              <Link
                to={item.path}
                className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                  isActive(item.path)
                    ? 'bg-purple-600 text-white'
                    : 'text-purple-100 hover:bg-purple-600'
                }`}
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </Link>
            </li>
          );
        })}
      </ul>
      
      <div className="mt-12 pt-6 border-t border-purple-600">
        <p className="text-purple-300 text-xs text-center">v0.1.0</p>
      </div>
    </nav>
  );
};

export default Navigation;
