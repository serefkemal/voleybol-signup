import React, { useState, useEffect } from 'react';
import { 
  format, 
  startOfMonth, 
  endOfMonth, 
  eachDayOfInterval, 
  isSameDay,
  startOfWeek,
  endOfWeek,
  isToday
} from 'date-fns';

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

  const renderCalendar = () => {
    const monthStart = startOfMonth(currentMonth);
    const monthEnd = endOfMonth(currentMonth);
    const calendarStart = startOfWeek(monthStart);
    const calendarEnd = endOfWeek(monthEnd);
    
    const days = eachDayOfInterval({ start: calendarStart, end: calendarEnd });

    return (
      <div>
        {/* Calendar header with month and navigation */}
        <div className="flex justify-between items-center mb-4 bg-gray-50 p-3 rounded-t-lg">
          <button
            onClick={() => setCurrentMonth(prev => new Date(prev.getFullYear(), prev.getMonth() - 1))}
            className="px-3 py-1 text-gray-600 hover:bg-gray-200 rounded"
          >
            ←
          </button>
          <h2 className="text-xl font-semibold">
            {format(currentMonth, 'MMMM yyyy')}
          </h2>
          <button
            onClick={() => setCurrentMonth(prev => new Date(prev.getFullYear(), prev.getMonth() + 1))}
            className="px-3 py-1 text-gray-600 hover:bg-gray-200 rounded"
          >
            →
          </button>
        </div>

        {/* Days of week headers */}
        <div className="grid grid-cols-7 gap-1 mb-1">
          {['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].map(day => (
            <div key={day} className="text-center text-sm font-medium text-gray-500 py-1">
              {day}
            </div>
          ))}
        </div>

        {/* Calendar grid */}
        <div className="grid grid-cols-7 gap-1">
          {days.map(day => {
            const game = games.find(g => isSameDay(new Date(g.date), day));
            const isCurrentMonth = day.getMonth() === currentMonth.getMonth();
            
            return (
              <div
                key={day.toISOString()}
                onClick={() => setSelectedDate(day)}
                className={`
                  h-20 p-1 border rounded cursor-pointer relative
                  ${!isCurrentMonth ? 'bg-gray-50 text-gray-400' : 'bg-white'}
                  ${isSameDay(day, selectedDate) ? 'ring-2 ring-blue-400' : ''}
                  ${isToday(day) ? 'border-blue-500' : 'border-gray-200'}
                  hover:bg-gray-50 transition-colors
                `}
              >
                <div className={`text-sm ${isToday(day) ? 'font-bold text-blue-500' : ''}`}>
                  {format(day, 'd')}
                </div>
                
                {game && (
                  <div className="mt-1">
                    <span className="inline-block px-1.5 py-0.5 bg-blue-100 text-blue-800 text-xs rounded">
                      Game
                    </span>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleManageGame(game.id);
                      }}
                      className="mt-1 text-xs bg-blue-500 text-white px-2 py-0.5 rounded hover:bg-blue-600 w-full"
                    >
                      Manage
                    </button>
                  </div>
                )}
                
                {isSameDay(day, selectedDate) && !game && isCurrentMonth && (
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      handleCreateGame();
                    }}
                    className="absolute bottom-1 right-1 text-xs bg-green-500 text-white px-2 py-0.5 rounded hover:bg-green-600"
                  >
                    +
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
    </div>
  );
};

export default AdminDashboard;