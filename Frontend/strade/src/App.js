import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import './App.css';
import Homepage from './Homepage';
import LogIn from './LogIn';
import SignUp from './SignUp';
import Subscription from './Subscription';

function App() {
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

            <Link to="/subscription">Subscription</Link>
              <Link to="/signup">Sign Up</Link>
              <Link to="/login">Login</Link>
            </nav>
          </nav>
        </header>
        <main>
          <Routes>
          <Route path="/subscription" element={<Subscription />} />
            <Route path="/login" element={<LogIn />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/" element={<Homepage />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </main>
        <footer className="App-footer">

          <div className="footer-content">
            <p>&copy; 2024 $TRADE</p>
            <Link to="/impressum">Impressum</Link>  {/* Link zum Impressum */}
            <Link to="/datenschutz">Datenschutz</Link>  {/* Link für Datenschutz hinzufügen */}
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;