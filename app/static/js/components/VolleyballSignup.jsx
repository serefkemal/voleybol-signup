import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { AlertDialog, AlertDialogContent, AlertDialogHeader, AlertDialogFooter, AlertDialogTitle, AlertDialogDescription, AlertDialogCancel, AlertDialogAction } from './ui/alert-dialog';

const VolleyballSignup = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: ''
  });
  const [playerCount, setPlayerCount] = useState(0);
  const [showCancelDialog, setShowCancelDialog] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetchPlayerCount();
  }, []);

  const fetchPlayerCount = async () => {
    try {
      const response = await fetch('/player-count');
      const data = await response.json();
      setPlayerCount(data.count);
    } catch (error) {
      console.error('Error fetching player count:', error);
    }
  };

  const formatPhoneNumber = (value) => {
    const digits = value.replace(/\D/g, '');
    if (digits.length <= 10 && digits.startsWith('5')) {
      return digits.replace(/(\d{3})(\d{3})(\d{2})(\d{2})/, '($1) $2 $3 $4').trim();
    }
    return '';
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');

    try {
      const response = await fetch('/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const result = await response.json();
      
      if (response.status === 400 && result.error === "Player with this phone or email already signed up!") {
        setShowCancelDialog(true);
      } else if (response.ok) {
        setMessage(result.message);
        setFormData({ name: '', email: '', phone: '' });
        fetchPlayerCount();
      } else {
        setError(result.error || 'An unexpected error occurred');
      }
    } catch (error) {
      setError('Network error. Please try again.');
    }
  };

  const handleCancel = async () => {
    try {
      const response = await fetch('/cancel', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      });

      const result = await response.json();
      if (response.ok) {
        setMessage(result.message);
        setFormData({ name: '', email: '', phone: '' });
        setShowCancelDialog(false);
        fetchPlayerCount();
      } else {
        setError(result.error || 'Error canceling signup');
      }
    } catch (error) {
      setError('Network error. Please try again.');
    }
  };

  return (
    <div className="max-w-md mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>Weekly Volleyball Signup</CardTitle>
          <div className="text-sm text-gray-600">Currently signed up: {playerCount} players</div>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData(prev => ({ ...prev, name: e.target.value }))}
                placeholder="Your Name"
                className="w-full p-2 border rounded"
                required
              />
            </div>
            <div>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData(prev => ({ ...prev, email: e.target.value }))}
                placeholder="Your Email"
                className="w-full p-2 border rounded"
                required
              />
            </div>
            <div>
              <input
                type="tel"
                value={formData.phone}
                onChange={(e) => setFormData(prev => ({ ...prev, phone: formatPhoneNumber(e.target.value) }))}
                placeholder="(5xx) xxx xx xx"
                pattern="\(5[0-9]{2}\) [0-9]{3} [0-9]{2} [0-9]{2}"
                className="w-full p-2 border rounded"
                required
                maxLength={15}
              />
            </div>
            <button
              type="submit"
              className="w-full bg-green-500 text-white p-2 rounded hover:bg-green-600"
            >
              Sign Up
            </button>
          </form>

          {message && <div className="mt-4 p-2 bg-green-100 text-green-700 rounded">{message}</div>}
          {error && <div className="mt-4 p-2 bg-red-100 text-red-700 rounded">{error}</div>}
        </CardContent>
      </Card>

      <AlertDialog open={showCancelDialog} onOpenChange={setShowCancelDialog}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Already Signed Up</AlertDialogTitle>
            <AlertDialogDescription>
              You are already signed up for this week's game. Would you like to cancel your signup?
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Keep Signup</AlertDialogCancel>
            <AlertDialogAction onClick={handleCancel} className="bg-red-500 hover:bg-red-600">
              Cancel Signup
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    </div>
  );
};

export default VolleyballSignup;