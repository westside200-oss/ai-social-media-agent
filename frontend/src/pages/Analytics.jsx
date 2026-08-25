import React, { useEffect, useState } from 'react';
import { analyticsAPI } from '../api/client';
import { FiBarChart2, FiTrendingUp } from 'react-icons/fi';

const Analytics = () => {
  const [insights, setInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedPlatform, setSelectedPlatform] = useState('instagram');
  
  useEffect(() => {
    fetchInsights();
  }, [selectedPlatform]);
  
  const fetchInsights = async () => {
    try {
      const response = await analyticsAPI.getInsights({ platform: selectedPlatform });
      setInsights(response.data);
    } catch (error) {
      console.error('Error fetching insights:', error);
    } finally {
      setLoading(false);
    }
  };
  
  if (loading) return <div className="p-8">Loading analytics...</div>;
  
  return (
    <div className="p-8">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Analytics & Insights</h1>
        <select
          value={selectedPlatform}
          onChange={(e) => setSelectedPlatform(e.target.value)}
          className="px-4 py-2 border border-gray-300 rounded-lg"
        >
          <option value="instagram">Instagram</option>
          <option value="tiktok">TikTok</option>
        </select>
      </div>
      
      {insights && (
        <div className="grid grid-cols-1 gap-6">
          {/* Top Themes */}
          {insights.top_themes && (
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center gap-2 mb-4">
                <FiBarChart2 className="text-purple-600" />
                <h2 className="text-xl font-bold">Top Performing Themes</h2>
              </div>
              <div className="space-y-3">
                {insights.top_themes.map(([theme, rate], idx) => (
                  <div key={idx} className="flex justify-between items-center">
                    <span className="font-medium text-gray-900">{theme}</span>
                    <div className="flex items-center gap-2">
                      <div className="w-48 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-purple-600 h-2 rounded-full"
                          style={{ width: `${Math.min(rate * 20, 100)}%` }}
                        />
                      </div>
                      <span className="text-sm font-semibold text-gray-600">{rate.toFixed(1)}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
          
          {/* Top Hashtags */}
          {insights.top_hashtags && (
            <div className="bg-white rounded-lg shadow p-6">
              <div className="flex items-center gap-2 mb-4">
                <FiTrendingUp className="text-pink-600" />
                <h2 className="text-xl font-bold">Top Performing Hashtags</h2>
              </div>
              <div className="flex flex-wrap gap-2">
                {insights.top_hashtags.slice(0, 10).map(([tag, rate], idx) => (
                  <span
                    key={idx}
                    className="px-3 py-1 bg-pink-100 text-pink-700 rounded-full text-sm font-medium"
                  >
                    {tag} ({rate.toFixed(1)}%)
                  </span>
                ))}
              </div>
            </div>
          )}
          
          {/* Recommendations */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">Recommendations</h2>
            <ul className="space-y-2">
              <li className="flex items-start gap-2">
                <span className="text-green-600 font-bold mt-1">✓</span>
                <span className="text-gray-700">Focus on top-performing themes for consistent engagement</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-600 font-bold mt-1">✓</span>
                <span className="text-gray-700">Use trending hashtags to increase reach and discoverability</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-600 font-bold mt-1">✓</span>
                <span className="text-gray-700">Post at 12:00 PM and 6:00 PM Cameroon Time for optimal reach</span>
              </li>
              <li className="flex items-start gap-2">
                <span className="text-green-600 font-bold mt-1">✓</span>
                <span className="text-gray-700">Engage with audience through captions that encourage comments</span>
              </li>
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default Analytics;
