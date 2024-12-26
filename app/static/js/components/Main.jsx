import React from 'react';

const Main = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50">
      <div className="space-y-4">
        <button
          onClick={() => window.location.href = '/signup/dashboard'}
          className="w-48 p-4 bg-green-500 text-white rounded-lg hover:bg-green-600 block"
        >
          Sign Up
        </button>
        <button
          onClick={() => window.location.href = '/admin'}
          className="w-48 p-4 bg-blue-500 text-white rounded-lg hover:bg-blue-600 block"
        >
          Admin
        </button>
      </div>
    </div>
  );
};

export default Main;