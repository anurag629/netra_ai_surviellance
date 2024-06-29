import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="bg-saffron p-4 shadow-md">
      <div className="container mx-auto flex justify-between">
        <div className="text-white text-xl font-bold">Surveillance System</div>
        <div className="flex space-x-4">
          <Link to="/" className="text-white">Dashboard</Link>
          <Link to="/manage" className="text-white">Manage</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
