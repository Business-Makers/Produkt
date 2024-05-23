import React, { useState} from 'react';
import { BrowserRouter as Router, Routes, Route, Link, Navigate } from 'react-router-dom';
import './App.css';
import Homepage from './Homepage';
import LogIn from './LogIn';
import SignUp from './SignUp';
import Dashboard from './Dashboard';
import useToken from './useToken';

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
            <nav className="nav">
            <Link to="/login">Login</Link>
            <Link to="/signup">Sign Up</Link>
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
        <footer className = "App-footer">
          <Link to="/">Impressum</Link>
          <Link to="/">About us</Link>
        </footer>
      </div>
    </Router>
    );
  }

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
            <nav className="nav">
            <Link to="/login">Test</Link>
            <Link to="/signup">Klappt</Link>
            </nav>
          </nav>
        </header>
        <main>
          <Routes>
            <Route path="/login" element={<LogIn />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/" element={<Dashboard />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </main>
        <footer className = "App-footer">
          <Link to="/">Impressum</Link>
          <Link to="/">About us</Link>
        </footer>
      </div>
    </Router>
  );

}

export default App;
