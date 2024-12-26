import React, { useState, useEffect } from 'react';
import { format, parseISO } from 'date-fns';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/card';
import { ChevronDown, ChevronRight } from 'lucide-react';

const GameDashboard = () => {
  const [game, setGame] = useState(null);
  const [players, setPlayers] = useState([]);
  const [expandedPlayer, setExpandedPlayer] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchGameData();
  }, []);

  const fetchGameData = async () => {
    try {
      const gameId = window.location.pathname.split('/').pop();
      const [gameData, playersData] = await Promise.all([
        fetch(`/admin/games/${gameId}/details`).then(r => r.json()),
        fetch(`/admin/games/${gameId}/players`).then(r => r.json())
      ]);
      setGame(gameData);
      setPlayers(playersData);
    } catch (error) {
      console.error('Error fetching game data:', error);
    } finally {
      setLoading(false);
    }
  };

  const togglePlayerExpand = (playerId) => {
    setExpandedPlayer(expandedPlayer === playerId ? null : playerId);
  };

  if (loading) return <div className="p-4">Loading...</div>;
  if (!game) return <div className="p-4">Game not found</div>;

  return (
    <div className="max-w-4xl mx-auto p-4 space-y-6">
      <Card>
        <CardHeader>
          <CardTitle>Game Details</CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-2 gap-4">
          <div>
            <p className="font-semibold">Date:</p>
            <p>{format(parseISO(game.date), 'MMMM d, yyyy')}</p>
          </div>
          <div>
            <p className="font-semibold">Time:</p>
            <p>{game.start_time} - {game.end_time}</p>
          </div>
          <div>
            <p className="font-semibold">Location:</p>
            <p>{game.location}</p>
          </div>
          <div>
            <p className="font-semibold">Players:</p>
            <p>{game.player_count} / {game.max_players}</p>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Player List</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-2">
            {players.map((player, index) => (
              <div key={player.id} className="border rounded-lg overflow-hidden">
                <div 
                  className="p-3 bg-gray-50 flex items-center cursor-pointer"
                  onClick={() => togglePlayerExpand(player.id)}
                >
                  {expandedPlayer === player.id ? 
                    <ChevronDown className="w-4 h-4 mr-2" /> : 
                    <ChevronRight className="w-4 h-4 mr-2" />
                  }
                  <span>{index + 1}. {player.name}</span>
                </div>
                
                {expandedPlayer === player.id && (
                  <div className="p-3 bg-white border-t">
                    <div className="grid grid-cols-2 gap-2 text-sm">
                      <div>
                        <p className="font-semibold">Email:</p>
                        <p className="text-gray-600">{player.email}</p>
                      </div>
                      <div>
                        <p className="font-semibold">Phone:</p>
                        <p className="text-gray-600">{player.phone}</p>
                      </div>
                      <div className="col-span-2">
                        <p className="font-semibold">Signed up:</p>
                        <p className="text-gray-600">
                          {format(parseISO(player.signup_time), 'MMM d, h:mm a')}
                        </p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ))}
            {players.length === 0 && (
              <div className="text-gray-500 text-center py-4">
                No players signed up yet
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default GameDashboard;