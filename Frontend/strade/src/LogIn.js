import React, { useState } from 'react';
import './App.css';
import { Link } from 'react-router-dom';


async function loginUser(username) {
  try {
    // Send a POST request to the login endpoint
    const response = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json' // Inform the server that the body contains JSON
      },
      body: JSON.stringify({ login_name: username }) // Convert the username into JSON format
    });

    // Check if the response is not ok (status code is not in the 200-299 range)
    if (!response.ok) {
      throw new Error('Failed to log in'); // Throw an error if the login failed
    }

    // Parse the JSON response and return it
    return response.json();
  } catch (error) {
    console.error('Error during login:', error); // Log any errors that occurred during the login process
    throw error; // Re-throw the error so it can be handled by the calling code
  }
}

export default function LogIn({ setToken }) {
  const [username, setUserName] = useState();
  const [password, setPassword] = useState();

  const handleSubmit = async e => {
    e.preventDefault();
    try {
      const data = await loginUser(username);
      setToken(data.token); // Assuming the API response contains the token
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
            onChange={e => setUserName(e.target.value)}
            required
          />
          <div className="password-container">
            <input
              type="password"
              name="password"
              placeholder="Enter Password"
              className="input-field"
              onChange={e => setPassword(e.target.value)}
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
