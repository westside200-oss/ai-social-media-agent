import React, { useEffect, useState } from 'react';
import { accountsAPI } from '../api/client';
import { FiEdit2, FiTrash2, FiPlus, FiCheck } from 'react-icons/fi';

const Accounts = () => {
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    platform: 'instagram',
    username: '',
    account_name: '',
    account_id: '',
    account_type: 'business',
    access_token: '',
  });
  
  useEffect(() => {
    fetchAccounts();
  }, []);
  
  const fetchAccounts = async () => {
    try {
      const response = await accountsAPI.list({ is_active: true });
      setAccounts(response.data);
    } catch (error) {
      console.error('Error fetching accounts:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await accountsAPI.create(formData);
      setFormData({
        platform: 'instagram',
        username: '',
        account_name: '',
        account_id: '',
        account_type: 'business',
        access_token: '',
      });
      setShowForm(false);
      fetchAccounts();
    } catch (error) {
      console.error('Error creating account:', error);
    }
  };
  
  const handleDelete = async (id) => {
    if (window.confirm('Are you sure?')) {
      try {
        await accountsAPI.delete(id);
        fetchAccounts();
      } catch (error) {
        console.error('Error deleting account:', error);
      }
    }
  };
  
  if (loading) return <div className="p-8">Loading accounts...</div>;
  
  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Social Media Accounts</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
        >
          <FiPlus /> Add Account
        </button>
      </div>
      
      {showForm && (
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-bold mb-4">Add New Account</h2>
          <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Platform</label>
              <select
                value={formData.platform}
                onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              >
                <option value="instagram">Instagram</option>
                <option value="tiktok">TikTok</option>
                <option value="facebook">Facebook</option>
                <option value="linkedin">LinkedIn</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Username</label>
              <input
                type="text"
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Account Name</label>
              <input
                type="text"
                value={formData.account_name}
                onChange={(e) => setFormData({ ...formData, account_name: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Account ID</label>
              <input
                type="text"
                value={formData.account_id}
                onChange={(e) => setFormData({ ...formData, account_id: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Account Type</label>
              <select
                value={formData.account_type}
                onChange={(e) => setFormData({ ...formData, account_type: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              >
                <option value="business">Business</option>
                <option value="creator">Creator</option>
                <option value="personal">Personal</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Access Token</label>
              <input
                type="password"
                value={formData.access_token}
                onChange={(e) => setFormData({ ...formData, access_token: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                required
              />
            </div>
            
            <button type="submit" className="col-span-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">
              Create Account
            </button>
          </form>
        </div>
      )}
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {accounts.map((account) => (
          <div key={account.id} className="bg-white rounded-lg shadow p-6">
            <div className="flex items-start justify-between mb-4">
              <div>
                <h3 className="font-bold text-gray-900">{account.account_name || account.username}</h3>
                <p className="text-sm text-gray-500 capitalize">{account.platform}</p>
              </div>
              {account.is_verified && <FiCheck className="text-blue-500" size={20} />}
            </div>
            
            <div className="text-sm text-gray-600 mb-4">
              <p>Type: {account.account_type}</p>
              <p>Followers: {account.followers_count.toLocaleString()}</p>
            </div>
            
            <div className="flex gap-2">
              <button className="flex-1 px-3 py-1 text-sm bg-blue-50 text-blue-600 rounded hover:bg-blue-100 flex items-center justify-center gap-1">
                <FiEdit2 size={16} /> Edit
              </button>
              <button
                onClick={() => handleDelete(account.id)}
                className="flex-1 px-3 py-1 text-sm bg-red-50 text-red-600 rounded hover:bg-red-100 flex items-center justify-center gap-1"
              >
                <FiTrash2 size={16} /> Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Accounts;
