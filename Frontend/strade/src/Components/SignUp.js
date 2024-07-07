import React, { useState } from 'react';
import '../Styles/SignUp.css';
import '../Styles/App.css';
import { countryOptions } from './countryOptions';
import { default as axios } from 'axios';
import { useNavigate } from 'react-router-dom';

/**Function to POST the signup data to the server.
 * 
 * @param credentials: All the potential data the server can accept, including username, password, name, mail, etc.
*/
async function signupUser(credentials) {
  try {
    // Send a POST request to the signup endpoint
    await axios.post('http://localhost:8001/register/', credentials);
  } catch (error) {
    console.error('Error during signup:', error); // Log any errors that occurred during the login process
    throw error; // Re-throw the error so it can be handled by the calling code
  }
}

/**The Signup website, including all the different inputs the user has to take and send to the server */
export default function SignUp () {
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    firstname: '',
    lastname: '',
    birthday: '',
    eMail: '',
    phone_number: '',
    address:'',
    country: '',
    login_name: '',
    password: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };
  /**Formats the data in the correct order for the database to then send it to the server.
   * 
   * If the registration happens without errors, the user will be redirected to the homepage.
  */
  const handleSubmit = async e => {
    e.preventDefault();
    try {
      await signupUser({
        firstname: formData.firstname,
        lastname: formData.lastname,
        birthday: formData.birthday,
        eMail: formData.eMail,
        phone_number: formData.phone_number,
        address: formData.address,
        country: formData.country,
        login_name: formData.login_name,
        password: formData.password});
      window.alert("Registration successful");
      navigate('/');
    } catch (error) {
      window.alert("Registration failed");
    }
  };

  return (
    <div className="App">
    <form className="signup-form" onSubmit={handleSubmit}>
      <h1>Sign up</h1>
      <input
        type="text"
        name="login_name"
        placeholder="Enter Username"
        value={formData.login_name}
        onChange={handleChange}
        required
      />
      <input
        type="text"
        name="firstname"
        placeholder="Enter first name"
        value={formData.firstname}
        onChange={handleChange}
        required
      />
      <input
        type="text"
        name="lastname"
        placeholder="Enter last name"
        value={formData.lastname}
        onChange={handleChange}
        required
      />
      <input
        type="date"
        name="birthday"
        placeholder="DD/MM/YYYY"
        value={formData.birthday}
        onChange={handleChange}
        required
      />
      <select
        name="country"
        value={formData.country}
        onChange={handleChange}
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
        name="address"
        placeholder="Enter Adress"
        value={formData.address}
        onChange={handleChange}
        />
      <input
        type="text"
        name="phone_number"
        placeholder="Enter Phone Number (optional)"
        value={formData.phone_number}
        onChange={handleChange}
      />
      <input
        type="email"
        name="eMail"
        placeholder="Enter Email"
        value={formData.eMail}
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
        onChange={handleChange}
        required
      />
      <button type="submit">Sign up</button>
    </form>
    </div>
  );
};