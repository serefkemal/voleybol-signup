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
    <div className="min-h-screen bg-[#1e2a4a] flex flex-col items-center justify-center p-4">
      <a href="/" className="flex flex-col items-center">
        <img src="/static/logo.svg" alt="Volla Logo" className="w-48 mb-4"/>
        <img src="/static/banner.svg" alt="Volla" className="w-48 mb-6"/>
      </a>
      {/* <div className="space-y-1 w-full max-w-sm"></div> */}
      {isAuthenticated && (
        // <div className="absolute top-4 right-4 space-x-4">
        <div className="absolute top-4 right-4 space-x-4">
          {isAdmin && (
            <button
              onClick={() => window.location.href = '/admin/dashboard'}
              className="px-4 py-2 bg-orange-500 text-white rounded hover:bg-orange-600 font-filsonsoft"
            >
              Manage Games
            </button>
          )}
          <button
            onClick={handleLogout}
            className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 font-filsonsoft"
          >
            Logout
          </button>
        </div>
      )}
      {/* <div className="flex items-center justify-center min-h-screen"> */}
      <div className="flex items-center justify-center">
        <div className="space-y-4">
          {isAuthenticated ? (
            <button
              onClick={() => window.location.href = '/signup/dashboard'}
              className="w-48 p-4 bg-green-500 text-white rounded-lg hover:bg-green-600 block font-filsonsoft"
            >
              View Games
            </button>
          ) : (
            <>
              <button
                onClick={() => window.location.href = '/auth/signup'}
                className="w-full p-4 bg-[#FF7F2A] text-white rounded-lg hover:bg-[#ff6a00] text-xl font-filsonsoft"
              >
                Üye Ol
              </button>
              <button
                onClick={() => window.location.href = '/auth/login'}
                className="w-full p-4 bg-[#FF7F2A] text-white rounded-lg hover:bg-[#ff6a00] text-xl font-filsonsoft"
              >
                Giriş
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Main;