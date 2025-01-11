import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      
      if (response.ok) {
        // window.location.href = data.isAdmin ? '/admin/dashboard' : '/signup/dashboard';
        window.location.href = '/';
      } else {
        setError(data.error);
      }
    } catch (error) {
      setError('Network error');
    }
  };

  return (
    <div className="min-h-screen bg-[#1e2a4a] flex flex-col items-center justify-center p-4">
      <a href="/" className="flex flex-col items-center">
        <img src="/static/logo.svg" alt="Volla Logo" className="w-48 mb-4"/>
        <img src="/static/banner.svg" alt="Volla" className="w-48 mb-6"/>
      </a>
      <div className="space-y-1 w-full max-w-sm"></div>
      <div className="max-w-md mx-auto p-4">
        <Card>
          <CardHeader>
            <CardTitle>Login</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <input
                type="email"
                placeholder="Email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                className="w-full p-2 border rounded"
                required
              />
              <input
                type="password"
                placeholder="Password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
                className="w-full p-2 border rounded"
                required
              />
              {error && <div className="text-red-500 text-sm">{error}</div>}
              <button
                type="submit"
                className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
              >
                Login
              </button>
            </form>
            <div className="mt-4 text-center">
              <a href="/auth/signup" className="text-blue-500 hover:underline">
                Don't have an account? Sign up
              </a>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Login;