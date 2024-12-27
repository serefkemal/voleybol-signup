import React, { useEffect, useState } from 'react';

const Main = () => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  
  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await fetch('/auth/check');
      setIsAuthenticated(response.ok);
    } catch (error) {
      setIsAuthenticated(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
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
  );
};

export default Main;