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
    const jsonData = JSON.stringify(formData);
  };

  return (
    <div className="App">
      <div className="login-container">
        <h1>Login</h1>
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
    </div>
  );
}


export default LogIn;