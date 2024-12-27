import React, { useState } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';

const Signup = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    password: ''
  });
  const [error, setError] = useState('');

  const formatPhoneNumber = (value) => {
    const digits = value.replace(/\D/g, '');
    if (digits.length <= 10 && digits.startsWith('5')) {
      return digits.replace(/(\d{3})(\d{3})(\d{2})(\d{2})/, '($1) $2 $3 $4').trim();
    }
    return '';
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      
      if (response.ok) {
        window.location.href = '/signup/dashboard';
      } else {
        setError(data.error);
      }
    } catch (error) {
      setError('Network error');
    }
  };

  return (
    <div className="max-w-md mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>Sign Up</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <input
              type="text"
              placeholder="Name"
              value={formData.name}
              onChange={(e) => setFormData({...formData, name: e.target.value})}
              className="w-full p-2 border rounded"
              required
            />
            <input
              type="email"
              placeholder="Email"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
              className="w-full p-2 border rounded"
              required
            />
            <input
              type="tel"
              placeholder="(5xx) xxx xx xx"
              value={formData.phone}
              onChange={(e) => setFormData({...formData, phone: formatPhoneNumber(e.target.value)})}
              pattern="\(5[0-9]{2}\) [0-9]{3} [0-9]{2} [0-9]{2}"
              className="w-full p-2 border rounded"
              required
              maxLength={15}
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
              className="w-full bg-green-500 text-white p-2 rounded hover:bg-green-600"
            >
              Sign Up
            </button>
          </form>
          <div className="mt-4 text-center">
            <a href="/auth/login" className="text-blue-500 hover:underline">
              Already have an account? Login
            </a>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Signup;