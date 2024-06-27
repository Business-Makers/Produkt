import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import { ExchangeProvider } from './ExchangeContext';
import '../Styles/App.css';
import '../Styles/LoggedIn.css';
import Homepage from './Homepage';
import LogIn from './LogIn';
import SignUp from './SignUp';
import Subscription from './Subscription';
import Dashboard from './Dashboard';
import useToken from './useToken';
import SideNav from './SideNav';
import Trading from './Trading';
import Portfolio from './Portfolio';
import Comms from './Comms';
import Profile from './Profile';
import ProfileIcon from './ProfileIcon';
import Settings from './Settings';

/**The Navigation of the whole Frontend: 
 * 
 * Depending on if the User is logged in (decided by the Token's status), different navigation paths are accessible
 * 
 * This is implemented via the use of the BrowserRouter from the package 'react-router-dom'.*/ 
function App() {
  const { token, setToken } = useToken();
  const [isAuthenticated, setIsAuthenticated] = useState(!!token);
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  useEffect(() => {
    setIsAuthenticated(!!token);
  }, [token]);

  const toggleDropdown = () => {
    setIsDropdownOpen(!isDropdownOpen);
  };

  const handleLogOut = () => {
    sessionStorage.removeItem('access_token');
    setIsAuthenticated(false);
  };

  return (
  <ExchangeProvider>
    <Router>
      <div className="App">
        {!isAuthenticated ? (
          <>
            <header className="App-header">
              <nav className="nav">
                <div className="logo">
                  <Link to="/">
                    <img src="/strade.png" alt="logo" />
                  </Link>
                </div>
                <nav className="nav-links">
                  <Link to="/signup">Sign Up</Link>
                  <Link to="/login">Login</Link>
                </nav>
              </nav>
            </header>
            <main>
              <Routes>
                <Route path="/login" element={<LogIn setToken={setToken} />} />
                <Route path="/signup" element={<SignUp />} />
                <Route path="/" element={<Homepage />} />
                <Route path="*" element={<Navigate to="/" />} />
              </Routes>
            </main>
            <footer className="App-footer">
              <div className="footer-content">
                <p>&copy; 2024 $TRADE</p>
                <Link to="/impressum">Impressum</Link>
                <Link to="/datenschutz">Datenschutz</Link>
              </div>
            </footer>
          </>
        ) : (
          <div className="App2">
            <header className="App-header2">
              <SideNav />
              <div className="profile-icon-container">
                <ProfileIcon onClick={toggleDropdown} />
                {isDropdownOpen && (
                  <div className="dropdown-menu">
                    <ul>
                      <li><Link to="/profile">Profile</Link></li>
                      <li><Link to="/settings">Settings</Link></li>
                      <li><button onClick={handleLogOut}>Log Out</button></li>
                    </ul>
                  </div>
                )}
              </div>
            </header>
            <div className="main-content">
              <Routes>
                <Route path="/subscription" element={<Subscription />} />
                <Route path="/trading" element={<Trading />} />
                <Route path="/portfolio" element={<Portfolio />} />
                <Route path="/comms" element={<Comms />} />
                <Route path="/" element={<Dashboard />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="*" element={<Navigate to="/" />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/settings" element={<Settings />} />
              </Routes>
            </div>
          </div>
        )}
      </div>
    </Router>
  </ExchangeProvider>
  );
}

export default App;