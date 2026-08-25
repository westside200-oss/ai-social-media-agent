import React, { useEffect, useState } from 'react';
import { postsAPI, accountsAPI } from '../api/client';
import { FiSend, FiTrash2, FiEye } from 'react-icons/fi';

const Posts = () => {
  const [posts, setPosts] = useState([]);
  const [accounts, setAccounts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    account_id: '',
    platform: 'instagram',
    theme: 'new_arrivals',
    template: '',
    additional_context: '',
  });
  
  useEffect(() => {
    fetchData();
  }, []);
  
  const fetchData = async () => {
    try {
      const [postsRes, accountsRes] = await Promise.all([
        postsAPI.list({}),
        accountsAPI.list({ is_active: true }),
      ]);
      setPosts(postsRes.data);
      setAccounts(accountsRes.data);
    } catch (error) {
      console.error('Error fetching data:', error);
    } finally {
      setLoading(false);
    }
  };
  
  const handleGenerate = async (e) => {
    e.preventDefault();
    try {
      await postsAPI.generate(formData);
      setFormData({
        account_id: '',
        platform: 'instagram',
        theme: 'new_arrivals',
        template: '',
        additional_context: '',
      });
      setShowForm(false);
      fetchData();
    } catch (error) {
      console.error('Error generating post:', error);
    }
  };
  
  const handlePublish = async (postId) => {
    try {
      await postsAPI.publish(postId);
      fetchData();
    } catch (error) {
      console.error('Error publishing post:', error);
    }
  };
  
  if (loading) return <div className="p-8">Loading posts...</div>;
  
  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Posts</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
        >
          Generate Post
        </button>
      </div>
      
      {showForm && (
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-bold mb-4">Generate AI Post</h2>
          <form onSubmit={handleGenerate} className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Account</label>
              <select
                value={formData.account_id}
                onChange={(e) => setFormData({ ...formData, account_id: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                required
              >
                <option value="">Select Account</option>
                {accounts.map((acc) => (
                  <option key={acc.id} value={acc.id}>
                    {acc.username} ({acc.platform})
                  </option>
                ))}
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Platform</label>
              <select
                value={formData.platform}
                onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              >
                <option value="instagram">Instagram</option>
                <option value="tiktok">TikTok</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Theme</label>
              <select
                value={formData.theme}
                onChange={(e) => setFormData({ ...formData, theme: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
              >
                <option value="new_arrivals">New Arrivals</option>
                <option value="styling_tips">Styling Tips</option>
                <option value="promotion">Promotion</option>
                <option value="fabric_education">Fabric Education</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Template (Optional)</label>
              <input
                type="text"
                value={formData.template}
                onChange={(e) => setFormData({ ...formData, template: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                placeholder="e.g., question_format"
              />
            </div>
            
            <div className="col-span-2">
              <label className="block text-sm font-medium text-gray-700 mb-1">Additional Context</label>
              <textarea
                value={formData.additional_context}
                onChange={(e) => setFormData({ ...formData, additional_context: e.target.value })}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg"
                rows="3"
                placeholder="Any specific details for the content..."
              />
            </div>
            
            <button type="submit" className="col-span-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700">
              Generate
            </button>
          </form>
        </div>
      )}
      
      <div className="space-y-4">
        {posts.map((post) => (
          <div key={post.id} className="bg-white rounded-lg shadow p-6">
            <div className="flex justify-between items-start mb-4">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="px-2 py-1 text-xs font-semibold rounded-full bg-purple-100 text-purple-800">
                    {post.platform}
                  </span>
                  {post.is_posted ? (
                    <span className="px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
                      Posted
                    </span>
                  ) : (
                    <span className="px-2 py-1 text-xs font-semibold rounded-full bg-yellow-100 text-yellow-800">
                      Draft
                    </span>
                  )}
                </div>
                <p className="text-sm text-gray-600 mb-2">{post.content}</p>
              </div>
            </div>
            
            <div className="flex gap-2">
              {!post.is_posted && (
                <button
                  onClick={() => handlePublish(post.id)}
                  className="flex items-center gap-2 px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  <FiSend size={16} /> Publish
                </button>
              )}
              {post.is_posted && (
                <button className="flex items-center gap-2 px-3 py-1 text-sm bg-gray-100 text-gray-600 rounded hover:bg-gray-200">
                  <FiEye size={16} /> View Analytics
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Posts;
