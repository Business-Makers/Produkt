import React, { useState } from 'react';
import './App.css';
import { Link } from 'react-router-dom';
import { default as axios } from 'axios';

async function loginUser(credentials) {
  try {
    // Send a POST request to the login endpoint
    const response = await axios.post('http://localhost:8000/login', credentials);
    return response.data;

  } catch (error) {
    console.error('Error during login:', error); // Log any errors that occurred during the login process
    throw error; // Re-throw the error so it can be handled by the calling code
  }
}

export default function LogIn({ setToken }) {
  const [username, setUserName] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const data = await loginUser({login_name: username, password: password});
      setToken("logged_in"); // TODO: Das hier ist absolut unsicher, dafuer muessen wir noch richtige Tokens verwenden.
      console.log('Login successful:', data);
    } catch (error) {
      console.error('Login failed:', error);
    }
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
            value={username}
            onChange={(e) => setUserName(e.target.value)}
            required
          />
          <div className="password-container">
            <input
              type="password"
              name="password"
              placeholder="Enter Password"
              className="input-field"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
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
