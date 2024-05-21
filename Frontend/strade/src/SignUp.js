import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './SignUp.css';
import './App.css';
import { countryOptions } from './countryOptions';

const SignUp = () => {
  const [formData, setFormData] = useState({
    username: '',
    firstName: '',
    lastName: '',
    birthDate: '',
    country: '',
    phoneNumber: '',
    email: '',
    password: '',
    confirmPassword: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Form data:', formData);
  };

  return (
    <div className="App">
    <form className="signup-form" onSubmit={handleSubmit}>
      <h1>Sign up</h1>
      <input
        type="text"
        name="username"
        placeholder="Enter Username"
        value={formData.username}
        onChange={handleChange}
        required
      />
      <input
        type="text"
        name="firstName"
        placeholder="Enter first name"
        value={formData.firstName}
        onChange={handleChange}
        required
      />
      <input
        type="text"
        name="lastName"
        placeholder="Enter last name"
        value={formData.lastName}
        onChange={handleChange}
        required
      />
      <input
        type="date"
        name="birthDate"
        placeholder="DD/MM/YYYY"
        value={formData.birthDate}
        onChange={handleChange}
        required
      />
      <select
        name="country"
        value={formData.country}
        onChange={handleChange}
        required
      >
        <option value="">Select Country</option>
          {countryOptions.map((country) => (
            <option key={country.value} value={country.value}>
              {country.label}
            </option>
          ))}
        
      </select>
      <input
        type="text"
        name="phoneNumber"
        placeholder="Enter Phone Number (optional)"
        value={formData.phoneNumber}
        onChange={handleChange}
      />
      <input
        type="email"
        name="email"
        placeholder="Enter Email"
        value={formData.email}
        onChange={handleChange}
        required
      />
      <input
        type="password"
        name="password"
        placeholder="Enter Password"
        value={formData.password}
        onChange={handleChange}
        required
      />
      <input
        type="password"
        name="confirmPassword"
        placeholder="Confirm Password"
        value={formData.confirmPassword}
        onChange={handleChange}
        required
      />
      <button type="submit">Sign up</button>
    </form>
    </div>
  );
};

export default SignUp;