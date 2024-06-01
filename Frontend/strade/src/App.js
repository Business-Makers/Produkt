import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import './App.css';
import './LoggedIn.css';
import Homepage from './Homepage';
import LogIn from './LogIn';
import SignUp from './SignUp';
import Subscription from './Subscription';
import Dashboard from './Dashboard';
import useToken from './useToken';
import SideNav from './SideNav';
import Trading from './Trading';

/**The Navigation of the whole Frontend: 
 * 
 * Depending on if the User is logged in (decided by the Token's status), different navigation paths are accessible
 * 
 * This is implemented via the use of the BrowserRouter from the package 'react-router-dom'.*/ 
function App() {

  const { token, setToken } = useToken();

  if(!token) {
    return (
    <Router>
      <div className="App">
        <header className="App-header">
          <nav className="nav">
            <div className="logo">
              <Link to="/">
                <img src="/strade.png" alt="logo"/>
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
            <Route path="/login" element={<LogIn setToken={setToken}/>} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/" element={<Homepage />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </main>
        <footer className="App-footer">

          <div className="footer-content">
            <p>&copy; 2024 $TRADE</p>
            <Link to="/impressum">Impressum</Link>  {/* Link to Impressum */}
            <Link to="/datenschutz">Datenschutz</Link>  {/* Add Link to Datenschutz-stuff */}
          </div>
        </footer>
      </div>
    </Router>
    );
  }

  return (
    <Router>
      <div className="App2">
        <header className="App-header2">
          <SideNav />
        </header>
        <div className="main-content">
          <Routes>
            <Route path="/subscription" element={<Subscription />} />
            <Route path="/trading" element={<Trading />} />
            <Route path="/" element={<Dashboard />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </div>
      </div>
    </Router>
  );

}

export default App;