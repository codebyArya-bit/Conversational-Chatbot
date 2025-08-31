import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';

const Navbar: React.FC = () => {
  const { isAuthenticated, isAdmin, user, logout } = useAuth();
  const navigate = useNavigate();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleLogout = () => {
    logout();
    navigate('/');
    setIsMenuOpen(false);
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  return (
    <nav className="bg-blue-600 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo and Brand */}
          <div className="flex items-center">
            <Link to="/" className="flex-shrink-0 flex items-center" onClick={closeMenu}>
              <span className="text-white text-xl font-bold">Student Chatbot</span>
            </Link>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-4">
            {/* Public Links */}
            <Link to="/" className="text-white hover:text-blue-200 px-3 py-2 rounded-md text-sm font-medium transition-colors">
              Home
            </Link>
            <Link to="/about" className="text-white hover:text-blue-200 px-3 py-2 rounded-md text-sm font-medium transition-colors">
              About
            </Link>
            <Link to="/services" className="text-white hover:text-blue-200 px-3 py-2 rounded-md text-sm font-medium transition-colors">
              Services
            </Link>
            <Link to="/resources" className="text-white hover:text-blue-200 px-3 py-2 rounded-md text-sm font-medium transition-colors">
              Resources
            </Link>
            <Link to="/contact" className="text-white hover:text-blue-200 px-3 py-2 rounded-md text-sm font-medium transition-colors">
              Contact
            </Link>

            {/* Authenticated User Links */}
            {isAuthenticated ? (
              <>
                <Link to="/chat" className="text-white hover:text-blue-200 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                  Chat
                </Link>
                <Link to="/chat-history" className="text-white hover:text-blue-200 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                  History
                </Link>
                <Link to="/device-specs" className="text-white hover:text-blue-200 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                  Device Specs
                </Link>
                <Link to="/support" className="text-white hover:text-blue-200 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                  Support
                </Link>
                
                {/* Admin Link */}
                {isAdmin && (
                  <Link to="/admin" className="text-white hover:text-blue-200 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                    Admin
                  </Link>
                )}
                
                {/* User Menu */}
                <div className="relative ml-3">
                  <div className="flex items-center space-x-3">
                    <Link to="/profile" className="text-white hover:text-blue-200 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                      {user?.username}
                    </Link>
                    <button
                      onClick={handleLogout}
                      className="bg-blue-700 hover:bg-blue-800 text-white px-3 py-2 rounded-md text-sm font-medium transition-colors"
                    >
                      Logout
                    </button>
                  </div>
                </div>
              </>
            ) : (
              /* Guest Links */
              <div className="flex items-center space-x-3">
                <Link to="/login" className="text-white hover:text-blue-200 px-3 py-2 rounded-md text-sm font-medium transition-colors">
                  Login
                </Link>
                <Link to="/register" className="bg-blue-700 hover:bg-blue-800 text-white px-3 py-2 rounded-md text-sm font-medium transition-colors">
                  Register
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={toggleMenu}
              className="text-white hover:text-blue-200 focus:outline-none focus:text-blue-200 transition-colors"
            >
              {isMenuOpen ? (
                <XMarkIcon className="h-6 w-6" />
              ) : (
                <Bars3Icon className="h-6 w-6" />
              )}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Navigation Menu */}
      {isMenuOpen && (
        <div className="md:hidden">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3 bg-blue-700">
            {/* Public Links */}
            <Link to="/" className="text-white hover:text-blue-200 block px-3 py-2 rounded-md text-base font-medium transition-colors" onClick={closeMenu}>
              Home
            </Link>
            <Link to="/about" className="text-white hover:text-blue-200 block px-3 py-2 rounded-md text-base font-medium transition-colors" onClick={closeMenu}>
              About
            </Link>
            <Link to="/services" className="text-white hover:text-blue-200 block px-3 py-2 rounded-md text-base font-medium transition-colors" onClick={closeMenu}>
              Services
            </Link>
            <Link to="/resources" className="text-white hover:text-blue-200 block px-3 py-2 rounded-md text-base font-medium transition-colors" onClick={closeMenu}>
              Resources
            </Link>
            <Link to="/contact" className="text-white hover:text-blue-200 block px-3 py-2 rounded-md text-base font-medium transition-colors" onClick={closeMenu}>
              Contact
            </Link>

            {/* Authenticated User Links */}
            {isAuthenticated ? (
              <>
                <Link to="/chat" className="text-white hover:text-blue-200 block px-3 py-2 rounded-md text-base font-medium transition-colors" onClick={closeMenu}>
                  Chat
                </Link>
                <Link to="/chat-history" className="text-white hover:text-blue-200 block px-3 py-2 rounded-md text-base font-medium transition-colors" onClick={closeMenu}>
                  History
                </Link>
                <Link to="/device-specs" className="text-white hover:text-blue-200 block px-3 py-2 rounded-md text-base font-medium transition-colors" onClick={closeMenu}>
                  Device Specs
                </Link>
                <Link to="/support" className="text-white hover:text-blue-200 block px-3 py-2 rounded-md text-base font-medium transition-colors" onClick={closeMenu}>
                  Support
                </Link>
                
                {/* Admin Link */}
                {isAdmin && (
                  <Link to="/admin" className="text-white hover:text-blue-200 block px-3 py-2 rounded-md text-base font-medium transition-colors" onClick={closeMenu}>
                    Admin
                  </Link>
                )}
                
                <Link to="/profile" className="text-white hover:text-blue-200 block px-3 py-2 rounded-md text-base font-medium transition-colors" onClick={closeMenu}>
                  Profile ({user?.username})
                </Link>
                <button
                  onClick={handleLogout}
                  className="text-white hover:text-blue-200 block px-3 py-2 rounded-md text-base font-medium transition-colors w-full text-left"
                >
                  Logout
                </button>
              </>
            ) : (
              /* Guest Links */
              <>
                <Link to="/login" className="text-white hover:text-blue-200 block px-3 py-2 rounded-md text-base font-medium transition-colors" onClick={closeMenu}>
                  Login
                </Link>
                <Link to="/register" className="text-white hover:text-blue-200 block px-3 py-2 rounded-md text-base font-medium transition-colors" onClick={closeMenu}>
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;