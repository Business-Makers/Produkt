import React, { useState } from 'react';
import './App.css';
import { FaEye, FaEyeSlash } from 'react-icons/fa';
import { Link } from 'react-router-dom';

function LogIn() {
  const [formData, setFormData] = useState({
    usernameOrEmail: '',
    password: ''
  });
  const [passwordVisible, setPasswordVisible] = useState(false);

  const togglePasswordVisibility = () => {
    setPasswordVisible(!passwordVisible);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Hier kannst du die Formularvalidierung und das Absenden hinzufügen
    console.log('Form data:', formData);
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
        <form onSubmit={handleSubmit} className="input-container">
          <input
            type="text"
            name="usernameOrEmail"
            placeholder="Enter Username or Email"
            className="input-field"
            value={formData.usernameOrEmail}
            onChange={handleChange}
            required
          />
          <div className="password-container">
            <input
              type={passwordVisible ? 'text' : 'password'}
              name="password"
              placeholder="Enter Password"
              className="input-field"
              value={formData.password}
              onChange={handleChange}
              required
            />
            <span
              onClick={togglePasswordVisibility}
              className="password-toggle-icon"
            >
              {passwordVisible ? <FaEyeSlash /> : <FaEye />}
            </span>
          </div>
          <button type="submit" className="login-button">Login</button>
          <p>
            Don't have an account? <Link to="/signup">Sign up</Link>
          </p>
        </form>
      </div>
      <footer className="App-footer">
        <a href="#">Impressum</a>
        <a href="#">About us</a>
      </footer>
    </div>
  );
}


export default LogIn;