import React, { useState, useEffect } from 'react';
import { format, startOfMonth, endOfMonth, eachDayOfInterval, isSameDay } from 'date-fns';

const AdminDashboard = () => {
  const [currentMonth, setCurrentMonth] = useState(new Date());
  const [games, setGames] = useState([]);
  const [selectedDate, setSelectedDate] = useState(null);

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
    if (!selectedDate) return;
    
    try {
      const response = await fetch('/admin/games', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          date: format(selectedDate, 'yyyy-MM-dd'),
          default_game: true
        }),
      });

      if (response.ok) {
        fetchGames();
      }
    } catch (error) {
      console.error('Error creating game:', error);
    }
  };

  const handleManageGame = (gameId) => {
    window.location.href = `/admin/games/${gameId}`;
  };

  const renderCalendar = () => {
    const monthStart = startOfMonth(currentMonth);
    const monthEnd = endOfMonth(currentMonth);
    const days = eachDayOfInterval({ start: monthStart, end: monthEnd });

    return (
      <div className="grid grid-cols-7 gap-1">
        {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
          <div key={day} className="p-2 text-center font-bold">
            {day}
          </div>
        ))}
        {days.map(day => {
          const game = games.find(g => isSameDay(new Date(g.date), day));
          return (
            <div
              key={day.toISOString()}
              onClick={() => setSelectedDate(day)}
              className={`min-h-24 p-2 border rounded-lg cursor-pointer transition-colors
                ${isSameDay(day, selectedDate) ? 'bg-blue-100' : 'hover:bg-gray-50'}
                ${game ? 'border-blue-500' : 'border-gray-200'}`}
            >
              <div className="font-semibold">{format(day, 'd')}</div>
              {game && (
                <div className="mt-1">
                  <div className="text-sm text-blue-600">
                    Game scheduled
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleManageGame(game.id);
                    }}
                    className="mt-1 text-sm bg-blue-500 text-white px-2 py-1 rounded hover:bg-blue-600"
                  >
                    Manage
                  </button>
                </div>
              )}
              {isSameDay(day, selectedDate) && !game && (
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    handleCreateGame();
                  }}
                  className="mt-1 text-sm bg-green-500 text-white px-2 py-1 rounded hover:bg-green-600"
                >
                  Create Game
                </button>
              )}
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <div className="p-4">
      <div className="mb-4 flex justify-between items-center">
        <h1 className="text-2xl font-bold">
          {format(currentMonth, 'MMMM yyyy')}
        </h1>
        <div className="space-x-2">
          <button
            onClick={() => setCurrentMonth(prev => new Date(prev.getFullYear(), prev.getMonth() - 1))}
            className="px-4 py-2 border rounded hover:bg-gray-100"
          >
            Previous
          </button>
          <button
            onClick={() => setCurrentMonth(prev => new Date(prev.getFullYear(), prev.getMonth() + 1))}
            className="px-4 py-2 border rounded hover:bg-gray-100"
          >
            Next
          </button>
        </div>
      </div>
      {renderCalendar()}
    </div>
  );
};

export default AdminDashboard;