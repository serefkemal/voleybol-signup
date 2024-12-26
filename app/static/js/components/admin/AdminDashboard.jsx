import React, { useState, useEffect } from 'react';
import { 
  format, 
  startOfMonth, 
  endOfMonth, 
  eachDayOfInterval, 
  isSameDay,
  startOfWeek,
  endOfWeek,
  isToday,
  parseISO
} from 'date-fns';
import {
  AlertDialog,
  AlertDialogContent,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogCancel,
  AlertDialogAction,
} from '../../components/ui/alert-dialog';

const AdminDashboard = () => {
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [games, setGames] = useState([]);
  const [selectedDate, setSelectedDate] = useState(null);
  const [selectedGame, setSelectedGame] = useState(null);
  const [isGameDialogOpen, setIsGameDialogOpen] = useState(false);
  const [isCreateDialogOpen, setIsCreateDialogOpen] = useState(false);
  const [newGameData, setNewGameData] = useState({
    location: '',
    start_time: '19:00',
    end_time: '21:00'
  });
  const [error, setError] = useState('');

  useEffect(() => {
    fetchGames();
  }, [currentMonth]);

  const fetchGames = async () => {
    try {
      const startDate = format(startOfMonth(currentMonth), 'yyyy-MM-dd');
      const endDate = format(endOfMonth(currentMonth), 'yyyy-MM-dd');
      
      const response = await fetch(`/admin/games?start=${startDate}&end=${endDate}`);
      if (response.ok) {
        const data = await response.json();
        setGames(data);
      }
    } catch (error) {
      console.error('Error fetching games:', error);
    }
  };

  const handleCreateGame = async () => {
    try {
      const response = await fetch('/admin/games', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          date: format(selectedDate, 'yyyy-MM-dd'),
          ...newGameData
        }),
      });

      if (response.ok) {
        await fetchGames();
        setIsCreateDialogOpen(false);
        setNewGameData({
          location: '',
          start_time: '19:00',
          end_time: '21:00'
        });
        setError('');
      } else {
        const data = await response.json();
        setError(data.error || 'Failed to create game');
      }
    } catch (error) {
      console.error('Error creating game:', error);
      setError('Failed to create game');
    }
  };

  const handleGameClick = (game) => {
    setSelectedGame(game);
    setIsGameDialogOpen(true);
  };

  const handleManageGame = (gameId) => {
    window.location.href = `/admin/games/${gameId}`;
  };

  const renderCreateGameDialog = () => {
    if (!selectedDate) return null;

    return (
      <AlertDialog open={isCreateDialogOpen} onOpenChange={setIsCreateDialogOpen}>
        <AlertDialogContent>
        <AlertDialogHeader>
            <AlertDialogTitle>Create New Game</AlertDialogTitle>
            <AlertDialogDescription>
              <div className="space-y-4 pt-4">
                <div>
                  <p className="font-semibold mb-2">Date:</p>
                  <p>{format(selectedDate, 'MMMM d, yyyy')}</p>
                </div>
                <div>
                  <label className="block font-semibold mb-2">Location:</label>
                  <input
                    type="text"
                    value={newGameData.location}
                    onChange={(e) => setNewGameData({ ...newGameData, location: e.target.value })}
                    className="w-full p-2 border rounded"
                    required
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="block font-semibold mb-2">Start Time:</label>
                    <input
                      type="time"
                      value={newGameData.start_time}
                      onChange={(e) => setNewGameData({ ...newGameData, start_time: e.target.value })}
                      className="w-full p-2 border rounded"
                      required
                    />
                  </div>
                  <div>
                    <label className="block font-semibold mb-2">End Time:</label>
                    <input
                      type="time"
                      value={newGameData.end_time}
                      onChange={(e) => setNewGameData({ ...newGameData, end_time: e.target.value })}
                      className="w-full p-2 border rounded"
                      required
                    />
                  </div>
                </div>
                {error && (
                  <div className="text-red-500 text-sm">{error}</div>
                )}
              </div>
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel onClick={() => setError('')}>Cancel</AlertDialogCancel>
            <AlertDialogAction
              onClick={handleCreateGame}
              className="bg-green-500 hover:bg-green-600 text-white"
            >
              Create Game
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    );
  };

  const renderGameDialog = () => {
    if (!selectedGame) return null;

    return (
      <AlertDialog open={isGameDialogOpen} onOpenChange={setIsGameDialogOpen}>
        <AlertDialogContent>
        <AlertDialogHeader>
            <AlertDialogTitle>Game Details</AlertDialogTitle>
            <AlertDialogDescription>
              <div className="space-y-4">
                <div>
                  <p className="font-semibold">Date:</p>
                  <p>{format(parseISO(selectedGame.date), 'MMMM d, yyyy')}</p>
                </div>
                <div>
                  <p className="font-semibold">Location:</p>
                  <p>{selectedGame.location}</p>
                </div>
                <div>
                  <p className="font-semibold">Time:</p>
                  <p>{selectedGame.start_time} - {selectedGame.end_time}</p>
                </div>
                <div>
                  <p className="font-semibold">Players:</p>
                  <p>{selectedGame.player_count || 0} / {selectedGame.max_players}</p>
                </div>
              </div>
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Close</AlertDialogCancel>
            <AlertDialogAction
              onClick={() => handleManageGame(selectedGame.id)}
              className="bg-blue-500 hover:bg-blue-600 text-white"
            >
              Manage Game
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>
    );
  };

  const renderCalendar = () => {
    const monthStart = startOfMonth(currentMonth);
    const monthEnd = endOfMonth(currentMonth);
    const calendarStart = startOfWeek(monthStart);
    const calendarEnd = endOfWeek(monthEnd);
    
    const days = eachDayOfInterval({ start: calendarStart, end: calendarEnd });

    return (
      <div>
        <div className="flex justify-between items-center mb-4 bg-gray-50 p-3 rounded-t-lg">
          <button
            onClick={() => {
              setSelectedDate(null);
              setCurrentMonth(prev => new Date(prev.getFullYear(), prev.getMonth() - 1));
            }}
            className="px-3 py-1 text-gray-600 hover:bg-gray-200 rounded"
          >
            ←
          </button>
          <h2 className="text-xl font-semibold">
            {format(currentMonth, 'MMMM yyyy')}
          </h2>
          <button
            onClick={() => {
              setSelectedDate(null);
              setCurrentMonth(prev => new Date(prev.getFullYear(), prev.getMonth() + 1));
            }}
            className="px-3 py-1 text-gray-600 hover:bg-gray-200 rounded"
          >
            →
          </button>
        </div>

        <div className="grid grid-cols-7 gap-1 mb-1">
          {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
            <div key={day} className="text-center text-sm font-medium text-gray-500 py-1">
              {day}
            </div>
          ))}
        </div>

        <div className="grid grid-cols-7 gap-1">
          {days.map(day => {
            const gamesOnDay = games.filter(g => isSameDay(parseISO(g.date), day));
            const isCurrentMonth = day.getMonth() === currentMonth.getMonth();
            const isSelected = isSameDay(day, selectedDate);
            
            return (
              <div
                key={day.toISOString()}
                onClick={() => setSelectedDate(isSelected ? null : day)}
                className={`
                  h-20 p-1 border rounded relative
                  ${!isCurrentMonth ? 'bg-gray-50 text-gray-400' : 'bg-white'}
                  ${isSelected ? 'ring-2 ring-orange-400' : ''}
                  ${isToday(day) ? 'border-orange-500' : 'border-gray-200'}
                  hover:bg-gray-50 transition-colors
                `}
              >
                <div className={`text-sm ${isToday(day) ? 'font-bold text-orange-500' : ''}`}>
                  {format(day, 'd')}
                </div>
                
                {gamesOnDay.length > 0 && (
                  <div className="mt-1 space-y-1">
                    {gamesOnDay.map(game => (
                      <div
                        key={game.id}
                        onClick={(e) => {
                          e.stopPropagation();
                          handleGameClick(game);
                        }}
                        className="px-1.5 py-0.5 rounded cursor-pointer text-xs"
                        style={{
                          backgroundColor: '#FF7F2A',
                          color: '#8B4513'
                        }}
                      >
                        {game.start_time}
                      </div>
                    ))}
                  </div>
                )}

                {/* Add Game Button - only show when date is selected */}
                {isCurrentMonth && isSelected && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setIsCreateDialogOpen(true);
                    }}
                    className="absolute bottom-1 right-1 w-6 h-6 rounded-full bg-green-500 text-white flex items-center justify-center hover:bg-green-600 transition-colors"
                    title="Add game"
                  >
                    <span className="text-lg leading-none">+</span>
                  </button>
                )}
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <div className="max-w-4xl mx-auto p-4">
      <div className="bg-white rounded-lg shadow">
        {renderCalendar()}
      </div>
      {renderGameDialog()}
      {renderCreateGameDialog()}
    </div>
  );
};

export default AdminDashboard;