import React, { useState } from 'react';
import './App.css';
import { Link } from 'react-router-dom';


async function loginUser(credentials) {
  return fetch('http://localhost:8000/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(credentials)
  })
    .then(data => data.json())
 }

export default function LogIn({ setToken}) {
  const [formData, setFormData] = useState({
    usernameOrEmail: '',
    password: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async e => {
    e.preventDefault();
    const token = await loginUser({
      formData
    });
    setToken(token);
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
              type="password"
              name="password"
              placeholder="Enter Password"
              className="input-field"
              value={formData.password}
              onChange={handleChange}
              required
            />
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
