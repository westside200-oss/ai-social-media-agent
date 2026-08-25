import React, { useEffect, useState } from 'react';
import { analyticsAPI, accountsAPI, postsAPI } from '../api/client';
import { FiActivity, FiTrendingUp, FiUsers, FiFileText } from 'react-icons/fi';

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalAccounts: 0,
    totalPosts: 0,
    totalImpressions: 0,
    avgEngagement: 0,
  });
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetchDashboardData = async () => {
      try {
        const accountsRes = await accountsAPI.list({ is_active: true });
        const postsRes = await postsAPI.list({ is_posted: true });
        
        setStats({
          totalAccounts: accountsRes.data.length,
          totalPosts: postsRes.data.length,
          totalImpressions: 0, // Will be populated from analytics
          avgEngagement: 0,
        });
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchDashboardData();
  }, []);
  
  const StatCard = ({ icon: Icon, label, value, color }) => (
    <div className={`bg-white rounded-lg shadow p-6 border-l-4 ${color}`}>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-gray-500 text-sm">{label}</p>
          <p className="text-2xl font-bold text-gray-900 mt-2">{value}</p>
        </div>
        <Icon className="text-gray-400" size={32} />
      </div>
    </div>
  );
  
  if (loading) {
    return <div className="p-8">Loading dashboard...</div>;
  }
  
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={FiUsers}
          label="Active Accounts"
          value={stats.totalAccounts}
          color="border-blue-500"
        />
        <StatCard
          icon={FiFileText}
          label="Total Posts"
          value={stats.totalPosts}
          color="border-purple-500"
        />
        <StatCard
          icon={FiActivity}
          label="Impressions"
          value={stats.totalImpressions.toLocaleString()}
          color="border-pink-500"
        />
        <StatCard
          icon={FiTrendingUp}
          label="Avg. Engagement"
          value={`${stats.avgEngagement.toFixed(1)}%`}
          color="border-green-500"
        />
      </div>
      
      <div className="mt-8 bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h2>
        <div className="flex gap-4">
          <button className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700">
            Add Account
          </button>
          <button className="px-4 py-2 bg-pink-600 text-white rounded-lg hover:bg-pink-700">
            Generate Post
          </button>
          <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
            Sync Analytics
          </button>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
