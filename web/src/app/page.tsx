'use client';

import { useState } from 'react';

export default function Home() {
  const [framework, setFramework] = useState('fastapi');
  const [projectName, setProjectName] = useState('my-awesome-project');
  const [dbEnabled, setDbEnabled] = useState(true);
  const [redisEnabled, setRedisEnabled] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    try {
      const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
      const response = await fetch(`${API_URL}/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          framework,
          project_name: projectName,
          db_enabled: dbEnabled,
          redis_enabled: redisEnabled,
        }),
      });

      if (!response.ok) throw new Error('Generate failed');

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${projectName}.zip`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error:', error);
      alert('Gagal generate project! Pastikan backend DocKit nyala di port 8000.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white p-8">
      <div className="max-w-2xl mx-auto">
        <h1 className="text-5xl font-bold mb-2 text-center bg-gradient-to-r from-blue-400 to-purple-400 bg-clip-text text-transparent">
          DocKit
        </h1>
        <p className="text-center text-gray-400 mb-12">
          Generate production-ready project boilerplates in seconds
        </p>

        <div className="bg-white/10 backdrop-blur-lg rounded-2xl p-8 shadow-2xl border border-white/20">
          <div className="space-y-6">
            <div>
              <label className="block text-sm font-medium mb-2 text-gray-300">
                Project Name
              </label>
              <input
                type="text"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-white"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-2 text-gray-300">
                Framework
              </label>
              <select
                value={framework}
                onChange={(e) => setFramework(e.target.value)}
                className="w-full px-4 py-3 bg-white/5 border border-white/20 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500 text-white"
              >
                <option value="fastapi" className="bg-slate-800">FastAPI</option>
                <option value="laravel" disabled className="bg-slate-800">
                  Laravel (Coming Soon)
                </option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-3 text-gray-300">
                Add-ons
              </label>
              <div className="space-y-3">
                <label className="flex items-center space-x-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={dbEnabled}
                    onChange={(e) => setDbEnabled(e.target.checked)}
                    className="w-5 h-5 rounded"
                  />
                  <span>PostgreSQL</span>
                </label>
                <label className="flex items-center space-x-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={redisEnabled}
                    onChange={(e) => setRedisEnabled(e.target.checked)}
                    className="w-5 h-5 rounded"
                  />
                  <span>Redis</span>
                </label>
              </div>
            </div>

            <button
              onClick={handleGenerate}
              disabled={loading}
              className="w-full py-4 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg font-semibold text-lg hover:from-blue-600 hover:to-purple-600 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? 'Generating...' : 'Generate Project'}
            </button>
          </div>
        </div>

        <p className="text-center text-sm text-gray-500 mt-8">
          Powered by FastAPI + Jinja2 + Docker
        </p>
      </div>
    </div>
  );
}