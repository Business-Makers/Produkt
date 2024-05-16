import React, { useState } from 'react';
import './App.css';
import { FaEye, FaEyeSlash } from 'react-icons/fa';
import { Link } from 'react-router-dom';

function LogIn() {
  const [passwordVisible, setPasswordVisible] = useState(false);

  const togglePasswordVisibility = () => {
    setPasswordVisible(!passwordVisible);
  };

  return (
    <div className="App">
      <header className="App-header">
        <div className="logo">
            <Link to="/">
                <img src="/strade.png" alt="Logo" />
            </Link>
        </div>
        <nav className="nav">
          <Link to="/signup">Sign up</Link>
          <Link to="#">Support</Link>
        </nav>
      </header>
      <div className="login-container">
        <h2>Login</h2>
        <div className="input-container">
          <input
            type="text"
            placeholder="Enter Username or Email"
            className="input-field"
          />
          <div className="password-container">
            <input
              type={passwordVisible ? 'text' : 'password'}
              placeholder="Enter Password"
              className="input-field"
            />
            <span
              onClick={togglePasswordVisibility}
              className="password-toggle-icon"
            >
              {passwordVisible ? <FaEyeSlash /> : <FaEye />}
            </span>
          </div>
          <button className="login-button">Login</button>
          <p>
            Don't have an account? <Link to="/signup">Sign up</Link>
          </p>
        </div>
      </div>
      <footer className="App-footer">
        <a href="#">Impressum</a>
        <a href="#">About us</a>
      </footer>
    </div>
  );
}

export default LogIn;