import React, { useState, useEffect } from 'react';
import { Card, CardHeader, CardTitle, CardContent } from './ui/card';
import { format, parseISO } from 'date-fns';

const GameSignup = () => {
  const [game, setGame] = useState(null);
  const [isSignedUp, setIsSignedUp] = useState(false);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetchGameData();
  }, []);

  const fetchGameData = async () => {
    try {
      const gameId = window.location.pathname.split('/').pop();
      const [gameData, signupData] = await Promise.all([
        fetch(`/admin/games/${gameId}/details`).then(r => r.json()),
        fetch(`/game/${gameId}/check_signup`).then(r => r.json())
      ]);
      setGame(gameData);
      setIsSignedUp(signupData.is_signed_up);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSignup = async () => {
    try {
      const gameId = window.location.pathname.split('/').pop();
      const response = await fetch(`/game/${gameId}/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });

      const result = await response.json();
      if (response.ok) {
        setMessage(result.message);
        setIsSignedUp(true);
      } else {
        setError(result.error);
      }
    } catch (error) {
      setError('Failed to sign up');
    }
  };

  const handleCancel = async () => {
    try {
      const gameId = window.location.pathname.split('/').pop();
      const response = await fetch(`/game/${gameId}/cancel`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      });

      const result = await response.json();
      if (response.ok) {
        setMessage(result.message);
        setIsSignedUp(false);
      } else {
        setError(result.error);
      }
    } catch (error) {
      setError('Failed to cancel signup');
    }
  };

  if (loading) return <div className="p-4">Loading...</div>;
  if (!game) return <div className="p-4">Game not found</div>;

  return (
    <div className="max-w-md mx-auto p-4">
      <Card>
        <CardHeader>
          <CardTitle>Game Details</CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-2 gap-4">
          <div>
            <p className="font-filsonsoft">Date:</p>
            <p>{format(parseISO(game.date), 'MMMM d, yyyy')}</p>
          </div>
          <div>
            <p className="font-filsonsoft">Time:</p>
            <p>{game.start_time} - {game.end_time}</p>
          </div>
          <div>
            <p className="font-filsonsoft">Location:</p>
            <p>{game.location}</p>
          </div>
          <div>
            <p className="font-filsonsoft">Players:</p>
            <p>{game.player_count} / {game.max_players}</p>
          </div>
        </CardContent>
      </Card>

      <div className="mt-4">
        {isSignedUp ? (
          <>
            <div className="mb-4 p-2 bg-green-100 text-green-700 rounded">
              You are signed up for this game!
            </div>
            <button
              onClick={handleCancel}
              className="w-full bg-red-500 text-white p-2 rounded hover:bg-red-600"
            >
              Cancel Signup
            </button>
          </>
        ) : (
          <button
            onClick={handleSignup}
            className="w-full bg-green-500 text-white p-2 rounded hover:bg-green-600"
          >
            Sign Up
          </button>
        )}
        {message && <div className="mt-4 p-2 bg-green-100 text-green-700 rounded">{message}</div>}
        {error && <div className="mt-4 p-2 bg-red-100 text-red-700 rounded">{error}</div>}
      </div>
    </div>
  );
};

export default GameSignup;