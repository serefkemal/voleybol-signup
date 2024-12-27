import React, { useEffect, useState } from 'react';

const Main = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isAdmin, setIsAdmin] = useState(false);
  
  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await fetch('/auth/check');
      const data = await response.json();
      setIsAuthenticated(response.ok);
      setIsAdmin(data.isAdmin);
    } catch (error) {
      setIsAuthenticated(false);
      setIsAdmin(false);
    }
  };

  const handleLogout = async () => {
    try {
      await fetch('/auth/logout');
      window.location.href = '/';
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {isAuthenticated && (
        <div className="absolute top-4 right-4 space-x-4">
          {isAdmin && (
            <button
              onClick={() => window.location.href = '/admin/dashboard'}
              className="px-4 py-2 bg-orange-500 text-white rounded hover:bg-orange-600"
            >
              Manage Games
            </button>
          )}
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
          >
            Logout
          </button>
        </div>
      )}
      <div className="flex items-center justify-center min-h-screen">
        <div className="space-y-4">
          {isAuthenticated ? (
            <button
              onClick={() => window.location.href = '/signup/dashboard'}
              className="w-48 p-4 bg-green-500 text-white rounded-lg hover:bg-green-600 block"
            >
              View Games
            </button>
          ) : (
            <>
              <button
                onClick={() => window.location.href = '/auth/login'}
                className="w-48 p-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 block"
              >
                Login
              </button>
              <button
                onClick={() => window.location.href = '/auth/signup'}
                className="w-48 p-4 bg-green-500 text-white rounded-lg hover:bg-green-600 block"
              >
                Sign Up
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Main;